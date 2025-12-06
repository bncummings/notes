# decision_trees

## File structure

- **src/**  
- **tree.py** — decision tree algorithm  
    - **evaluate.py** — evaluation utilities: ten-fold cross-validation, confusion matrix, metrics, and classification
    - **load.py** — example script to train a tree and visualise it with matplotlib
- **wifi_db/**  
    - **clean_dataset.txt** — clean WiFi dataset
    - **noisy_dataset.txt** — noisy version of the dataset  
- **requirements.txt**
- **README.md**

## Installing dependencies

Ensure you have set up a [python virtual environment](https://www.imperial.ac.uk/computing/people/csg/tutorials/python/virtual-environment/) and that it is activated.

run
 ```bash
 pip install -r requirements.txt
 ```

## Training and visualising a decision tree

From the project root run:

```bash
python3 src/load.py
```

This script trains a decision tree on the clean dataset using the algorithm in `tree.py`.

It then plots a visualisation of this tree using matplotlib.

## Running the evaluation

From the project root run:

```bash
python3 src/evaluate.py
```

This script trains and evaluates our decision tree algorithm using 10-fold cross validation on the datasets in `wifi_db/` (expects `clean_dataset.txt` and `noisy_dataset.txt`). It prints total confusion matrices and metrics (accuracy, precision, recall, f1) for trees trained on each of the datasets.

The decision trees are created using the algorithm in `tree.py`.

Place datasets in `wifi_db/` relative to the project root or update paths in `src/evaluate.py` if running from a different working directory.