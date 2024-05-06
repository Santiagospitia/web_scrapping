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
OPENCRITICS_API_KEY = os.getenv("OPENCRITICS_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

prompt = 'Eres un gran captador de sentimientos a través de texto. A continuación, te voy a pasar una lista de reseñas de un videojuego y me gustaría que me dijeras, según las reseñas, por qué el juego es bueno y por qué el juego es malo. Seperandolo en títulos respectivamente, es decir, colocar **POR QUÉ EL JUEGO ES BUENO** y **POR QUÉ EL JUEGO ES MALO**. Por favor, pasame el texto en prosa, es decir, no hagas listas con las cosas buenas y malas, sino que hablame en prosa. Aquí tienes las reseñas: '


@app.route('/')
def index():
    return 'Hola mundo'

#Se obtienen las reseñas de un videojuego de la página de OpenCritic y de RAWG, se concatenan y se envían al modelo para que genere un texto con las razones por las que el juego es bueno y malo.
@app.route('/analyze/<id>/<string:game_name>')
def analyze(id,game_name):
    try:
        reviews1 = get_reviews(id,game_name)['reviews']
        reviews_text1 = [review['text'] for review in reviews1]

        try:
            reviews2 = get_rawg_review(game_name)['reviews']
            reviews_text2 = [review['text'] for review in reviews2]
        except Exception as e:
            reviews_text2 = []
            print(f"Error obteniendo reviews de RAWG: {str(e)}")

        reviews_text = reviews_text1 + reviews_text2
        reviews_string = ' '.join(reviews_text)

        response = model.generate_content(prompt + reviews_string)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#webscrapping a la página de OpenCritic para obtener las reseñas de un videojuego.
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


#webscrapping a la página de RAWG para obtener las reseñas de un videojuego.
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
        print("error: ",str(e))
        return jsonify({"error": str(e)}), 500


#Se utiliza una API para obtener la lista de videojuegos que coinciden con la palabra que ingresa el usuario.
@app.route('/search/<string:game_name>')
def search_game(game_name):
    options = {
        'method': 'GET',
        'url': 'https://opencritic-api.p.rapidapi.com/game/search',
        'params': {'criteria': game_name},
        'headers': {
            'X-RapidAPI-Key': OPENCRITICS_API_KEY,
            'X-RapidAPI-Host': 'opencritic-api.p.rapidapi.com'
        }
    }

    try:
        response = requests.request(**options)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)