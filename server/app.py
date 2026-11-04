"""Central DLP server and dashboard entry point."""

from flask import Flask, jsonify, render_template


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def dashboard():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    # TODO: add policy management and agent event endpoints.
    return app


if __name__ == "__main__":
    create_app().run(debug=True)
