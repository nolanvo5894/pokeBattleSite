# pokeBattleSite

This is the source code for a web app that lets the user pick 2 pokemons from the list of all pokemons up to Gen VII, and outputs the winner of the battle between these 2 chosen pokemons. The app is publicly available at: https://awesomepokebattle.herokuapp.com<br/>
The model for this app was trained on data from https://www.kaggle.com/terminus7/pokemon-challenge and can be found in Model.ipynb. <br/>
The Pokemon type chart was downloaded from https://github.com/zonination/pokemon-chart. <br/>
The framework used to make the app is Flask. <br/>
Pictures of pokemons used for the app was scraped from the official Pokedex from Nintendo https://www.pokemon.com/us/pokedex/ using code in OfficialPokeDexScrape.ipynb. <br/>
Considering new features:
* A browser for Pokemons with their pictures, stats, fun facts, etc.
* A search option in addition to dropdown selection.
* Team mode: battles are between teams of Pokemons, not just individual ones.
