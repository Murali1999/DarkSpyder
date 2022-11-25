#!/usr/bin/python3

import requests
import os
import sys
import random
from requests.exceptions import ConnectionError

import argparse
from bs4 import BeautifulSoup
import re
import subprocess
import time

from termcolor import colored
from colored import fg, bg, attr
from progressbar import progressbar

#ascii banner for the CLI tool
ret=os.system('figlet -f slant DarkSpyder')
print('\n \033[1m\033[3m' + '           Created by Nrchy' +  '\033[0m \n')

#system information and version check
if sys.version_info[0] < 3:
    print("Python3 is needed to run Spyder, Try \"python3 project.py\" instead\n")
    sys.exit(2)

#examples for reference
example = "\nEXAMPLES: \n"
example += "--------------------------------------------------------------------------------------------------------->\n"
example += "$ python3 project.py -s 'hidden wiki'   #Providing query for crawling through the darknet search engine\n"
example += "$ python3 project.py -id        #Checking your current IP address and user-agent\n"
example += "$ python3 project.py -ip listoflinks.txt -num 20  #Finding IP address of specified number of .onion links\n"
example += "--------------------------------------------------------------------------------------------------------->\n"

#function to run commands on shell
def cmdline(command):
	process = subprocess.Popen(
	args = command,
	shell = True,
	stdout = subprocess.PIPE,
	stdin = subprocess.PIPE,
	stderr = subprocess.STDOUT,
	universal_newlines=True,
	)
	return process
	
#function to start tor service if it's not running
def checkservicetor():
    print(colored("%sChecking if Tor is running..... \n", "white") % (attr("bold"))) 
    time.sleep(5)
    cmd = 'service tor status'
    out = cmdline(cmd).communicate()[0]
    if 'inactive' in str(out):
        print(colored("%sTor is not running currently!! \n", "red") % (attr("bold")))
        print(colored("%sTor service is needed to run this script!! \n", "red") % (attr("bold")))
    else:
        print(colored("%sTor service is running. \n", "yellow") % (attr("bold")))

#function to check if file exists or not and create an incremental file if one already exists
def incrfilename(f):
    newfile = f
    name, ext = os.path.splitext(f)
    i = 0
    while os.path.exists(newfile):
        i += 1
        newfile = '{0}-{1}{2}'.format(name,i,ext)
    return newfile

#function to display message for tool information
def msg(name=None):
    return '''
    -> darkspyder -s query
    [Automate the crawling process by providing the query to be searched.]
    
    -> darkspyder -id 
    [Option to find your IP address and user-agent.]
    
    -> darkspyder -ip filename.txt -num 10
    [Option to find the IP address of given number of .onion links from a text file.]
    '''

#set up the parser and description for the tool
parser = argparse.ArgumentParser(description='Dark Web Crawler', epilog=example, formatter_class=argparse.RawDescriptionHelpFormatter, usage=msg())

parse = parser.add_argument_group('Crawling Options')
parse.add_argument('-s', help='Query to crawl through the dark web')
parse.add_argument('-id', help='Find your IP address and user agent', action='store_true')
parse.add_argument('-ip', help='Find the ip address of the .onion links from text file')
parse.add_argument('-num', help='Number of links to crawl from the list of .onion links', type=int, default=20)

#setting up tor and its proxies
session = requests.session()
session.proxies = {
    'http' : 'socks5h://127.0.0.1:9050',
    'https' : 'socks5h://127.0.0.1:9050'
    }
#change user-agent randomly 
A = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
       	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
       	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        )
Agent = A[random.randrange(len(A))]
headers = {'user-agent': Agent}

#get the arguments given by the user
args = parser.parse_args()

if (args.id):
    #check tor service is running or not before running the script
    checkservicetor()
    
    #check tor status and IP check
    print(colored("%sTor Status: ", "yellow") % (attr("bold")))
    ret=os.system('service tor status')
    print()

    try:
        req = session.get('https://httpbin.org/ip', headers=headers)
        print(req.text)
        
        r = session.get('https://httpbin.org/user-agent', headers=headers)
        print(r.text)

    except ConnectionError:
        print(colored("%sENABLE TOR SERVICE!! \n", "red") % (attr("bold")))
        sys.exit(141)

query = args.s 
if (args.s):
    #run the query given by the user
    
    try:
        #check tor service is running or not before running the script
        checkservicetor()
        
        #ahmia search engine
        #https://ahmia.fi/search/?q={}
        #a list of all links crawled by the search engine
        linklist=[]
        j=1
        query = query.replace(' ','+')
        page = session.get("https://ahmia.fi/search/?q={}".format(query), headers=headers)
        soup = BeautifulSoup(page.content,'html.parser')
        soup1 = soup.find('ol', class_='searchResults')
        print("Running Ahmia search engine... \n")
        for li in soup1.find_all('li'):
            linklist.append(li.cite.text)
        print(colored("%sCRAWLING COMPLETE. \n", "blue") % (attr("bold")))
        for i in progressbar(range(len(linklist)), redirect_stdout=True): 
            print(str(j) + '. ' + linklist[i]) 
            time.sleep(0.1)
        print("\nGot " + str(len(linklist)) + " links. \n") 
        #add .onion links to a file
        filename = incrfilename('listoflinks.txt') 
        fp = open(filename, 'w')
        for i in linklist:
            fp.write(i+'\n')  
        fp.close()
        print(colored("%sADDED .onion LINKS TO {}\n".format(filename), "yellow") % (attr("bold")))
    except ConnectionError:
        print(colored("%sENABLE TOR SERVICE!! \n", "red") % (attr("bold")))
        sys.exit(141)

if (args.ip):
    #variable for getting file name of .onion links
    files = args.ip
    #variable for only getting IP addresses of specified number of links
    nums = args.num
    #variable to check name and extension of file, and only allow valid types
    name, ext = os.path.splitext(files)
    #check if the file extension is .txt or not
    if ext in ['.txt']:
        if os.path.exists(files):
            print(colored("%sIP ADDRESS OF CRAWLED .onion LINKS:\n", "yellow") % (attr("bold")))
            with open(files, 'r') as l:
                links=l.readlines()[0:nums]
                k=1
                for i in links:
                    cmd = 'proxychains curl -s -I {}'.format(i)
                    out = cmdline(cmd).communicate()[0]
                    out = str(out)
                    if 'DNS-response' in out: 
                        splitword = '|DNS-response| ' 
                        content = out.splitlines()
                        line = content[3]
                        res = line.split(splitword, 1)
                        print(str(k)+'. '+res[1])
                        k+=1
        else:
            print(colored("%sNO SUCH FILE EXISTS!! \n", 'red') % (attr("bold")))
            print(colored("%sTRY AGAIN. \n", 'white') % (attr("bold")))
    else: 
        print(colored("%sNO OTHER FILE EXTENSION IS ALLOWED!! \n", 'red') % (attr("bold")))
        print(colored("%sTRY AGAIN. \n", 'white') % (attr("bold")))
