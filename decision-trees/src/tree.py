import numpy as np
import math

Node = dict[str, object] # {’attribute’, ’value’, ’left’, ’right’, 'leaf', 'label'}
Decision = tuple[int, float] # (entry/attribute, value)
Distribution = dict[int, int] # classification -> count
Data = list[list]

def dec_tree_learning(training_data: Data, depth: int) -> tuple[Node, int]:
    """ Recursively generates a decision tree from a training data set. """

    if not len(training_data):
        return None, depth
    
    # base case: all samples have the same label
    first_label = training_data[0][-1]
    if all(x[-1] == first_label for x in training_data):
        return {"leaf" : True, "label": first_label}, depth
    
    attr, value = find_split(training_data)
    node = {"attribute" : attr, "value" : value, "leaf" : False}

    left_data, right_data  = split_data(training_data, attr, value)
    node["left"], l_depth  = dec_tree_learning(left_data, depth + 1)
    node["right"], r_depth = dec_tree_learning(right_data, depth + 1)

    return node, max(l_depth, r_depth)

def split_data(training_data, attr, value) -> tuple[Data, Data]:
    """ Splits data into two subsets based on an inequality at a given attribute index. """

    left_data = []
    right_data = []

    for entry in training_data:
        if entry[attr] < value:
            left_data.append(entry)
            continue
        right_data.append(entry)

    return left_data, right_data

def calculate_info_gain(
        total_distribution: Distribution, 
        data_l: Distribution, 
        data_r: Distribution
) -> float:
    """ Calculate the information gained by a split by analysing 
    the entropy of the left and right sets. """
    
    def _size(distr: Distribution) -> int: 
        return sum(distr.values())
    
    def _entropy(distr: Distribution) -> float:
        entropy: float  = 0
        size = _size(distr)

        for v in distr.values(): 
            if v == 0: continue

            p = v / size
            entropy -= np.log2(p) * p
               
        return entropy

    l_size, r_size = _size(data_l), _size(data_r)
    total_size = l_size + r_size

    if not total_size: 
        return 0.0

    left_ent  = _entropy(data_l) * l_size
    right_ent = _entropy(data_r) * r_size
    remainder = (left_ent + right_ent) / total_size

    return _entropy(total_distribution) - remainder

def find_split(data: Data) -> Decision:
    """ Finds the optimal Decision to split the data, maximising information gain. """

    labels: set[int] = get_labels(data)
    n_rows = len(data)
    total_distribution = get_distribution(data, labels)
    max_info_gain = -math.inf
    split = (0, 0.0)

    for col_i in range(len(data[0]) - 1):
        # sort the data by parameter col_i
        sorted_data = sorted(data, key=lambda x: x[col_i])

        left_counts = dict.fromkeys(labels, 0)
        right_counts = total_distribution.copy()

        for row_i in range(n_rows - 1):
            if sorted_data[row_i][col_i] == sorted_data[row_i + 1][col_i]:
                continue

            split_value = (sorted_data[row_i][col_i] + sorted_data[row_i + 1][col_i]) / 2

            # add the data value from right distribution to left.
            label = int(sorted_data[row_i][-1])
            left_counts[label] += 1
            right_counts[label] -= 1

            # compare with max info gain.
            info_gain = calculate_info_gain(total_distribution, left_counts, right_counts)
            if info_gain > max_info_gain:
                max_info_gain = info_gain
                split = col_i, split_value
   
    return split

def get_labels(data: Data) -> set[int]:
    """ Returns the set of labels which appear in the data. """

    return {int(entry[-1]) for entry in data}

def get_distribution(data: Data, labels: set[int]) -> Distribution:
    """ Generates a label distribution from a list of data. """

    # Initialize total counts for each label to 0
    distr = dict.fromkeys(labels, 0)

    # Count class frequencies
    for row in data:
        label = row[-1]
        distr[label] += 1

    return distr
