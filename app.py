import os

from flask import Flask, Response, jsonify


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/api/hello")
    def hello():
        return jsonify({"message": "hello"}), 200

    @app.route("/api/hello/text")
    def hello_text():
        return Response("Hello from plain text\n", mimetype="text/plain; charset=utf-8")

    @app.route("/api/hello/ping")
    def hello_ping():
        return jsonify({"kind": "ping", "ok": True}), 200

    @app.route("/api/hello/meta")
    def hello_meta():
        endpoints = [
            "/api/hello",
            "/api/hello/text",
            "/api/hello/ping",
            "/api/hello/meta",
        ]
        return jsonify({"service": "tests_in_CI", "endpoints": endpoints}), 200

    return app


# Для gunicorn: gunicorn --factory app:create_app ...
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    create_app().run(host="0.0.0.0", port=port, debug=False)
