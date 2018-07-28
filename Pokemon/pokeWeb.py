from flask import Flask, render_template, request, url_for, session
from sklearn.externals import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    poke = pd.read_csv('pokemon.csv')
    pokeList = list(poke['Name'])
    return render_template('index.html', pokeList = pokeList)

@app.route('/battleStage', methods = ['POST'])
def battleStage():
    if request.method == 'POST':
        pokeFirst = request.values.get('pokeFirst')
        pokeSecond = request.values.get('pokeSecond')
        session['pokeFirst'] = pokeFirst
        session['pokeSecond'] = pokeSecond
        return render_template('battleStage.html', pokeFirst = pokeFirst, pokeSecond = pokeSecond)

@app.route('/predict', methods = ['POST']) #without setting methods to 'POST', getting an error page with 'Method Not Allowed'
def predict():
    if request.method == 'POST':
        # pokeFirst = request.values.get('pokeFirst')
        # pokeSecond = request.values.get('pokeSecond')
        pokeFirst = session.get('pokeFirst')
        pokeSecond = session.get('pokeSecond')

        #loading stat features for first and second pokemons
        pokeStats = joblib.load('pokeStats.pkl')

        firstHP = pokeStats[pokeStats['Name'] == pokeFirst]['HP']
        firstAttack = pokeStats[pokeStats['Name'] == pokeFirst]['Attack']
        firstDefense = pokeStats[pokeStats['Name'] == pokeFirst]['Defense']
        firstSpAtk = pokeStats[pokeStats['Name'] == pokeFirst]['Sp. Atk']
        firstSpDef = pokeStats[pokeStats['Name'] == pokeFirst]['Sp. Def']
        firstSpeed = pokeStats[pokeStats['Name'] == pokeFirst]['Speed']
        firstLegendary = pokeStats[pokeStats['Name'] == pokeFirst]['Legendary']

        secondHP = pokeStats[pokeStats['Name'] == pokeSecond]['HP']
        secondAttack = pokeStats[pokeStats['Name'] == pokeSecond]['Attack']
        secondDefense = pokeStats[pokeStats['Name'] == pokeSecond]['Defense']
        secondSpAtk = pokeStats[pokeStats['Name'] == pokeSecond]['Sp. Atk']
        secondSpDef = pokeStats[pokeStats['Name'] == pokeSecond]['Sp. Def']
        secondSpeed = pokeStats[pokeStats['Name'] == pokeSecond]['Speed']
        secondLegendary = pokeStats[pokeStats['Name'] == pokeSecond]['Legendary']

        typeChart = joblib.load('typeChart.pkl')

        firstType1 = pokeStats[pokeStats['Name'] == pokeFirst]['Type 1']
        firstType2 = pokeStats[pokeStats['Name'] == pokeFirst]['Type 2']
        secondType1 = pokeStats[pokeStats['Name'] == pokeSecond]['Type 1']
        secondType2 = pokeStats[pokeStats['Name'] == pokeSecond]['Type 2']

        # typeChart.loc[firstType1][secondType1] returns a DataFrame object with 1 row x 1 column. squeeze() turns it into np.float64
        typeMatch = typeChart.loc[firstType1][secondType1].squeeze() * typeChart.loc[firstType2][secondType2].squeeze() * typeChart.loc[firstType1][secondType2].squeeze() * typeChart.loc[firstType2][secondType1].squeeze()

        pokeModel = joblib.load('pokeModel.pkl')
        X = np.array([firstHP, firstAttack, firstDefense, firstSpAtk, firstSpDef, firstSpeed, firstLegendary, secondHP, secondAttack, secondDefense, secondSpAtk, secondSpDef, secondSpeed, secondLegendary, typeMatch])
        X = X.reshape(1,-1) #this suggestion from the error page works, but why? sklearn only accepts 2D array?
        winner = pokeModel.predict(X)

        if winner == 0:
            winner = pokeFirst
        else:
            winner = pokeSecond

        return render_template('predict.html', pokeFirst = pokeFirst, pokeSecond = pokeSecond, winner = winner)

if __name__ == '__main__':
    app.secret_key = 'pokemonBattle'
    app.run(debug = True)
