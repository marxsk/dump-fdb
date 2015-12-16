#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# run as ./script (file from fdb.cz/*/obsazeni)

from bs4 import BeautifulSoup
import sys
import logging

def print_xml(finfo):
  print "<movie>"
  print "\t<title>%s</title>" % (finfo["title"])
  if "original_title" in finfo:
    print "\t<title_original>%s</title_original>" % (finfo["original_title"])
  if "other_titles" in finfo:
    print "\t<other_titles>%s</other_titles>" % (finfo["other_titles"])
  if "released" in finfo:
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

def print_xml_serie(finfo):
  print "<serie>"
  print "\t<title>%s</title>" % (finfo["title"])
  print "\t<episode_title>%s</episode_title>" % (finfo["episode_title"])
  if "original_title" in finfo:
    print "\t<episode_title_original>%s</episode_title_original>" % (finfo["original_title"])
  if "episode_info" in finfo:
    print "\t<episode_info>%s</episode_info>" % (finfo["episode_info"])
  if "released_year" in finfo:
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
  print "</serie>"
  return finfo

logging.getLogger().setLevel(logging.INFO)
info = {}

fh = sys.stdin
if len(sys.argv) > 1:
  fh = open(sys.argv[1],"r")
  logging.info(sys.argv[1])
source = fh.read()
soup = BeautifulSoup(source, "html.parser")

infobasic = soup.find(id="zakladni_info")
info["title"]= infobasic.h1.string
info["cast"] = []
logging.debug("Title: %s" % (info["title"]))

x = soup.find("h2", { "class"  : "title_next"})
if x:
	info["original_title"] = x.string

for x in soup.findAll("div", { "class" : "left_text" }):
	if "Další název:" in str(x):
		# @todo: this should be split but there are several separators in DB
		info["other_titles"] = x.next_sibling.string.strip()

for x in soup.findAll("div", { "class" : "row" }):
  if "Rok:" in str(x):
    info["released_year"] = x.find("div", {"class" : "right_text"}).string

x = soup.find("h2", { "class" : "dil" })
if x:
  try:
    info["episode_title"] = x.contents[0].string.strip()
  except:
    pass

  try:
    info["episode_info"] = x.contents[1].string.strip()
  except:
    pass

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

if "episode_title" in info:
  print_xml_serie(info)
else:
  print_xml(info)
