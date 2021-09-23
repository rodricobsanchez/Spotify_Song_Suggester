"""Web application functions

Robert & Rodrico
2021/09/20"""


from .recomend import get_nn_query, query_nn_pickles, recomend, search
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import requests
import pickle
import os


attriname = ['Acousticness', 'Danceability', 'Duration (ms)', 'Energy',
    'Instrumentalness', 'Liveness', 'Loudness', 'Speechiness', 'Tempo',
    'Valence']


def create_app():
    """Create App"""

    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def song_suggestor():
        """Create a suggestor route"""
        link = request.get_data('link')
        message = ''
        attributes = []
        results = False
        links = []

        if link:
            print(link)
            # if 'spot.spotify.com' in str(link):
            #     try:
            #         # WHY MUST IT SCREW ME LIKE THIS
            #         link = str(link)[48:70]
            #         # ^^^ ACTUAL CRINGE ^^^

            #         links, features = recomend(link)

            #         for x in range(10):
            #             attributes.append(f'{attriname[x]}: {features[x]}')
            #     except:
            #         message = 'Invalid Link'
            # else:
            try:
                searchy = str(link).split('=')[1][:-1].replace('=', ' ')
                results = search(searchy)

                links, features = recomend(results['id'])

                for x in range(10):
                    attributes.append(f'{attriname[x]}: {features[x]}')
            except:
                message = 'No results found'

        return render_template('testsuggestor.html',
            links=links, message=message, attr=attributes, song=results)


    return app
