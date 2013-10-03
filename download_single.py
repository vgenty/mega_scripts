import credentials as c
import os,sys
from mega import Mega

def download_single():
#Account info
    details=c.logmein()
    email = details[0]
    password = details[1]
    
#Make new mega
    mega = Mega({'verbose': True})
    m = mega.login(email, password)
    url=sys.argv[1]
    print 'Downloading... '
    print url
    m.download_url(url)
    

download_single()
