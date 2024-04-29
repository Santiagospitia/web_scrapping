from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hola mundo'


@app.route('/reviews/<id>/<string:game_name>')
def get_reviews(id,game_name):
    try:
        opencritic_url = f'https://opencritic.com/game/{id}/{game_name}/reviews?sort=newest'
        response = requests.get(opencritic_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = []
        for review in soup.find_all('p', class_='mb-0 wspw'):
            text = review.text.strip()
            reviews.append({'text': text})
        return {'reviews': reviews}
    except Exception as e:
        return jsonify({"error": str(errh)}), 500


@app.route('/search/<string:game_name>')
def search_game(game_name):
    options = {
        'method': 'GET',
        'url': 'https://opencritic-api.p.rapidapi.com/game/search',
        'params': {'criteria': game_name},
        'headers': {
            'X-RapidAPI-Key': 'c35c71d756msh7a289352821bdb6p172b17jsn0c43e3135bf2',
            'X-RapidAPI-Host': 'opencritic-api.p.rapidapi.com'
        }
    }

    try:
        response = requests.request(**options)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)