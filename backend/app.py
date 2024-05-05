from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os   

load_dotenv()
app = Flask(__name__)
CORS(app)


API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

prompt = 'Eres un gran captador de sentimientos a través de texto. A continuación, te voy a pasar una lista de reseñas de un videojuego y me gustaría que me dijeras, según las reseñas, por qué el juego es bueno y por qué el juego es malo. Seperandolo en títulos respectivamente, es decir, colocar POR QUÉ EL JUEGO ES BUENO y POR QUÉ EL JUEGO ES MALO. Por favor, pasame el texto en prosa, es decir, no hagas listas con las cosas buenas y malas, sino que hablame en prosa. Aquí tienes las reseñas: '


@app.route('/')
def index():
    return 'Hola mundo'


@app.route('/analyze/<id>/<string:game_name>')
def analyze(id,game_name):
    try:
        revies = get_reviews(id,game_name)['reviews']
        reviews_text = [review['text'] for review in revies]
        reviews_string = ' '.join(reviews_text)
        response = model.generate_content(prompt + reviews_string)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#@app.route('/reviews/<id>/<string:game_name>')
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
        return jsonify({"error": str(e)}), 500

@app.route('/rawg_analyze/<game_name>')
def analyze_rawg(game_name):
    revies = get_rawg_review(game_name)['reviews']
    reviews_text = [review['text'] for review in revies]
    reviews_string = ' '.join(reviews_text)
    response = model.generate_content(prompt + reviews_string)
    return jsonify({'response': response.text})

def get_rawg_review(game_name):
    try:    
        rawg_url = f'https://rawg.io/games/{game_name}'

        response = requests.get(rawg_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = []
        count = 0

        cards_view = soup.find_all('div', class_='review-card__text')

        for card in cards_view:
            text = card.text.strip()
            reviews.append({"text":text})

        return {"reviews":reviews}

    except Exception as e:
        return jsonify({"error": str(e)})

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