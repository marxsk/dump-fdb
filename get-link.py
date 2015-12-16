#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# find a correct URL from movie page
# run as ./script (file from fdb.cz/*/obsazeni)

from bs4 import BeautifulSoup
import sys
import logging

logging.getLogger().setLevel(logging.DEBUG)

fh = sys.stdin
source = fh.read()
soup = BeautifulSoup(source, "html.parser")

# check if we are on the right page, if not print correct URL to stderr and quit
for x in soup.findAll("a"):
  if unicode(x.get("href")).find("/obsazeni/") != -1:
    url = "http://www.fdb.cz/"
    sys.stdout.write(url + x.get("href") + "\n")
    sys.exit(0)

logging.error("URL not found")
sys.exit(1)
