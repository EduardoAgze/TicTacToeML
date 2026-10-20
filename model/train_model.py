"""Entrena un arbol de decision y guarda el modelo."""

import os

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

CSV = "data/dataset.csv"
MODEL = "model/tictactoe_dt.joblib"

FEATURES = [f"c{i}" for i in range(9)]
TEST_SIZE = 0.2
RANDOM_STATE = 42


def _ensure_parent(path):
    """Crea la carpeta destino si no existe.

    Args:
        path: Ruta de archivo cuyo directorio se desea asegurar.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)


def train(csv_path=CSV, model_path=MODEL):
    """Entrena, evalua y guarda el modelo.

    Args:
        csv_path: Ruta del dataset de entrada.
        model_path: Ruta donde guardar el modelo entrenado.

    Returns:
        Tupla (accuracy_train, accuracy_test, n_rows).
    """
    df = pd.read_csv(csv_path)
    X = df[FEATURES].values
    y = df["label"].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    clf = DecisionTreeClassifier(random_state=RANDOM_STATE)
    clf.fit(X_train, y_train)
    acc_train = accuracy_score(y_train, clf.predict(X_train))
    acc_test = accuracy_score(y_test, clf.predict(X_test))

    _ensure_parent(model_path)
    joblib.dump(clf, model_path)

    return acc_train, acc_test, len(df)


if __name__ == "__main__":
    tr, te, n = train()
    print(f"Filas: {n} train={tr:.3f} test={te:.3f}")
