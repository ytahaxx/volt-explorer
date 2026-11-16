import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from flask import Flask, jsonify, render_template, request

from config import Config
from database import models
from database.db import close_db, connect, init_db
from routes import assistant, main, programme, quiz, search
from services.quiz_service import QuizService
from services.rag_service import RagService


def create_app(config_object=Config, overrides=None):
    app = Flask(__name__)
    app.config.from_object(config_object)

    if overrides:
        app.config.update(overrides)

    if not Path(app.config["DATABASE"]).exists():
        init_db(app.config["DATABASE"], app.config["PROPOSITIONS_JSON"])

    app.teardown_appcontext(close_db)

    conn = connect(app.config["DATABASE"])
    try:
        propositions = models.list_all_propositions(conn)
    finally:
        conn.close()

    app.extensions["quiz_service"] = QuizService(app.config["QUIZ_JSON"])
    app.extensions["rag_service"] = RagService(propositions, app.config)

    for module in (main, programme, search, quiz, assistant):
        app.register_blueprint(module.bp)

    @app.errorhandler(404)
    def not_found(_e):
        if request.path.startswith("/api/"):
            return jsonify(error="Ressource introuvable."), 404
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed(_e):
        if request.path.startswith("/api/"):
            return jsonify(error="Méthode non autorisée."), 405
        return render_template("404.html"), 405

    @app.errorhandler(500)
    def server_error(_e):
        if request.path.startswith("/api/"):
            return jsonify(error="Erreur interne du serveur."), 500
        return render_template("404.html", error500=True), 500

    return app


# Instance Flask principale
app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "0") == "1"
    )
