"""Launcher for the h9_v0 request assistant Flask app."""

from __future__ import annotations

import os

from request_ai_agent_h9_v0.config import load_local_env


load_local_env()

from request_ai_agent_h9_v0 import create_app


app = create_app()


if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "8503"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
