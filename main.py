from flask import Flask, render_template, request
import database_manager as dbHandler

app = Flask(__name__)

@app.route('/index.html', methods=['GET'])
@app.route('/', methods=['POST', 'GET'])
def index():
    data = dbHandler.listExtension()
    return render_template('index.html', content=data)

@app.route('/games', methods=['GET'])
def games():
    return render_template('games.html')

@app.route('/players', methods=['GET'])
def show_players():
    return render_template('partials/players.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)