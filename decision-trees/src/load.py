import numpy as np
from tree import dec_tree_learning
from plot import plot_tree

if __name__ == "__main__":
    (tree, max_depth) = dec_tree_learning(np.loadtxt("./wifi_db/clean_dataset.txt"), 0)
    plot_tree(tree, max_depth)
