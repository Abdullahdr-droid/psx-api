from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ PSX API is live!"

@app.route('/api/stock/<symbol>')
def get_stock(symbol):
    url = f'https://dps.psx.com.pk/quote/{symbol.upper()}'
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data'}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        price_tag = soup.select_one('.price-box .price')
        change_tag = soup.select_one('.price-box .change')
        return jsonify({
            'symbol': symbol.upper(),
            'price': price_tag.text.strip(),
            'change': change_tag.text.strip()
        })
    except:
        return jsonify({'error': 'Symbol not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
