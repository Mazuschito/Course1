from flask import Flask, Blueprint

from bp_api.views import bp_api
from bp_posts.views import bp_posts
import config_logger

from exceptions.data_exceptions import DataSourceError


def create_and_config_app(config_path):
    """Setup the app"""
    app = Flask(__name__)

    app.register_blueprint(bp_posts)
    app.register_blueprint(bp_api, url_prefix="/api/")
    app.config.from_pyfile(config_path)
    config_logger.config(app)

    return app


app = create_and_config_app("config.py")


@app.errorhandler(404)
def page_error_404(error):
    return f"This page does not exist {error}", 404


@app.errorhandler(500)
def page_error_500(error):
    return f"Error on the server - {error}", 500


@app.errorhandler(DataSourceError)
def page_error_data_source_error(error):
    return f"Error on the server, data is damaged - {error}", 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
