import requests
import re
import json

def getCats(source):
  if (source == "felineRescue"):
    req = requests.get('http://toolkit.rescuegroups.org/javascript/v2.0/?key=JOIAuoQb') #gets the page we're going to scrape
    p = re.compile(ur'\[\'(?P<ID>\d*)(?:\',\'.*?){3}(?P<Location>[^\-\_]*).*?\',\'(?P<Name>.*?)(?:\',\'.*?){2}\',\'(?P<Breed>.*?)(?:\',\'.*?){2}(?P<Gender>Male|Female)(?:\',\'.*?).*?>\',\'.*?img.*?(?P<ImgUrl>http.*?jpg).*?]', re.MULTILINE | re.DOTALL | re.IGNORECASE)#Regex Pattern for the scraping! 
  elif(source== "humane"):
    req = requests.get('https://www.animalhumanesociety.org/adoption?species=Cat&sex=All&date_filter_op=%3C&date_filter%5Bvalue%5D%5Byear%5D=2015&date_filter%5Bvalue%5D%5Bmonth%5D=9&date_filter%5Bvalue%5D%5Bday%5D=21&date_filter%5Bmin%5D%5Byear%5D=2015&date_filter%5Bmin%5D%5Bmonth%5D=9&date_filter%5Bmin%5D%5Bday%5D=21&date_filter%5Bmax%5D%5Byear%5D=&date_filter%5Bmax%5D%5Bmonth%5D=&date_filter%5Bmax%5D%5Bday%5D=&location=All&breed=&field_pp_declawed_value=No&field_pp_animalname_value=') #gets the page we're going to scrape
    p = re.compile(ur'/(?P<ID>\d{8})">(?P<Name>[a-zA-Z1-9\. ]*[^<]).{0,50}desc">.{0,50}(?P<Gender>M|F) \/ (?P<Breed>.{0,50})<br>(?P<Location>[a-zA-Z\. ]*[^<])', re.MULTILINE | re.DOTALL | re.IGNORECASE)#Regex Pattern for the scraping! 
  req = req.text #sets req to just the text from the response(the raw HTML)
  cats = [m.groupdict() for m in p.finditer(req)] # uses the regex to scrape the HTML and creates a list of dicts with the labels and values from the scraped HTML
    
  return cats


      
      
FRCats = getCats("felineRescue")
for cat in FRCats:
  cat["Link"] = 'https://toolkit.rescuegroups.org/javascript/v2.0/template1?animalID='+ cat['ID'] + u'&key=JOIAuoQb'
AHSCats = getCats("humane")
for cat in AHSCats:
    if (cat["Gender"] == "F"):
      cat["Gender"] = "Female"
    if (cat["Gender"] == "M"):
      cat["Gender"] = "Male"
    cat["ImgUrl"] = u'http://www.animalhumanesociety.org/sites/default/files/imagecache/animal_detail_thumb_161/adoption/images/large/'+cat['ID']+u'-1.jpg'
    cat["Link"] = u'http://www.animalhumanesociety.org/adoption/detail/' + cat['ID'] + u'/'
cats = FRCats + AHSCats
with open('cats.json', 'w') as outfile:
      json.dump(cats, outfile)