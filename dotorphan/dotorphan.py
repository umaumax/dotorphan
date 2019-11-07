#!/usr/bin/env python3

import sys

import argparse
import networkx


def pygraphviz_module_assert():
    import importlib.util
    pygraphviz_spec = importlib.util.find_spec("pygraphviz")
    found = pygraphviz_spec is not None
    if not found:
        print("not found pygraphviz", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gui', action='store_true', help='show graph (requires: pygraphviz)')
    parser.add_argument('--agrpah-prog', default='dot', type=str, help='graph drawing prog (neato, dot, twopi, circo, fdp, nop, wc, acyclic, gvpr, gvcolor, ccomps, sccmap, tred, sfdp, unflatten)')
    parser.add_argument('--exclude', default=['main'], type=str, nargs='*', help='exclude node names')
    parser.add_argument('-o', '--output', default='', type=str, help='output filepath (dot, svg, png, pdf, ...)')
    parser.add_argument('input', type=str, help='input dot file')

    args, extra_args = parser.parse_known_args()

    G = networkx.DiGraph(networkx.drawing.nx_pydot.read_dot(args.input))

    filtered_graph = networkx.DiGraph()

    if len(extra_args) > 0:
        print("found extra args {}".format(extra_args), file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    exclude_nodes = args.exclude
    print(exclude_nodes)
    print('# all orphan nodes')
    for node in list([k for k, v in G.degree() if v == 0 and k not in exclude_nodes]):
        print(node)
        filtered_graph.add_node(node)

    print('# all orphan edges')
    for edges in list([G.edges(component) for component in networkx.connected_components(G.to_undirected()) if len(G.edges(component)) > 0 and len(set(exclude_nodes) & set(component)) == 0]):
        print(edges)
        filtered_graph.add_edges_from(edges)

    if args.gui:
        pygraphviz_module_assert()
        networkx.nx_agraph.view_pygraphviz(G, prog=args.agrpah_prog)
    if args.output:
        pygraphviz_module_assert()
        agrpah = networkx.nx_agraph.to_agraph(filtered_graph)
        agrpah.draw(args.output, prog=args.agrpah_prog)


if __name__ == '__main__':
    main()
