"""Web application functions

Rico & Robert
2021/09/20"""


from flask import Flask, render_template, request


def create_app():
    """Create App"""

    app = Flask(__name__)

    
    @app.route('/')
    def base():
        """Creates the home page"""

        return 'Spotify API'

    @app.route('/song_suggestor')
    def song_suggestor():
        """Create a suggestor route"""

        return 'song suggestions'


    return app