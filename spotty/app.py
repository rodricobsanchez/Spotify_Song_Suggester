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
        <h3><a href="/">Home</a></h3>

        <form action="/song_suggestor", method="POST">
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

    
    @app.route('/')
    def base():
        """Creates the home page"""

        return render_template('testindex.html')

    @app.route('/song_suggestor', methods=['GET', 'POST'])
    def song_suggestor():
        """Create a suggestor route"""
        link = request.get_data('link')
        if link:
            try:
                # WHY MUST IT SCREW ME LIKE THIS
                link = str(link)[41:63]
                # ^^^ ACTUAL CRINGE ^^^

                links = recomend(link)
                print(links)

                template = """            <li><a href=\"{link}\">{link}\
</a></li>
"""
                blank = """"""
                for link in links:
                    blank += template.format(link=link)
            except:
                blank = """            <p>Invalid Track ID</p>"""
        else:
            blank = """            <p>Similar songs will go here</p>"""

        return suggestHTML.format(blank)


    return app
