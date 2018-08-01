from bs4 import BeautifulSoup as soup

from urllib.request import urlopen as uOpen
from urllib.request import urlretrieve as uRetrieve

import numpy as np
import pandas as pd

poke = pd.read_csv('../pokemon.csv') # this file should be put in a container folder for all images
poke['Type 2'].fillna(poke['Type 1'], inplace = True) # for every Pokemon with no Type 2, Type 2 is set to be the same with Type 1
poke.set_index('#', inplace = True) # without this, 800 would be lost
poke['Name'].fillna('Primeape', inplace = True)
pokeList = list(poke['Name'].values)

# pokeListMega is the List of all Mega pokemons in pokeList
pokeListMega = [poke for poke in pokeList if 'Mega' in poke]

# pokeListNormal is the List of all pokemons that are not Mege or Primal pokemons in pokeList
pokeListNormal = [poke for poke in pokeList if 'Mega' not in poke and 'Primal' not in poke]

# Since there are pokemons with many formes and their names start with the same word, need to trimmed pokeListNormal to a list of unique words.
# This is done by first filtering out only the original names, followed by getting a Set of the list of original names.
# The scraping process only need the original names of these pokemons and will scrape pictures of all formes.
# Also, since male and female Nidoran has the weird male and female symbol in their names, stripping those off and replacing with just Nidoran. Again, the scraper will get pictures of both genders.
pokeListNormalUnique = [poke.split(' ')[0] for poke in pokeListNormal if 'Nidoran' not in poke]
pokeListNormalUnique.append('Nidoran')
pokeListNormalUniqueSet = set(pokeListNormalUnique)
# pokeListNormalUniqueSet

pokeURLs = ['https://www.pokemon.com/us/pokedex/' + poke for poke in pokeListNormalUniqueSet]

# function for download the images of pokemons from the PokeDex website given names of the pokemons
def getPokeImage(pokeURL):
    # getting the basename of the pokemon
    pokeBaseName = pokeURL.split('/')[-1] #Charizard is the pokeBaseName for Charizard and the two Mega forms Mega Charizard X and Mega Charizard Y
    # open the URL for that pokemon and read in the html
    pokemon = uOpen(pokeURL)
    pokePage = pokemon.read()
    pokeSoup = soup(pokePage, 'html.parser')
    # pictures are linked to in divs of class profile-images
    pokeProfile = pokeSoup.findAll('div',{'class':'profile-images'})[0]
    pokeImages = pokeProfile.findAll('img')
    # the 'alt' attribute stores the names of the pokemons
    pokeNames = [pokeImage['alt'] for pokeImage in pokeImages]
    # the 'src' attribute stores the links to the pictures of the pokemons
    pokePicLinks = [pokeImage['src'] for pokeImage in pokeImages]
    pokePicTuple = list(zip(pokePicLinks, pokeNames))
    # given the name and the link of a pokemon, uRetrieve can download its picture
    for pokePicLink,pokeName in pokePicTuple:
        # sometimes the 'alt' attribute does have the basename of the pokemon, so need to add it in to the name of the png file.
        if pokeBaseName not in pokeName:
            pokePic = uRetrieve(pokePicLink, pokeBaseName + ' ' + pokeName + '.png')
        else:
            pokePic = uRetrieve(pokePicLink, pokeName + '.png')

if __name__ == '__main__':
    for pokeURL in pokeURLs:
    try:
        getPokeImage(pokeURL)
    except:
        # there are some pokemon with weird names that the scraper cannot catch, their names are printed out here
        print(pokeURL)

    # the weird pokemons are handled with seperately
    # Frost, Heat, Mow, Fan, and Wash are sub-type of the pokemon Rotom
    # Mime Jr. and Mr. Mime are just weird (who might have guess :D) Farfetch'd has that ' which make it special too.

    pokeExceptURLs = ['https://www.pokemon.com/us/pokedex/mime-jr','https://www.pokemon.com/us/pokedex/flabebe','https://www.pokemon.com/us/pokedex/nidoran-male','https://www.pokemon.com/us/pokedex/nidoran-female','https://www.pokemon.com/us/pokedex/farfetchd', 'https://www.pokemon.com/us/pokedex/mr-mime']
    for pokeURL in pokeExceptURLs:
        getPokeImage(pokeURL)
