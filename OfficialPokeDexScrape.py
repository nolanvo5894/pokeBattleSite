from bs4 import BeautifulSoup as soup

from urllib.request import urlopen as uOpen
from urllib.request import urlretrieve as uRetrieve

import numpy as np
import pandas as pd

poke = pd.read_csv('../pokemon.csv') #this file should be put in a container folder for all images
poke['Type 2'].fillna(poke['Type 1'], inplace = True) #for every Pokemon with no Type 2, Type 2 is set to be the same with Type 1
poke.set_index('#', inplace = True) #without this, 800 would be lost
poke['Name'].fillna('Primeape', inplace = True)
pokeList = list(poke['Name'].values)

pokeListMega = [poke for poke in pokeList if 'Mega' in poke]
#pokeListMega

pokeListNormal = [poke for poke in pokeList if 'Mega' not in poke and 'Primal' not in poke]
#pokeListNormal

pokeListNormalUnique = [poke.split(' ')[0] for poke in pokeListNormal if 'Nidoran' not in poke]
pokeListNormalUnique.append('Nidoran')
pokeListNormalUniqueSet = set(pokeListNormalUnique)
#pokeListNormalUniqueSet

pokeURLs = ['https://www.pokemon.com/us/pokedex/' + poke for poke in pokeListNormalUniqueSet]

def getPokeImage(pokeURL):
    pokeBaseName = pokeURL.split('/')[-1] #Charizard is the pokeBaseName for Charizard and the two Mega forms
    pokemon = uOpen(pokeURL)
    pokePage = pokemon.read()
    pokeSoup = soup(pokePage, 'html.parser')
    pokeProfile = pokeSoup.findAll('div',{'class':'profile-images'})[0]
    pokeImages = pokeProfile.findAll('img')
    pokeNames = [pokeImage['alt'] for pokeImage in pokeImages]
    pokePicLinks = [pokeImage['src'] for pokeImage in pokeImages]
    pokePicTuple = list(zip(pokePicLinks, pokeNames))
    for pokePicLink,pokeName in pokePicTuple:
        if pokeBaseName not in pokeName:
            pokePic = uRetrieve(pokePicLink, pokeBaseName + ' ' + pokeName + '.png')
        else:
            pokePic = uRetrieve(pokePicLink, pokeName + '.png')

if __name__ == '__main__':
    for pokeURL in pokeURLs:
    try:
        getPokeImage(pokeURL)
    except:
        print(pokeURL)

    #Frost, Heat, Mow, Fan, and Wash are sub-type of the pokemon Rotom Mime Jr. and Mr. Mime are just weird (who might have guess :D) Farfetch'd has that ' which make it special too.

    pokeExceptURLs = ['https://www.pokemon.com/us/pokedex/mime-jr','https://www.pokemon.com/us/pokedex/flabebe','https://www.pokemon.com/us/pokedex/nidoran-male','https://www.pokemon.com/us/pokedex/nidoran-female','https://www.pokemon.com/us/pokedex/farfetchd', 'https://www.pokemon.com/us/pokedex/mr-mime']
    for pokeURL in pokeExceptURLs:
        getPokeImage(pokeURL)
