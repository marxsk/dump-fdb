#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# run as ./script (file from fdb.cz/*/obsazeni)

from bs4 import BeautifulSoup
import sys

def print_xml(finfo):
  print "<movie>"
  print "\t<title>%s</title>" % (finfo["title"])
  print "\t<released>%s</released>" % (finfo["released_year"])
  print "\t<cast>"
  for x in finfo["cast"]:
    print "\t\t<cast-entry>"
    print "\t\t\t<person>%s</person>" % (" ".join(x["name"].split()))
    print "\t\t\t<role>%s</role>" % (x["role"])
    if x.has_key("character"):
      print "\t\t\t<character>%s</character>" % (" ".join(x["character"].split()))
    print "\t\t</cast-entry>"
  print "\t</cast>"
  print "</movie>"
  return finfo

info = {}

fh = sys.stdin
if len(sys.argv) > 1:
  fh = open(sys.argv[1],"r")
source = fh.read()
soup = BeautifulSoup(source)

infobasic = soup.find(id="zakladni_info")
info["title"]= infobasic.h1.string
info["cast"] = []

for x in soup.findAll("div", { "class" : "row" }):
  if "Rok:" in str(x):
    info["released_year"] = x.find("div", {"class" : "right_text"}).string


role = None
for x in soup.find("div", { "class" : "obsazeni" }).contents:
  if (hasattr(x, "name")) and (x.name == "div") and (x.has_attr("class")) and ("title" in x["class"]):
    role = x.string[:-1]

  if (hasattr(x, "name")) and (x.name == "table"):
    for tr in x.findAll("tr"):
      person = None
      character = None

      try:
        person = tr.find("td", {"class" : "nazev"}).find("a", {"class" : "text_vetsi_120"}).string
        character = tr.find("td", {"class" : "next"}).find("a").string
      except:
        # matching fails - ignore line then
        pass

      if person and role:
        if character == None:
          pinfo = {"name" : person, "role" : role}
        else:
          pinfo = {"name" : person, "role" : role, "character" : unicode(character)}

        info["cast"].append(pinfo)

print_xml(info)