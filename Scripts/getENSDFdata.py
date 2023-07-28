import urllib.request, urllib.error, urllib.parse
import re
import sys
import chemistry
import socket
from urllib.request import Request
from bs4 import BeautifulSoup

class URLLister:
    def __init__(self):
        self.urls = []

    def feed(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')
            if href:
                self.urls.append(href)

    def start_a(self, attrs):
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.urls.extend(href)

    def getPage(self, url, ele, A):
        dir = './Data/Decays/'
        fname = dir + 'ensdf' + ele.capitalize() + str(A) + '.dat'
        f = open(fname, 'w')
        req = Request(url)
        page = ''
        try:
            page = urllib.request.urlopen(req, timeout=3)
        except socket.timeout:
            print("ERROR: TIMEOUT")
            print(url)

        text = re.sub('<.*>', '', page.read().decode())
        text = text[re.search('[0-9]', text).start():]
        newtext = ""
        for line in text.split('\n'):
            if len(line) > 1:
                newtext += line + '\n'
        text = re.sub(r'^\t', '', newtext, flags=re.MULTILINE)
        # print(text)
        f.write(text)
        f.close()
        return page.read()

    def getURL(self, ele, A):
        Z = chemistry.getZ(ele)
        dau_A = A - 4
        dau_Z = Z - 2
        dau_ele = chemistry.getElement(dau_Z)

        nndc_url = 'https://www.nndc.bnl.gov/nudat2/decaysearchdirect.jsp?nuc=' + str(A) + ele.upper() + '&unc=nds'
        nndc_page = urllib.request.urlopen(nndc_url, timeout=3)
        soup = BeautifulSoup(nndc_page, 'html.parser')
        url_ends = []

        for a_tag in soup.find_all('a', href=True):
            mod_url = re.sub(' ', '%20', a_tag['href'])
            if re.search('getdecaydataset', mod_url) and re.search('a%20decay', mod_url):
                url_ends.append(mod_url)

        for url_end in url_ends:        
            # url = 'https://www.nndc.bnl.gov/chart/' + url_end
            url = 'https://www.nndc.bnl.gov/nudat2/' + url_end

            print('Retrieving ENSDF data from:\t', url)
            req = Request(url)
            page = ''
            try:
                page = urllib.request.urlopen(req, timeout=3)
            except (socket.timeout, urllib.error.URLError):
                print("ERROR: TIMEOUT")
                print(url)

            text = re.sub('<.*>', '', page.read().decode())

            # Check that this page is for an alpha decay
            is_adecay = re.search(" A DECAY", text)
            if not is_adecay:
                continue
            adecay_pos = text.find("A DECAY")
            if adecay_pos > 0 and adecay_pos < 30:
                break

            # Prune the page and check that it might have interesting content
            if re.search('[0-9]', text):
                text = text[re.search('[0-9]', text).start():]
            else:
                continue
            if len(text) < 30:
                print('WARNING: Could not find alpha for ele = {}, A = {}'.format(ele, A))
                break

            # Check that this page is for a ground state decay
            level = 0
            for line in text.split('\n'):
                if len(line) > 8 and line[6] == ' ' and line[7] == 'P':
                    level = line.split()[2]
            if level == '0.0': 
                break

        return url

    def main(self, argv):
        if len(argv) != 3:
            print('Usage: ./getENSDFdata.py [element] [A]')
            return

        ele = argv[1]
        A = int(argv[2])
        url = self.getURL(ele, A)
        self.getPage(url, ele, A)

if __name__ == "__main__":
    url_lister = URLLister()  # Create an instance of the URLLister class
    url_lister.main(sys.argv)  # Call the main method using the instance