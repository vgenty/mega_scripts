def sites():
    f=open('websites.dat','r')
    details=[]
    for line in f:
        line=line.rstrip()
        details.append(line)
    return details
