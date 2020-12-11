#!/usr/bin/python
import urllib2
import re
import sys
import chemistry
import socket
from urllib2 import Request
from sgmllib import SGMLParser

class URLLister(SGMLParser):
  def reset(self):
    SGMLParser.reset(self)
    self.urls = []

  def start_a(self, attrs):
    href = [v for k, v in attrs if k=='href']
    if href:
      self.urls.extend(href)


def getPage(url, ele, A):
    dir = './Data/Decays/'
    fname = dir + 'ensdf' + ele.capitalize() + str(A) + '.dat'
    f = open(fname,'w')
    req  = Request(url)
    page = ''
    try:
        page = urllib2.urlopen(req,timeout=3)
    except socket.timeout:
        print "ERROR: TIMEOUT"
        print url

    text = re.sub('<.*>','',page.read())
    text = text[re.search('[0-9]',text).start():]
    newtext = ""
    for line in text.split('\n'):
      if(len(line)>1):
        newtext += line + '\n'
    text = re.sub(r'^\t','',newtext,flags=re.MULTILINE)
    #print(text)
    f.write(text)
    return page.read()

def getURL(ele, A):
    Z = chemistry.getZ(ele)
    dau_A = A - 4
    dau_Z = Z-2
    dau_ele = chemistry.getElement(dau_Z)

    # nndc_url = 'https://www.nndc.bnl.gov/chart/decaysearchdirect.jsp?nuc='+str(A)+ele.upper()+'&unc=nds'
    nndc_url = 'https://www.nndc.bnl.gov/nudat2/decaysearchdirect.jsp?nuc='+str(A)+ele.upper()+'&unc=nds'
    nndc_page = urllib2.urlopen(nndc_url,timeout=3)
    parser = URLLister()
    parser.feed(nndc_page.read())
    parser.close()
    nndc_page.close()
    url_ends = []
    for a_url in parser.urls: 
        mod_url = re.sub(' ','%20',a_url)
        if re.search('getdecaydataset',mod_url) and re.search('a%20decay',mod_url):
            url_ends.append(mod_url)

    for url_end in url_ends:        
        #url = 'https://www.nndc.bnl.gov/chart/' + url_end
        url = 'https://www.nndc.bnl.gov/nudat2/' + url_end

        print 'Retrieving ENSDF data from:\t',url
        req = Request(url)
        page = ''
        try:
            page = urllib2.urlopen(req,timeout=3)
        except (socket.timeout, urllib2.URLError):
            print "ERROR: TIMEOUT"
            print url

        text = re.sub('<.*>','',page.read())

        # Check that this page is for an alpha decay
        is_adecay = re.search(" A DECAY",text)
        if not is_adecay:
            continue
        adecay_pos = text.find("A DECAY")
        if adecay_pos > 0 and adecay_pos < 30 :
            break

        # Prune the page and check that it might have interesting content
        if re.search('[0-9]',text) :
            text = text[re.search('[0-9]',text).start():]
        else :
            continue
        if len(text) < 30 :
            print 'WARNING: Could not find alpha for ele = {}, A = {}'.format(ele,A)
            break

        # Check that this page is for a ground state decay
        level = 0
        for line in text.split('\n'):
            if len(line) > 8 and line[6] == ' ' and line[7] == 'P':
                level = line.split()[2]
        if level == '0.0': 
            break

    return url

def main(argv):
    if(len(argv) != 3):
        print 'Usage: ./getENSDFdata.py [element] [A]'
        return

    ele = argv[1]
    A = int(argv[2])
    url = getURL(ele,A)
    getPage(url, ele, A)

if __name__ == "__main__":
    main(sys.argv)
