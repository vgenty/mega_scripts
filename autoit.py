import mechanize
import cookielib
import urllib
import pyimgur
import os,sys
from mega import Mega
from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import credentials as c
import websites    as w

def bibliotik(uurl,site,uusername,ppassword) :
    bibdata = []

    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    r= br.open(uurl)
    br.select_form(nr=0)

    br.form['username'] = uusername
    br.form['password'] = ppassword
    
    br.submit()
    
    torrent = site
    
    r=br.open(torrent)
    html = r.read()

    soup = BeautifulSoup(html)
    
    image = soup.findAll('a',attrs={'rel':'lightbox'})
    image = image[0].attrs[1][1]
    
    CLIENT_ID="3d6e50fe4468788"
    CLIENT_SECRET="543bc4299181740033fd65ee28da4d1d0e9493ae"

    im = pyimgur.Imgur(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    bibimg=im.upload_image(url=image)
    
    bibdata.append(bibimg.link)
    
    title = soup.findAll('h1', attrs={'id' : 'title'})
    bibtitle=title[0].getText()
    bibdata.append(bibtitle)
    
    description = soup.findAll('div',attrs={'id' : 'description'})
    bibdescription=description[0].getText()[11:]
    bibdata.append(bibdescription)
   
    author = soup.findAll('p',attrs={'id' : 'creatorlist'})
    bibauthor=author[0].getText()[2:]
    bibdata.append(bibauthor)

    published = soup.findAll('p',attrs={'id' : 'published'})
    cnt=0
    for x in published[0].getText() : cnt += 1
    bibpublished = published[0].getText()[0:12] + " " + published[0].getText()[12:cnt-7] + " " + published[0].getText()[cnt-7:]
    cnt = 0
    bibdata.append(bibpublished)

    details = soup.findAll('p',attrs={'id' : 'details_content_info'})
    bibdetails = details[0].getText()
    bibdata.append(bibdetails)

    tags = soup.findAll('p',attrs={'id' : 'details_tags'})
    bibtags = tags[0].getText()[5:]
    bibtags=bibtags.split(',')
    bibdata.append(bibtags)
    
    return bibdata
    
def SIG(bibdata,link,username,password,add) :
    sigdata=[]
    sigdata.append(bibdata[1])
    authorss=bibdata[3].split(',')
    authorsss=", ".join(authorss)
    sigdata.append('<b>Author</b>:\n' + authorsss + "\n\n<b>Description</b>:\n" + bibdata[4] + "\n" + bibdata[5] + "\n\n" + bibdata[2])
    sigdata.append(bibdata[0])
    sigdata.append(link)
    sigdata.append('soitgoes')

    driver = webdriver.Chrome()
    driver.get(add)
    driver.find_element_by_name("user").send_keys(username)
    driver.find_element_by_name("pass").send_keys(password)
    driver.find_element_by_xpath("//*[@type='submit']").click()

    driver.find_element_by_xpath("//*[@id='title']/input").send_keys(sigdata[0])
    driver.find_element_by_xpath("//*[@id='category']/span[2]/input").click()
    driver.find_element_by_xpath("//*[@id='2']/input[4]").click()
    driver.find_element_by_xpath("//*[@id='rightdiv']/span[2]/span[7]/input").click()
    driver.find_element_by_xpath("//*[@id='rightdiv']/span[2]/span[8]/input").click()
    driver.find_element_by_xpath("//*[@id='rightdiv']/span[2]/span[9]/input").click()
    driver.find_element_by_xpath("//*[@id='summary']/textarea").send_keys(sigdata[1])
    driver.find_element_by_xpath("//*[@id='links_imgref']/textarea").send_keys(sigdata[2])
    driver.find_element_by_xpath("//*[@id='links_mega']/textarea").send_keys(sigdata[3])
    driver.find_element_by_xpath("//*[@id='password']/input").send_keys(sigdata[4])
    driver.find_element_by_xpath("//*[@id='subcontent']").click()

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
    print 'Getting websites'
    web=w.sites()
    print 'Logging in to MEGA'
    details=c.logmein()
    email = details[0]
    password = details[1]
    mega = Mega({'verbose': True})
    m = mega.login(email, password)    
    ##################################
    print 'Getting file list'
    os.chdir("./multiple_upload")
    files = [x for x in os.listdir('.')]
    print 'Found: '
    files.sort()
    print files    
    realfiles = rename(files)
    print realfiles
    seed = sys.argv[2]
    print 'RARing'
    rars = rarme(realfiles,seed)
    print 'Uploading to MEGA'
    links = upload(realfiles,rars)
    write_to_file(realfiles,rars,links)
    print 'MEGA upload complete'
    #################################
    print 'Scraping Bibliotik'
    site=sys.argv[1]
    bibdata=bibliotik(w[0],site,details[4],details[5])
    ################################
    print 'Filling SIG'
    SIG(bibdata,links[0],details[2],details[3],web[1])


if __name__ == '__main__':
    main()
