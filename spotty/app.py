"""Web application functions

Robert Davis
2021/09/20"""


from flask import Flask, render_template, request


def create_app():
    """Creates the application"""

    app = Flask(__name__)



    return app