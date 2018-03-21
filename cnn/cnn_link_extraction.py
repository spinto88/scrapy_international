import dryscrape
import time
import cPickle as pk
import datetime
from copy import deepcopy

sess = dryscrape.Session()

for i in range(1000):

    try:
        sess.visit('https://edition.cnn.com/search/?q=politics&size=10&from={}'.format(i*10))
      
        links = sess.xpath('//h3[@class="cnn-search__result-headline"]//a[@href]')
 
        hrefs = [link['href'] for link in links]

        fp = open('links_cnn.txt','a')
        for href in set(hrefs):
            fp.write('http:{}\n'.format(href))
        fp.close()

    except:
        pass

    time.sleep(2)

sess.reset()

