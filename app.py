"""Bootstrap Flask estilo envWeb-main: solo registra rutas."""
from flask import Flask # type: ignore
from controller.game_controller import index, move, reset

app = Flask(__name__)

# Registro de rutas (como en envWeb-main/app.py)
app.add_url_rule("/", view_func=index, methods=["GET"])
app.add_url_rule("/move", view_func=move, methods=["POST"])
app.add_url_rule("/reset", view_func=reset, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)
