"""Flask application entry point and web dashboard."""
from flask import Flask, render_template

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    from server.routes.policies import bp as policies_bp
    from server.routes.events import bp as events_bp
    from server.routes.agents import bp as agents_bp
    app.register_blueprint(policies_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(agents_bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/")
    def dashboard():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=False)
