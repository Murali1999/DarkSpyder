#!/usr/bin/python3

import requests
import os
import sys
import random

import argparse
from bs4 import BeautifulSoup
import re
import subprocess

#ascii banner for the CLI tool
ret=os.system('figlet -f slant DarkSpyder')
print('\n \033[1m\033[3m' + '    Created by Nrchy' +  '\033[0m \n')

#system information and version check
if sys.version_info[0] < 3:
    print("Python3 is needed to run Spyder, Try \"python3 project.py\" instead\n")
    sys.exit(2)

#examples for reference
example = "\nEXAMPLES: \n"
example += "----------------------------------------------------------------->\n"
example += "python3 project.py -s hidden wiki   #Providing query for crawling\n"
example += "----------------------------------------------------------------->\n"

#function to run commands on shell
def cmdline(command):
	process = subprocess.Popen(
	args = command,
	shell = True,
	stdout = subprocess.PIPE
	)
	return process
	
#function to start tor service if it's not running
def checkservicetor():
    print("Checking if Tor is running..... \n")
    cmd = 'service tor status'
    out = cmdline(cmd).communicate()[0]
    if 'inactive' in str(out):
        print("Tor is not running currently....\n")
        print("Tor service is needed to run this script....\n")
        starttorservice()
    else:
        print("Tor service is running....\n")

#function to start tor if tor hasn't started
def starttorservice():
    print("Starting Tor...... \n")
    cmd = 'systemctl start tor'
    out = cmdline(cmd)
    print(str(out))

#function to display message for tool information
def msg(name=None):
    return '''
    -> darkspyder -s query
    [Automate the crawling process by providing the query to be searched.]
    
    -> darkspyder -id 
    [Option to find your IP address and user-agent.]
    '''

#set up the parser and description for the tool
parser = argparse.ArgumentParser(description='Dark Web Crawler', epilog=example, formatter_class=argparse.RawDescriptionHelpFormatter, usage=msg())

parse = parser.add_argument_group('Crawling Options')
parse.add_argument('-s', help='Query to crawl through the dark web')
parse.add_argument('-id', help='Find your IP address and user agent', action='store_true')

#setting up tor and its proxies
session = requests.session()
session.proxies = {
    'http' : 'socks5://127.0.0.1:9050',
    'https' : 'socks5://127.0.0.1:9050'
    }
#change user-agent randomly 
A = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
       	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
       	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        )
Agent = A[random.randrange(len(A))]
headers = {'user-agent': Agent}

args = parser.parse_args()

#check tor service is running or not before running the script
checkservicetor()

if (args.id):
    #check tor status and IP check
    print("Tor Status:")
    ret=os.system('service tor status')
    print()

    req = session.get('https://httpbin.org/ip', headers=headers)
    print(req.text)

    r = session.get('https://httpbin.org/user-agent', headers=headers)
    print(r.text)

query = args.s 
if (args.s):
    #run the query given by the user
    i=1
    query = query.replace(' ','+')
    page = session.get("https://ahmia.fi/search/?q={}".format(query), headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')
    soup1 = soup.find('ol', class_='searchResults')
    for li in soup1.find_all('li'):
	    print(str(i) + '. ' + li.cite.text)
	    #print(li.h4.a['href']) 
	    i+=1
