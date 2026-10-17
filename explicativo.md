# TicTacToeML — Tres en Raya con Minimax y Machine Learning

Documento para alguien que no sabe nada del proyecto y quiere
comprenderlo por completo: qué es, cómo funciona, dónde está cada
cosa y por qué se hizo así.

## 1. Qué es este proyecto

Una app web del juego Tres en Raya (3x3) con tres modos:

1. **Humano vs Humano (hvh):** dos personas juegan en el mismo navegador.
2. **Humano vs IA Minimax (hvai):** juegas con X y la máquina responde
   con O calculando la mejor jugada exacta.
3. **Humano vs IA ML (hvml):** juegas con X y la máquina responde con O
   usando un árbol de decisión aprendido (rápido, casi siempre óptimo).

Además la app muestra métricas educativas: nodos explorados y tiempo
de respuesta de la IA, y el dibujo del árbol aprendido.

## 2. Cómo se usa (2 minutos)

```bash
pip install -r requirements.txt
python3 app.py
```

Abre `http://127.0.0.1:5000`. Elige modo, haz clic en una casilla,
pulsa Reiniciar cuando quieras. En modo ML hay un enlace "Ver árbol".

## 3. Arquitectura MVC (la idea central)

- **Modelo (`model/`):** reglas y cerebro. No sabe nada de HTML.
- **Vista (`templates/`, `static/`):** solo muestra. No decide jugadas.
- **Controlador (`controller/`):** recibe clics, llama al modelo/IA
  y devuelve la página. `app.py` solo registra rutas.

Flujo de una jugada: clic → `POST /move` → `controller.move()` →
`model.play_turn()` (y si toca IA, `_juega_ia()` o `_juega_ml()`) →
`redirect /` → `controller.index()` → `index.html`.

Rutas en `app.py`: `GET /`, `POST /move`, `POST /reset`,
`POST /mode`.

## 4. Reglas del juego (`model/game_model.py`)

`TicTacToeModel` guarda `board` (matriz 3x3 con `' '`, `'X'`, `'O'`)
y `current_player`. Métodos clave:

- `is_valid_move(move)`: dentro del tablero y vacía.
- `get_available_moves()`: lista las casillas libres (las ramas).
- `make_move(move, player)` / `undo_move(move)`: poner y quitar ficha.
  Esto es **backtracking**: probar sin copiar el tablero.
- `check_winner(player)`, `is_draw()`, `is_game_over()`.
- `play_turn(move)`: valida, coloca, mira si hay win/draw y si no
  cambia de turno. Devuelve `invalid/win/draw/continue`.

## 5. Evaluación (`model/evaluation.py`)

Convención fija: Humano = X, IA = O. La nota es desde la vista de la IA:

- `+10` gana O, `-10` gana X, `0` empate, `None` partida abierta.
- `evaluate(board)` usa `_wins()` (filas, columnas, 2 diagonales)
  y `_is_full()`.

`None` significa "no es hoja, sigue buscando". Sin esto Minimax no
sabría cuándo parar.

## 6. Minimax (`model/minimax_agent.py`)

`best_move(juego)` prueba cada jugada legal con make/undo y se queda
con la de mayor valor. `_minimax(board, es_maximo, nodos)`:

- Suma `nodos[0] += 1` por estado visitado (fin educativo).
- Si `evaluate()` no es `None`, retorna esa nota.
- Si es turno IA maximiza (`max`), si es humano minimiza (`min`).

Ejemplo real medido: tablero vacío explora ~550.000 nodos; una
respuesta típica ~59.704 nodos / ~479 ms. Exacto pero costoso.

## 7. Datos sintéticos (`model/ml_agent.py`, `data/dataset.csv`)

Como no tenemos miles de humanos jugando, simulamos:
aleatorio (X) vs Minimax (O) y anotamos lo que el experto hizo.

- `encode_board()`: 3x3 → 9 números (0=vacío, 1=X, 2=O, por filas).
- `decode_label()`: etiqueta 0-8 → `(fila, columna)`.
- `generate_dataset(n_games, csv_path, seed)`: por cada turno de O
  guarda `c0..c8,label`. Con 300 partidas salen ~1072 filas.
  Para 1000 partidas: `generate_dataset(1000)`.

## 8. Modelo ML (`model/train_model.py`, `model/tictactoe_dt.joblib`)

`train()` lee el CSV con pandas, separa 80% entrenar / 20% probar,
entrena `DecisionTreeClassifier`, calcula accuracy, guarda el modelo
con `joblib` y dibuja `static/tree.png` con `plot_tree(max_depth=4)`.

Resultado obtenido: train 1.000, test 0.930 con 1072 filas.
El árbol aprende preguntas tipo `c4 <= 1.5` hasta predecir la casilla.

## 9. IA ML en la web (`controller/game_controller.py`)

`modo` puede ser `hvh`, `hvai` o `hvml`. `_juega_ml()`:

1. Carga el `.joblib` una sola vez (lazy, sin romper si falta).
2. Codifica el tablero y hace `predict()` (~1 ms).
3. Valida con `is_valid_move()`; si es ilegal, fallback a Minimax
   (se marca `nodos=-1` = "ML fallback", si fue directo `nodos=0`).
4. Mide todo con `time.perf_counter()` → `ultimo_tiempo_ms`.

Comparativa medida en 100 estados: ML 0.50 ms vs Minimax
126 ms por jugada (~250x más rápido), acuerdo 99%.

## 10. Interfaz (`templates/index.html`, `static/styles.css`)

- Selector de modo (`hvh`/`hvai`/`hvml`), estado (turno/ganador),
  tablero 3x3 con formularios (sin JS de juego), botón Reiniciar.
- Métricas solo en modos IA: `Nodos` + `Tiempo IA`. En ML muestra
  `ML directo` o `ML fallback Minimax`.
- `static/styles.css`: tarjeta centrada, celdas 84px, X azul, O rojo.
- `static/tree.png`: imagen del árbol aprendido.

## 11. Estructura de archivos

```text
app.py                        rutas Flask
controller/game_controller.py modos, mensajes, IA, metricas
model/game_model.py           reglas + backtracking
model/evaluation.py           +10/-10/0/None
model/minimax_agent.py        busqueda exacta + nodos
model/ml_agent.py             simulacion + encode/decode
model/train_model.py          entrenamiento + grafico
model/tictactoe_dt.joblib     modelo aprendido
data/dataset.csv              1072 estados etiquetados
templates/index.html          vista
static/styles.css, tree.png   estilo + arbol
requirements.txt              Flask, sklearn, pandas, matplotlib
```

## 12. Glosario mínimo

- **Estado:** un tablero concreto. **Terminal:** alguien ganó o empate.
- **Backtracking:** probar y deshacer con make/undo.
- **Heurística:** nota +10/-10/0 de una hoja.
- **Minimax:** maximizar lo propio minimizando lo rival.
- **Dataset:** tabla estado → mejor jugada. **Label:** jugada 0-8.
- **Accuracy:** % de aciertos en test. **Latencia:** ms por jugada.
- **Fallback:** si ML propone ilegal, usa Minimax.
