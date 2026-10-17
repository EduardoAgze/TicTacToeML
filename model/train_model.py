"""Entrena DecisionTree con el dataset y exporta modelo + grafico."""

import os

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree

from model.ml_agent import decode_label  # noqa: F401 (documenta formato)

CSV = "data/dataset.csv"
MODEL = "model/tictactoe_dt.joblib"
PNG = "static/tree.png"


def train(csv_path=CSV, model_path=MODEL, png_path=PNG):
    """Entrena, evalua y guarda modelo y grafico.

    Returns:
        (accuracy_train, accuracy_test, n_rows).
    """
    import pandas as pd

    df = pd.read_csv(csv_path)
    X = df[[f"c{i}" for i in range(9)]].values
    y = df["label"].values
    xtr, xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(xtr, ytr)
    acc_tr = accuracy_score(ytr, clf.predict(xtr))
    acc_te = accuracy_score(yte, clf.predict(xte))

    os.makedirs(os.path.dirname(model_path) or ".", exist_ok=True)
    joblib.dump(clf, model_path)

    os.makedirs(os.path.dirname(png_path) or ".", exist_ok=True)
    plt.figure(figsize=(20, 10))
    plot_tree(clf, filled=True, max_depth=4,
              feature_names=[f"c{i}" for i in range(9)],
              class_names=[str(i) for i in range(9)])
    plt.tight_layout()
    plt.savefig(png_path)
    plt.close()
    return acc_tr, acc_te, len(df)


if __name__ == "__main__":
    tr, te, n = train()
    print(f"Filas: {n} train={tr:.3f} test={te:.3f}")
