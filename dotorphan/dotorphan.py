#!/usr/bin/env python3

import json
import os
import os.path
import re
import subprocess
import sys
import tempfile
import argparse

import networkx


def demangle(input_file_object, output_file_object, verbose=True):
    args = ['c++filt', '-n']
    pipe = subprocess.Popen(args, stdin=input_file_object,
                            stdout=output_file_object)
    _, errs = pipe.communicate()
    if errs:
        print(
            "[log] c++filt demangle failed: {}".format(errs),
            file=sys.stderr)
        return False
    return True


def pygraphviz_module_assert():
    import importlib.util
    pygraphviz_spec = importlib.util.find_spec("pygraphviz")
    found = pygraphviz_spec is not None
    if not found:
        print("not found pygraphviz", file=sys.stderr)
        sys.exit(1)


def remove_nodes(graph, node_names, verbose=True):
    # NOTE: simple method without warning
    # graph.remove_nodes_from(node_names)
    for node_name in node_names:
        if graph.has_node(node_name):
            graph.remove_node(node_name)
        else:
            if verbose:
                print("[remove_nodes] not found node name '{}'".format(
                    node_name), file=sys.stderr)
            return False
    return True


def remove_traversed_nodes_regex(graph, node_patterns, verbose=True):
    detected_node_names = []
    for node_pattern in node_patterns:
        matcher = re.compile(node_pattern)
        for node in list([n for n in graph.nodes() if matcher.search(n)]):
            print(
                "[remove_traversed_nodes_regex]"
                " match {} by '{}' regex pattern".format(
                    node, node_pattern), file=sys.stderr)
            detected_node_names.append(str(node))
    # NOTE: remove nodes after detection
    graph.remove_nodes_from(list(set([element for tuple in list(
        networkx.edge_dfs(graph, detected_node_names)) for element in tuple]+detected_node_names)))
    return True


def remove_traversed_nodes(graph, node_names, verbose=True):
    detected_node_names = []
    for node_name in node_names:
        if graph.has_node(node_name):
            detected_node_names.append(node_name)
        else:
            if verbose:
                print(
                    "[remove_traversed_nodes] not found node name '{}'".format(
                        node_name),
                    file=sys.stderr)
            return False
    # NOTE: remove nodes after detection
    graph.remove_nodes_from(list(set([element for tuple in list(
        networkx.edge_dfs(graph, detected_node_names)) for element in tuple]+detected_node_names)))
    return True


def uniq_nodes_from_edges_list(head_node, edges_list):
    duplicated_nodes = list(
        [element for tupl in list(edges_list) for element in tupl])
    # for orphan root node (without edges)
    unique_nodes = [head_node] if head_node else []
    [unique_nodes.append(item)
     for item in duplicated_nodes if item not in unique_nodes]
    return unique_nodes


def run(input, output_filepath, orphan_info_output, args):
    filtered_node_graph = networkx.DiGraph()
    filtered_edge_graph = networkx.DiGraph()
    # NOTE: input type: filename or file object
    print("# [log] parse file", file=sys.stderr)
    G = networkx.DiGraph(networkx.drawing.nx_pydot.read_dot(input))
    if args.relabel:
        G = networkx.relabel_nodes(
            G, lambda x: str(G.nodes[x]['label']).strip(args.relabel_strip_chars) if 'label' in G.nodes[x] else x)

    print("# [log] remove_traversed_nodes", file=sys.stderr)
    ret = remove_traversed_nodes_regex(
        G, args.remove_traversed) if args.regex else remove_traversed_nodes(
        G, args.remove_traversed)
    if not ret:
        return False
    print("# [log] remove_nodes", file=sys.stderr)
    ret = remove_nodes(G, args.remove)
    if not ret:
        return False

    orphan_info = {
        'node_list': [],
        'nodes_list': [],
        'root_node_list': [],
        'root_nodes_list': [],
    }
    orphan_info_output.write('# orphan nodes' + '\n')
    orphan_info_output.flush()
    for node in list([n for n, v in G.degree() if v == 0]):
        orphan_info_output.write(node+'\n')
        filtered_node_graph.add_node(node)
        orphan_info['node_list'].append(node)
    orphan_info_output.flush()

    orphan_info_output.write('# orphan edges' + '\n')
    orphan_info_output.flush()
    for edges in list([G.edges(component) for component in networkx.connected_components(
            G.to_undirected()) if len(G.edges(component)) > 0]):
        orphan_info_output.write(str(edges) + '\n')
        filtered_edge_graph.add_edges_from(edges)
        unique_nodes = uniq_nodes_from_edges_list(None, edges)
        orphan_info['nodes_list'].append(unique_nodes)
    orphan_info_output.flush()

    # NOTE: get root nodes
    orphan_info_output.write('# orphan root nodes' + '\n')
    root_nodes = [n for n, d in G.in_degree() if d == 0]
    orphan_info_output.write(str(root_nodes) + '\n')
    orphan_info['root_node_list'].extend(root_nodes)
    orphan_info_output.flush()

    def set_root_node_style(node):
        node['fillcolor'] = 'lightgreen'
        node['style'] = 'filled'

    cnt = 0
    orphan_info_output.write('# orphan edges from root node' + '\n')
    orphan_info_output.flush()
    for node in root_nodes:
        unique_nodes = []
        if filtered_node_graph.has_node(node):
            set_root_node_style(filtered_node_graph.nodes[node])
            unique_nodes = [node]
        if filtered_edge_graph.has_node(node):
            set_root_node_style(filtered_edge_graph.nodes[node])
            unique_nodes = uniq_nodes_from_edges_list(
                node, networkx.edge_dfs(filtered_edge_graph, [node]))
        orphan_info_output.write('[{}]{}\n'.format(cnt, str(unique_nodes)))
        orphan_info['root_nodes_list'].append(unique_nodes)
        cnt += 1
    orphan_info_output.flush()

    print("# [log] json output:",
          args.orphan_info_json_output, file=sys.stderr)
    with open(args.orphan_info_json_output, 'w') as f:
        json.dump(orphan_info, f, ensure_ascii=False, indent=2)

    for _, attrs in filtered_node_graph.nodes(data=True):
        attrs['shape'] = 'box'
    for _, attrs in filtered_edge_graph.nodes(data=True):
        attrs['shape'] = 'box'

    # get all nodes & edges of both graphs, including attributes
    # where the attributes conflict, it uses the attributes of 2nd graph
    filtered_combined_graph = networkx.compose(
        filtered_node_graph, filtered_edge_graph)

    def insert_key_before_filepath(filepath, key):
        return "{0}_{2}{1}".format(*os.path.splitext(filepath) + (key,))

    if output_filepath:
        print("# [log] file output", file=sys.stderr)
        pygraphviz_module_assert()
        agrpah = networkx.nx_agraph.to_agraph(filtered_combined_graph)
        agrpah.graph_attr.update(ranksep='5.0')
        agrpah.draw(output_filepath, prog=args.agrpah_prog)
        if args.split_output:
            print("# [log] gen splited file", file=sys.stderr)
            agrpah = networkx.nx_agraph.to_agraph(filtered_node_graph)
            agrpah.graph_attr.update(ranksep='5.0')
            agrpah.draw(insert_key_before_filepath(
                output_filepath, 'node'), prog=args.agrpah_prog)
            agrpah = networkx.nx_agraph.to_agraph(filtered_edge_graph)
            agrpah.graph_attr.update(ranksep='5.0')
            agrpah.draw(insert_key_before_filepath(
                output_filepath, 'edge'), prog=args.agrpah_prog)
    if args.gui:
        print("# [log] gui output", file=sys.stderr)
        pygraphviz_module_assert()
        if not networkx.is_empty(filtered_combined_graph):
            networkx.nx_agraph.view_pygraphviz(
                filtered_combined_graph, prog=args.agrpah_prog)
        else:
            print("# [log] filtered graph is empty", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--no-demangle',
        action='store_true',
        help='without demangle c++ symbol')
    parser.add_argument(
        '--relabel',
        action='store_false',
        help='relabel node name by label attr')
    parser.add_argument(
        '--relabel-strip-chars',
        default='{}"',
        type=str,
        help='relabel strip chars')
    parser.add_argument(
        '--regex',
        action='store_true',
        help="enable regex of --remove-traversed e.g. '^main$'")
    parser.add_argument(
        '--gui',
        action='store_true',
        help='show graph (requires: pygraphviz)')
    parser.add_argument(
        '--agrpah-prog',
        default='dot',
        type=str,
        help='graph drawing prog (neato, dot, twopi, circo, fdp, nop, wc, acyclic, gvpr, gvcolor, ccomps, sccmap, tred, sfdp, unflatten)')
    parser.add_argument(
        '--remove',
        default=['external node'],
        type=str,
        nargs='*',
        help='remove node names')
    parser.add_argument(
        '--remove-traversed',
        default=['main'],
        type=str,
        nargs='*',
        help='remove nodes traversed from these node names')
    parser.add_argument(
        '--split-output',
        action='store_true',
        help='split output file to (combined, node, edge)')
    parser.add_argument(
        '-o',
        '--output',
        default='',
        type=str,
        help='output filepath (dot, svg, png, pdf, ...)')
    parser.add_argument(
        '--orphan-info-output',
        default='/dev/stdout',
        type=str,
        help='orphan info output filepath')
    parser.add_argument(
        '--orphan-info-json-output',
        default='/dev/stdout',
        type=str,
        help='orphan info json output filepath')
    parser.add_argument('input',
                        type=str, help='input dot file')

    args, extra_args = parser.parse_known_args()
    if len(extra_args) > 0:
        print("found extra args {}".format(extra_args), file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    ret = True
    with open(args.orphan_info_output, 'w') as orphan_info_file:
        if args.no_demangle:
            ret = run(args.input, args.output, orphan_info_file, args)
        else:
            with open(args.input, 'r') as input_file, \
                    tempfile.TemporaryFile(mode='w+') as tmp_output_file:
                ret = demangle(input_file, tmp_output_file)
                if ret:
                    tmp_output_file.seek(0)
                    ret = run(tmp_output_file, args.output,
                              orphan_info_file, args)
    if not ret:
        sys.exit(1)
    return True


if __name__ == '__main__':
    main()
