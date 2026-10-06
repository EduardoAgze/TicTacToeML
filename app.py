from flask import Flask

from controller.game_controller import index, move, reset

app = Flask(__name__)

app.add_url_rule("/", view_func=index, methods=["GET"])
app.add_url_rule("/move", view_func=move, methods=["POST"])
app.add_url_rule("/reset", view_func=reset, methods=["POST"])


if __name__ == "__main__":
    app.run(debug=True)
