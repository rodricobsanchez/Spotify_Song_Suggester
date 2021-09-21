"""Web application functions

Robert & Rodrico
2021/09/20"""


from .recomend import get_nn_query, query_nn_pickles, recomend
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import requests
import pickle
import os


suggestHTML = """<html>
    <head>
        <title>Test Suggestor</title>
    </head>
    <body>
        
        <h1>Test Suggestor</h1>

        <form action="/", method="POST">
            <p>Song Link:</p>
            <input type="text" name="link">
            <input type="submit" value="Submit">
        </form>

        <h2>Results</h2>
        <ol>
{}
        </ol>
        
    </body>
</html>"""


def create_app():
    """Create App"""

    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def song_suggestor():
        """Create a suggestor route"""
        link = request.get_data('link')
        if link:
            try:
                # WHY MUST IT SCREW ME LIKE THIS
                link = str(link)[48:70]
                # ^^^ ACTUAL CRINGE ^^^

                links = recomend(link)

                template = """            <li><a href=\"{link}\">{link}\
</a></li>
"""
                blank = """"""
                for link in links:
                    blank += template.format(link=link)
            except:
                blank = """            <p>Invalid Song Link</p>"""
        else:
            blank = """            <p>Similar songs will go here</p>"""

        return suggestHTML.format(blank)


    return app
