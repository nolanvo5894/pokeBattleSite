import os

path = os.getcwd()

files = os.listdir(path)

for file in files:
    if os.path.isdir(file):

        picPath = os.path.join(path,file)
        pics = os.listdir(picPath)
        for pic in pics:
            os.rename(os.path.join(picPath, pic),os.path.join(picPath, file + '.png'))
