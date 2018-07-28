import os

path = os.getcwd()
filenames = os.listdir(path)

for file in filenames:
    os.rename(file, file.split('.png')[0])
