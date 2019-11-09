#!/usr/bin/env python3

import re
import subprocess
import sys
import tempfile

import argparse
import networkx


def demangle(input_file_object, output_file_object, verbose=True):
    args = ['c++filt', '-n']
    pipe = subprocess.Popen(args, stdin=input_file_object, stdout=output_file_object)
    _, errs = pipe.communicate()
    if errs:
        print("[log] c++filt demangle failed: {}".format(errs), file=sys.stderr)
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
                print("[remove_nodes] not found node name '{}'".format(node_name), file=sys.stderr)
            return False
    return True


def remove_traversed_nodes_regex(graph, node_patterns, verbose=True):
    for node_pattern in node_patterns:
        matcher = re.compile(node_pattern)
        for node in list([n for n in graph.nodes() if matcher.search(n)]):
            print("[remove_traversed_nodes_regex] match {} by '{}' regex pattern".format(node, node_pattern), file=sys.stderr)
            graph.remove_nodes_from(list(set([element for tuple in list(networkx.edge_bfs(graph, [str(node)])) for element in tuple])))
    return True


def remove_traversed_nodes(graph, node_names, verbose=True):
    for node_name in node_names:
        if graph.has_node(node_name):
            graph.remove_nodes_from(list(set([element for tuple in list(networkx.edge_bfs(graph, [node_name])) for element in tuple])))
        else:
            if verbose:
                print("[remove_traversed_nodes] not found node name '{}'".format(node_name), file=sys.stderr)
            return False
    return True


def run(input, output, log_output, args):
    filtered_graph = networkx.DiGraph()
    # NOTE: input type: filename or file object
    G = networkx.DiGraph(networkx.drawing.nx_pydot.read_dot(input))
    if args.relabel:
        G = networkx.relabel_nodes(G, lambda x: G.node[x]['label'] if 'label' in G.node[x] else x)

    ret = remove_traversed_nodes_regex(G, args.remove_traversed) if args.regex else remove_traversed_nodes(G, args.remove_traversed)
    if not ret:
        return False
    ret = remove_nodes(G, args.remove)
    if not ret:
        return False

    log_output.write('# orphan nodes' + '\n')
    for node in list([n for n, v in G.degree() if v == 0]):
        log_output.write(node)
        filtered_graph.add_node(node)

    log_output.write('# orphan edges' + '\n')
    for edges in list([G.edges(component) for component in networkx.connected_components(G.to_undirected()) if len(G.edges(component)) > 0]):
        log_output.write(str(edges) + '\n')
        filtered_graph.add_edges_from(edges)

    # NOTE: get root nodes
    log_output.write('# orphan root nodes' + '\n')
    log_output.write(str([n for n, d in filtered_graph.in_degree() if d == 0]) + '\n')

    cnt = 0
    log_output.write('# orphan edges from root node' + '\n')
    for node in [n for n, d in filtered_graph.in_degree() if d == 0]:
        # NOTE: root node color setting
        filtered_graph.node[node]['fillcolor'] = 'darkorange'
        filtered_graph.node[node]['style'] = 'filled'
        duplicated_nodes = list([element for tupl in list(networkx.edge_bfs(filtered_graph, [node])) for element in tupl])
        unique_nodes = [node]  # for orphan root node (without edges)
        [unique_nodes.append(item) for item in duplicated_nodes if item not in unique_nodes]
        log_output.write('[{}]{}\n'.format(cnt, str(unique_nodes)))
        cnt += 1

    if output:
        pygraphviz_module_assert()
        agrpah = networkx.nx_agraph.to_agraph(filtered_graph)
        agrpah.draw(output, prog=args.agrpah_prog)
    if args.gui:
        pygraphviz_module_assert()
        if not networkx.is_empty(filtered_graph):
            networkx.nx_agraph.view_pygraphviz(filtered_graph, prog=args.agrpah_prog)
        else:
            print("# [log] filtered graph is empty", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--demangle', action='store_false', help='demangle c++ symbol')
    parser.add_argument('--relabel', action='store_false', help='relabel node name by label attr')
    parser.add_argument('--regex', action='store_true', help='enable regex of --remove-traversed')
    parser.add_argument('--gui', action='store_true', help='show graph (requires: pygraphviz)')
    parser.add_argument('--agrpah-prog', default='dot', type=str, help='graph drawing prog (neato, dot, twopi, circo, fdp, nop, wc, acyclic, gvpr, gvcolor, ccomps, sccmap, tred, sfdp, unflatten)')
    parser.add_argument('--remove', default=['"{external node}"'], type=str, nargs='*', help='remove node names')
    parser.add_argument('--remove-traversed', default=['"{main}"'], type=str, nargs='*', help='remove nodes traversed from these node names')
    parser.add_argument('-o', '--output', default='', type=str, help='output filepath (dot, svg, png, pdf, ...)')
    parser.add_argument('--log-output', default='/dev/stdout', type=str, help='log output filepath')
    parser.add_argument('input', type=str, help='input dot file')

    args, extra_args = parser.parse_known_args()
    if len(extra_args) > 0:
        print("found extra args {}".format(extra_args), file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    ret = True
    with open(args.log_output, 'w') as log_file:
        if not args.demangle:
            ret = run(args.input, args.output, log_file, args)
        else:
            with open(args.input, 'r') as input_file:
                with tempfile.TemporaryFile(mode='w+') as tmp_output_file:
                    ret = demangle(input_file, tmp_output_file)
                    if ret:
                        tmp_output_file.seek(0)
                        ret = run(tmp_output_file, args.output, log_file, args)
    if not ret:
        sys.exit(1)
    return True


if __name__ == '__main__':
    main()
