#!/usr/local/bin/python3.9
import uvicorn
from flask import Flask

from src.routes.api_routes import simple_page

app = Flask(__name__)


def setup_routes(app):
    app.register_blueprint(simple_page)


setup_routes(app)

if __name__ == '__main__':
    uvicorn.run("example:app", host="0.0.0.0", port=5000, log_level="info")

