from mega.mega import Mega

def download_single(email,password,url):
    #Make new mega
    mega = Mega({'verbose': True})
    m = mega.login(email, password)
    print 'Downloading... '
    print url
    m.download_url(url)

def getlinks():
    print 'Opening links.dat'
    file=open('links.dat','r')
    links = [line[4:] for line in file]
    links = [x.rstrip() for x in links]
    file.close()
    return links
