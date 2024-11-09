import xml.etree.ElementTree as ET
from graphviz import Digraph

def parse_xml_to_tree(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    dot = Digraph(comment='Behavior Tree')

    dot.attr(size='11.7,8.3')  # A4 in inches
    dot.attr(page='11.7,8.3')  # A4 in inches
    dot.attr(orientation='landscape')
    dot.attr('graph', rankdir='TB')

    dot.attr('node', fontsize='20', width='1.5', height='1.5')
    dot.attr('edge', fontsize='16')

    def add_nodes_edges(node, parent_name=None):
        node_id = f"{node.tag}_{id(node)}"
        if node.tag in ["Condition", "Action"]:
            label = f"{node.tag}: {node.attrib.get('type', '')}"
        else:
            label = f"{node.tag}: {node.attrib.get('name', '')}" if 'name' in node.attrib else node.tag

        dot.node(node_id, label)

        if parent_name:
            dot.edge(parent_name, node_id)

        for child in node:
            add_nodes_edges(child, node_id)

    add_nodes_edges(root)
    return dot

bt_dot = parse_xml_to_tree('bt.xml')

bt_dot.render('BehaviorTree', format='png')
