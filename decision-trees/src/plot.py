import matplotlib.pyplot as plt

INITIAL_WIDTH_SPACING = 40
FIG_WIDTH = 20
FONT_SCALER = 3 # A control on the amount font scales with depth
DEFAULT_MAX_DEPTH = 5

def plot_tree(tree, tree_depth):
    """ Takes in the tree and its depth and plots it. """

    global max_depth, graph
    max_depth = min(tree_depth, DEFAULT_MAX_DEPTH)
    _, graph = plt.subplots()

    # Flip the y axis so the tree grows downwards
    graph.set_ylim(max_depth, 0)

    # Plot the tree and display the plot without the axes
    plot_node(FIG_WIDTH / 2, tree, 1)
    plt.axis('off')
    plt.show()
 
def plot_node(node_x, node, depth):
    """ Takes in a node, its x position and its depth in the tree
    Plots the node and its children recursively. """

    # Draw the current node
    node_y = depth - 1
    draw_node(node, node_x, node_y)

    # If the node is a leaf or max depth reached, do not plot children
    if node["leaf"] or depth >= max_depth:
        return 

    # Plot the right child and its edge
    right_child = node["right"]
    if right_child is not None:
        right_x = node_x + INITIAL_WIDTH_SPACING / (2 ** depth)
        draw_line(node_x, right_x, node_y)
        plot_node(right_x, right_child, depth + 1)

    # Plot the left child and its edge
    left_child = node["left"]
    if left_child is not None:
        left_x = node_x - INITIAL_WIDTH_SPACING / (2 ** depth)
        draw_line(node_x, left_x, node_y)
        plot_node(left_x, left_child, depth + 1)

def draw_node(node, x, y):
    """ Draws the given node at position (x, y). """

    if node["leaf"]:
        text, color = f'Label: {node["label"]}', 'lightcoral'
    else: 
        text, color = f'X{node["attribute"]} < {node["value"]}', 'limegreen'

    plt.text(x, y, text, ha='center', bbox=dict(boxstyle="round", fc=color), 
        va='center', size=FONT_SCALER * (max_depth - y / 2))

def draw_line(x_init, x_end, y_init):
    """ Draw a line from parent to child nodes from their x positions. """

    graph.plot([x_init, x_end], [y_init, y_init + 1], color='chocolate', lw=3)
