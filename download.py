from mega import Mega
from multiprocessing import Process
import credentials as c

def getlinks():
    print 'Opening links.dat'
    file=open('links.dat','r')
    links = [line[4:] for line in file]
    links = [x.rstrip() for x in links]
    file.close()
    return links

def download_single(email,password,url):
    mega = Mega({'verbose': True})
    m = mega.login(email, password)
    print 'Downloading... '
    print url
    m.download_url(url)
    
def main():
    details=c.logmein()
    email = details[0]
    password = details[1]
    links=getlinks()
    pp=[]
    for url in links :
        pp.append(Process(target=download_single, args=(email,password,url)))
    for k in pp :
        k.start()
    for j in pp :
        k.join()

if __name__ is '__main__':
    main()
