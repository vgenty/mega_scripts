import os,sys
from mega import Mega
import credentials as c

def upload(files,rars):
    print '\nUploading to MEGA'
    links=[]
    
    for k in xrange(len(rars)) :
        print '\n'
        print 'Uploading: ' + files[k] + ' in ' + rars[k]
        uploaded = m.upload(rars[k])
        print 'Uploaded, public link: '
        links.append(m.get_upload_link(uploaded))
        print links[k] 

    return links

def rarme(files,seed):
    print 'Rar-ing with seed string: ' + seed
    passw='soitgoes'
    count=0
    rars=[]
    
    for file_n in files :
        if not file_n.startswith('.') and not file_n.endswith('.rar'):
            os.system('rar a -r -hp%s %s.rar %s' %(passw,seed+str(count),file_n))
        rars.append(seed+str(count) + '.rar')
        count += 1

    return rars
    
def write_to_file(files,rars,links) :    
    fLinks = open('links.dat', 'w')
    fAll   = open('all.dat', 'w')
    
    for i in xrange(len(files)):
        fAll.write(files[i] + ' ' + rars[i] + ' ' + links[i] + '\n')
        fLinks.write(links[i] + '\n')

    fLinks.close()
    fAll.close()

def rename(files) :
    realfiles=[]
    realfiles2=[]
    temp=''
    temp2=''
    newname={}
    
    for x in files:
        for j in x:
            if j==' ':
                temp+='\ '
                temp2+='_'
            elif j=='(':
                temp+='\('
                temp2+='_'
            elif j==')':
                temp+='\)'
                temp2+='_'
            elif j=='[':
                temp+='\['
                temp2+='_'
            elif j==']':
                temp+='\]'
                temp2+='_'
            elif j=='{':
                temp+='\{'
                temp2+='_'
            elif j=='}':
                temp+='\}'
                temp2+='_'
            else:
                temp+=j
                temp2+=j
        realfiles.append(temp)
        realfiles2.append(temp2)
        newname[temp]=temp2
        temp=''
        temp2=''


    for x in realfiles :
        os.system('mv %s %s' % (x , newname[x]))
    
    return realfiles2 
    
def main():
    print 'Logging in'
    details=c.logmein()
    email = details[0]
    password = details[1]
    
    mega = Mega({'verbose': True})
    m = mega.login(email, password)    
    
    os.chdir("./multiple_upload")
    files = [x for x in os.listdir('.')]
    print 'Found: '
    files.sort()
    print files
    
    realfiles = rename(files)
    print realfiles
    seed = sys.argv[1]

    rars = rarme(realfiles,seed)

    links = upload(realfiles,rars)
    
    write_to_file(realfiles,rars,links)
    print 'Done'

if __name__ == '__main__':
    main()
