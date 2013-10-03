from mega import Mega
from multiprocessing import Process
import dl_methods as m
import credentials as c

def main():
    details  = c.logmein()
    email    = details[0]
    password = details[1]
    links    = m.getlinks()
    print links
    print details
    pp=[]
    for url in links :
        pp.append(Process(target=m.download_single, args=(email,password,url)))
    for k in pp :
        k.start()
    for j in pp :
        k.join()

if __name__ == '__main__':
    main()
