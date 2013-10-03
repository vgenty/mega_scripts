import os,sys
from mega import Mega
import credentials as c

def upload_single(filename):
    #Account info
    details=c.logmein()
    email = details[0]
    password = details[1]
    
    #Make new mega
    
    mega = Mega()
    m = mega.login(email, password)
    print 'Uploading: ' + filename
    uploaded = m.upload(filename)
    print 'Uploaded, public link: '
    print m.get_upload_link(uploaded)


upload_single(sys.argv[1])
