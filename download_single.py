import dl_methods as m
import sys
import credentials as c

def main():
    details=c.logmein()
    email = details[0]
    password = details[1]

    m.download_single(email,password,sys.argv[1])

if __name__ == '__main__' :
    main()
