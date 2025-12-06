import numpy as np
from tree import dec_tree_learning, Node, Data

def ten_fold_evaluate(db: Data) -> tuple[np.ndarray, dict]:
    """ Perform 10-fold cross validation on the given dataset and return 
    confusion matrix + metrics. """
    
    # shuffle data before we split into folds
    np.random.shuffle(db)

    # compute size of each fold
    fold_size = len(db) // 10
    total_confusion_matrix = np.zeros((4, 4), dtype=int)

    for i in range(10):
        # find test data for a given fold
        test_db = db[i * fold_size:(i + 1) * fold_size]
        # find train data for a given fold
        train_db = np.concatenate((db[:i * fold_size], db[(i + 1) * fold_size:]), axis=0)

        # train the decision tree on the training data
        (trained_tree, _) = dec_tree_learning(train_db, 0)
        # evaluate the decision tree on the test data and get the confusion matrix
        total_confusion_matrix += evaluate_to_cm(test_db, trained_tree)
    
    return (total_confusion_matrix, retrieve_metrics(total_confusion_matrix))

def evaluate(test_db: Data, trained_tree: Node) -> float:
    """ Return the accuracy of the trained tree on the test data only. """

    return retrieve_metrics(evaluate_to_cm(test_db, trained_tree))['accuracy']

def evaluate_to_cm(test_db: Data, trained_tree: Node) -> np.ndarray:
    """ Evaluate the trained tree on the test data and return the confusion matrix. """

    confusion_matrix = np.zeros((4, 4), dtype=int)

    # classify each entry and update confusion matrix
    for entry in test_db:
        true_label = int(entry[-1]) - 1
        predicted_label = int(classify(entry, trained_tree)) - 1
        confusion_matrix[true_label][predicted_label] += 1

    return confusion_matrix

def retrieve_metrics(confusion_matrix: np.ndarray) -> dict:
    """ Given a confusion matrix, return accuracy, precision, recall, and f1 score. """

    metrics = {
        'accuracy': round(float(np.trace(confusion_matrix) / np.sum(confusion_matrix)), 3),
        'precision': [],
        'recall': [],
        'f1_score': []
    }

    for i in range(len(confusion_matrix)):
        # number of correct predictions for class i
        num_correct = confusion_matrix[i][i]
        # number of false positives for class i
        num_false_pos = np.sum(confusion_matrix[:, i]) - num_correct
        # number of false negatives for class i
        num_false_neg = np.sum(confusion_matrix[i, :]) - num_correct

        # precision, recall, f1 score calculations
        if (num_correct + num_false_pos) > 0:
            prec = num_correct / (num_correct + num_false_pos)  
            recall = num_correct / (num_correct + num_false_neg)
        else:
            prec, recall = 0, 0

        if (prec + recall) > 0:
            f1_score = 2 * (prec * recall) / (prec + recall)
        else:
            f1_score = 0

        # append rounded metrics to lists
        metrics['precision'].append(round(float(prec), 3))
        metrics['recall'].append(round(float(recall), 3))
        metrics['f1_score'].append(round(float(f1_score), 3))

    return metrics

def classify(entry: list, tree: Node) -> int:
    """ Classify a single entry using the trained decision tree. """

    node = tree
    while not node["leaf"]:
        attr = node["attribute"]
        value = node["value"]
        if entry[attr] < value:
            node = node["left"]
        else:
            node = node["right"]

    return node["label"]

if __name__ == "__main__":
    tree, _ = dec_tree_learning(np.loadtxt("./wifi_db/clean_dataset.txt"), 0)
    noisy_dataset = np.loadtxt("./wifi_db/noisy_dataset.txt")
    clean_dataset = np.loadtxt("./wifi_db/clean_dataset.txt")
    cm, metrics = ten_fold_evaluate(clean_dataset)

    print(f"Confusion Matrix (Clean Data):\n {cm}")
    print(f"Metrics (Clean Data):\n {metrics}")

    cm, metrics = ten_fold_evaluate(noisy_dataset)

    print(f"Confusion Matrix (Noisy Data):\n {cm}")
    print(f"Metrics (Noisy Data):\n {metrics}")
