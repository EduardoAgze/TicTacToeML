"""Exporta un DecisionTreeClassifier a JSON para dibujarlo con D3.

No depende de Flask. Los ids de nodo coinciden con los que devuelve
`clf.decision_path()`, lo que permite resaltar la ruta activa.
"""

FEATURES = ["c{}".format(i) for i in range(9)]


def export_tree_json(clf, max_depth=4):
    """Convierte el arbol a un diccionario anidado.

    Args:
        clf: DecisionTreeClassifier entrenado.
        max_depth: Profundidad maxima a exportar (para legibilidad).

    Returns:
        Diccionario raiz con las claves id, samples, is_leaf,
        label, counts y, si no es hoja, feature, threshold y children.
    """
    tree = clf.tree_
    classes = [int(c) for c in clf.classes_]

    def build(node_id, depth):
        left = int(tree.children_left[node_id])
        right = int(tree.children_right[node_id])
        is_leaf = left == -1 and right == -1
        counts = [int(v) for v in tree.value[node_id][0]]
        total = sum(counts)
        best = max(range(len(counts)), key=lambda k: counts[k])
        node = {
            "id": int(node_id),
            "depth": depth,
            "samples": total,
            "is_leaf": is_leaf,
            "label": classes[best] if is_leaf else None,
            "counts": counts,
        }
        if is_leaf:
            return node
        node["feature"] = FEATURES[int(tree.feature[node_id])]
        node["threshold"] = round(float(tree.threshold[node_id]), 2)
        if depth >= max_depth:
            node["truncated"] = True
            node["children"] = []
        else:
            node["children"] = [
                build(left, depth + 1),
                build(right, depth + 1),
            ]
        return node

    return build(0, 0)


def active_path(clf, x_row):
    """Devuelve los ids de nodo que visita el arbol para un estado.

    Args:
        clf: DecisionTreeClassifier entrenado.
        x_row: Lista de 9 enteros (0=vacio, 1=X, 2=O).

    Returns:
        Lista de enteros con los ids de nodo del recorrido.
    """
    camino = clf.decision_path([x_row])
    return [int(i) for i in camino.indices]
