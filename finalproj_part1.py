import requests
from bs4 import BeautifulSoup
import json


# The main function of this .py document is to crawl and scrap data from WWF website
# Ideally, you may need to wait for about 30s-  1min for all html information being scrapped into local file
# You only need to run this .py document once, and you can move to finalproj_part2.py for more functions
# Enjoy your trip to learn about wildlife! :)



########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########




# >>>>>>>>>>>>>>>>>> 1. Cral and .py <<<<<<<<<<<<<<<<<
# ------------------ 1.1 Preparation ------------------

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

CACHE_FNAME="wwf_species.json"
try:
    cache_file = open(CACHE_FNAME,"r")
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION={}

# ------------------ 1.2 Make Cache Storing All Species Brief Intro and Specific Url to Details Page ------------------
print ("\n ********* PART 1*********")
print ("WWF - Get Species' Info")

# ------------------ (1) "download" species information from species directory page ------------------

baseurl_1="https://www.worldwildlife.org"
basehtml_1=requests.get(baseurl_1).text
soup_1=BeautifulSoup(basehtml_1,"html.parser")
result_1=soup_1.find_all(class_="view-all")
baseurl_2=""
for each in result_1:
    if "View species" in each.text:
        baseurl_2=each["href"]

# ------------------ (2) go inside species page with full directory ------------------

basehtml_2=requests.get(baseurl_2).text
soup_2=BeautifulSoup(basehtml_2,"html.parser")
result_2=soup_2.find(class_="span4 ad card-species")
add_find=result_2.find("a")
add_url=add_find["href"]
allspecies_1=baseurl_1+add_url

# ------------------ (3) get common name, scientific name, and conservation status, as well as href for specific species ------------------

basehtml=requests.get(allspecies_1).text
soup_all=BeautifulSoup(basehtml,"html.parser")
species_intro=soup_all.find("tbody")
species=species_intro.find_all("tr")
for each in species:
    name_each=each.find("a").text
    url_each=each.find("a")["href"]
    sci_name=each.find("em").text
    td_ls=[]
    for every in each:
        if every.string != "\n":
            td_ls.append(every.string)
        else:
            pass
    conservation_status=td_ls[2]
    if name_each not in CACHE_DICTION:
        CACHE_DICTION[url_each]={"name":name_each,"scientific name":sci_name,"conservation status":conservation_status}

# ------------------ (4) check if one can go to next page ------------------
### if one can go to next page, find species information, if not, stop
next_one=soup_all.find("a",{"rel":"next"})

while next_one is not None:
    next_page=next_one["href"]
    next_url=baseurl_1+next_page
    next_html=requests.get(next_url).text
    soup_all=BeautifulSoup(next_html,"html.parser")
    species_intro=soup_all.find("tbody")
    species=species_intro.find_all("tr")
    for each in species:
        name_each=each.find("a").text
        url_each=each.find("a")["href"]
        sci_name=each.find("em").text
        td_ls=[]
        for every in each:
            if every.string != "\n":
                td_ls.append(every.string)
            else:
                pass
        conservation_status=td_ls[2]
        if name_each not in CACHE_DICTION:
            CACHE_DICTION[url_each]={"name":name_each,"scientific name":sci_name,"conservation status":conservation_status}
    next_one=soup_all.find("a",{"rel":"next"})

dumped_json_cache=json.dumps(CACHE_DICTION)
fw=open(CACHE_FNAME,"w")
fw.write(dumped_json_cache)
fw.close()

# >>>>>>>>>>>>>>>>>> 1. END <<<<<<<<<<<<<<<<<





########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########





# >>>>>>>>>>>>>>>>>> 2. Get Information from Each Details Page <<<<<<<<<<<<<<<<<

# ------------------ 2.1  define a function to find information include places, habitats, population,weight, length ------------------
def find_details(urladd):
    detailsurl=baseurl_1+urladd
    details_ls=[]
    details_html=requests.get(detailsurl).text
    soup_all=BeautifulSoup(details_html,"html.parser")
    #find introduction
    intro=soup_all.find("div",{"class":"lead gutter-bottom-6 medium-add-gutter wysiwyg"})
    more_details=soup_all.find("ul",{"class":"list-bordered list-bordered-items list-labeled"})
    print (detailsurl)
    if intro is not None:
        #find place and habitat
        try:
            place_habit_details=soup_all.find("ul",{"class":"list-data list-spaced"})
            place_habit=[] #in place-habit sequence
            li_ph=place_habit_details.find_all("li")
            for each in li_ph:
                detail=each.find(class_="lead").text
                if detail != "\n":
                    place_habit.append(detail)
            #=find height, weight and details of habitats
            more_details=soup_all.find("ul",{"class":"list-data list-stats list-items"})
            mht_wt={}
            li_more=more_details.find_all("li")
            for each in li_more:
                title=each.find("strong",{"class":"hdr"}).text
                content=each.find("div",{"class":"container"}).text
                mht_wt[title]=content
        except:
            place_habit=[]
            mht_wt={}
    elif more_details is not None:
        try:
            place_habit=["",""]
            mht_wt={}
            li_more=more_details.find_all("li")
            for each in li_more:
                title=each.find("strong",{"class":"label"}).text
                content=each.find("div",{"class":"container"}).text
                if title in ["POPULATION","HABITATS","HEIGHT","WEIGHT"]:
                    mht_wt[title]=content
        except:
            place_habit=[]
            mht_wt={}
    else:
        place_habit=[]
        mht_wt={}
    place_habit_new=[]
    mht_wt_new={}
    ### get rid of \n
    for each in mht_wt:
        each_clean=mht_wt[each].strip()
        mht_wt_new[each]=each_clean
    for each in place_habit:
        each_clean=each.strip()
        place_habit_new.append(each_clean)
    try:
        mht_wt_new["Place"]=place_habit_new[0]
    except:
        mht_wt_new["Place"]="None"
    try:
        mht_wt_new["General Habitat"]=place_habit_new[1]
    except:
        mht_wt_new["General Habitat"]="None"
    ### check all information inside the dict and make those empty values into "None"
        #### 01.check Status
    for every in ["Status","Population","Scientific Name","Height","Weight","Length","Habitats","Place","General Habitat"]:
        if every not in mht_wt_new:
            mht_wt_new[every]="None"
        else:
            pass
    ### check those rough numbers and get only numbers instead of "over 800 pounds"
    return mht_wt_new

# ------------------ 2.2  save details information into a local json file in a clear structure for future use ------------------
CACHE_FNAME2="species_detail.json"
try:
    cache_file2 = open(CACHE_FNAME2,"r")
    cache_contents2 = cache_file2.read()
    CACHE_DICTION2 = json.loads(cache_contents2)
    cache_file2.close()
except:
    CACHE_DICTION2={}

with open(CACHE_FNAME) as more_fw:
    species_dict=json.loads(more_fw.read())
for each in species_dict:
    if species_dict[each]["name"] not in species_dict:
        result = find_details(each)
        CACHE_DICTION2[species_dict[each]["name"]]=result
    else:
        pass

dumped_json_cache2=json.dumps(CACHE_DICTION2)
fw=open(CACHE_FNAME2,"w")
fw.write(dumped_json_cache2)
fw.close()

# >>>>>>>>>>>>>>>>>> 2. END <<<<<<<<<<<<<<<<<




########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########




# >>>>>>>>>>>>>>>>>> PLEASE OPEN "finalproj_part2.py" TO EXPLORE MORE <<<<<<<<<<<<<<<<<
