# 🎮 Tres en Raya: Minimax + Machine Learning

Un Tres en Raya hecho con **Flask** para jugar y comparar dos formas de inteligencia artificial:

- **Minimax**, que piensa las jugadas futuras.
- **Machine Learning**, con un árbol de decisión que aprende a imitar a Minimax.

La interfaz muestra en vivo cuántos **nodos** exploró la IA y cuánto **tiempo** tardó en decidir.

---

## 🕹️ Modos de juego

| Modo | Descripción |
|------|-------------|
| 👥 **Humano vs Humano** | Dos personas juegan en el mismo tablero. |
| 🤖 **Humano vs IA (Minimax)** | La IA usa Minimax con dificultad ajustable. |
| 🧠 **Humano vs IA (ML)** | La IA usa un árbol de decisión entrenado con partidas de Minimax. |

El humano juega con **X** y la IA con **O**.

### Dificultad de Minimax

| Nivel | Profundidad | Comportamiento |
|-------|-------------|----------------|
| 🟢 Fácil | 1 jugada | Solo mira su jugada inmediata. |
| 🟡 Medio | 2 jugadas | Ve tu respuesta y bloquea amenazas simples. |
| 🔴 Difícil | Hasta el final | Juega de forma perfecta. |

> La dificultad solo aplica al modo Minimax. El modelo de ML es uno solo.
> Al cambiar de modo o dificultad, la partida se reinicia.

---

## 🚀 Cómo iniciarlo

Desde la raíz del proyecto:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abre **http://127.0.0.1:5000** en el navegador.

> El proyecto ya incluye el dataset y el modelo entrenado, así que puedes jugar sin regenerar nada.

---

## 🧠 Cómo funciona

### Minimax

Minimax imagina la partida como un árbol de jugadas:

- Si gana la IA: **+10**
- Si gana el humano: **-10**
- Empate: **0**
- Si nadie ha ganado: sigue explorando

Para no repetir trabajo usa **backtracking**: prueba una jugada, explora, la deshace y prueba otra. La dificultad limita cuántas jugadas hacia adelante puede mirar. Si llega al límite y nadie ha ganado, ese estado vale **0**.

### Machine Learning

1. `model/ml_agent.py` simula partidas de Minimax contra un jugador aleatorio.
2. Guarda cada tablero junto a la jugada óptima en `data/dataset.csv`.
3. `model/train_model.py` entrena un árbol de decisión con esos datos.
4. Al jugar, el modelo predice una casilla. Si la predicción es inválida, la app usa Minimax como respaldo.

El dataset incluido tiene **1072 estados** generados a partir de **300 partidas**.

---

## 📊 Métricas

- **Nodos:** cantidad de estados que revisó la IA. Menos nodos = menos pensó.
- **Tiempo IA:** milisegundos que tardó en elegir la jugada.
- **ML directo / fallback:** indica si jugó el modelo o si tuvo que usar Minimax como respaldo.

---

## 📁 Estructura

```text
TicTacToeML/
├── app.py
├── controller/
│   └── game_controller.py
├── model/
│   ├── game_model.py
│   ├── evaluation.py
│   ├── minimax_agent.py
│   ├── ai_service.py
│   ├── session.py
│   ├── ml_agent.py
│   ├── train_model.py
│   └── tictactoe_dt.joblib
├── data/
│   └── dataset.csv
├── templates/
│   └── index.html
├── static/
│   └── styles.css
├── requirements.txt
└── README.md
```

---

## 🔁 Regenerar dataset y modelo

El dataset y el modelo ya están incluidos. Si quieres regenerarlos:

```bash
# 1. Generar nuevas partidas (puede tardar unos minutos)
python -m model.ml_agent

# 2. Entrenar y guardar el modelo
python -m model.train_model
```

> Ejecuta estos comandos desde la raíz del proyecto. Usa `python -m ...`; si ejecutas `python model/ml_agent.py`, Python no encontrará el paquete `model`.

---

## 🎓 ¿Qué puedes aprender con este proyecto?

- Búsqueda en árboles, recursión y backtracking.
- Evaluación de estados y búsqueda con profundidad limitada.
- Generación de datasets sintéticos y entrenamiento de un clasificador.
- Separación de responsabilidades entre modelo, servicio, sesión y controlador.

---

## 🛠️ Tecnologías

- Python 3
- Flask
- scikit-learn
- pandas
- joblib

---

## 💡 Notas

- Es un proyecto educativo: el modo ML aprende de un dataset pequeño y no es perfecto; el fallback a Minimax evita jugadas ilegales.
- `app.py` usa `debug=True`, ideal para desarrollo local, no para producción.
