#!/usr/bin/python
import urllib2
import re
import sys
import chemistry
import socket
from urllib2 import Request

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
    f.write(text)
    return page.read()

def getURL(ele, A):
    Z = chemistry.getZ(ele)
#208082005'
#    url = 'http://www.nndc.bnl.gov/nudat2/getdecaydataset.jsp?nucleus='
    dau_A = A - 4
    dau_Z = Z-2
    dau_ele = chemistry.getElement(dau_Z)
    dataset = 0
    while True :
        if dataset == 0:
            url = 'http://www.nndc.bnl.gov/chart/getdecaydataset.jsp?nucleus='+str(dau_A)+dau_ele.upper()+'&dsid='+str(A)+ele.lower()+'%20a%20decay%20(3.098%20m)'
        else:
            url = 'http://www.nndc.bnl.gov/ensdf/EnsdfDispatcherServlet?dbclass=ensdf&dataset_table=dataset_table&pagesource=singular&chooseit=View%20in%20ENSDF%20format&datasetcheck={0:03d}{1:03d}{2:03d}'.format(dau_A,dau_Z,dataset)

        dataset = dataset+1        
        print url
        req = Request(url)
        page = ''
        try:
            page = urllib2.urlopen(req,timeout=3)
        except (socket.timeout, urllib2.URLError):
            print "ERROR: TIMEOUT"
            print url

        if page == '':
            return 'http://www.nndc.bnl.gov/ensdf/EnsdfDispatcherServlet?dbclass=ensdf&dataset_table=dataset_table&pagesource=singular&chooseit=View%20in%20ENSDF%20format&datasetcheck=231092001'
                
        text = re.sub('<.*>','',page.read())
        is_adecay = re.search(" A DECAY",text)
        if not is_adecay:
            continue
        if re.search('[0-9]',text) :
            text = text[re.search('[0-9]',text).start():]
        else :
            continue
        if len(text) < 30 :
            print 'WARNING: Could not find alpha for ele = {}, A = {}'.format(ele,A)
            break
        adecay_pos = text.find("A DECAY")
#        if text[15] == 'A':
        if adecay_pos > 0 and adecay_pos < 30 :
            break

#    url += str(dau_A)
#    url += dau_ele.upper()
#    url += '&dsid='
#    url += str(A)
#    url += ele.lower()
#    url += '%20a%20decay'
    return url

#getPage('http://www.nndc.bnl.gov/nudat2/getdecaydataset.jsp?nucleus=237NP&dsid=241am%20a%20decay')

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
