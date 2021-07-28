import os
from PIL import Image

types = ['train', 'test', 'validation']

for t in types :
    path = "./old"+t
    file_list = os.listdir(path)

    for file in file_list :
        im = Image.open('./old'+t+'/'+file)
        im.save('./'+t+'/'+file.split('.')[0]+'.jpg')