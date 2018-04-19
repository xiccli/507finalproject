import json
import sqlite3
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go
import pandas as pd
import secrets
import requests


# Welcome to part2! Both database storage and user interaction is considered here.
# Now I are going to do some mathematics and make some raw data more "easy" for people to understand
# Also I will generate plots and provide users with the option to view these species basic information

# In database generated, there will be 2 tables with one including raw data get from part1 and one including data for visualing/plots
# The 2 table can be linked to each other based on species name

# A series of plots can be generated during the interaction section, feel free to play with it!
# Also, this is not for absolute accuracy but only for user to understand a rough scope of information about wildlifes and their current situations
# Enjoy the trip!




########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########





# preparation
DBNAME = 'species.db'
SPECIESJS = 'species_detail.json'



# >>>>>>>>>>>>>>>>>> 1. DEAL WITH RAW DATA GOT FROM finalproj_part1.py <<<<<<<<<<<<<<<<<
# ---------------------------- 1.1 create species class -----------------------------
### this class is created for later use in interactive input / list species
class species():
    def __init__(self,name,status,population,scientificname,height,weight,length,habitats,place,generalhabitat):
        self.name = name
        self.status = status
        self.population = population
        self.scientificname = scientificname
        self.height = height
        self.weight = weight
        self.length = length
        self.habitats = habitats
        self.place=place
        self.generalhabitat=generalhabitat
    def __str__(self):
        return "{} ({}): {} animal, has a population of around {}. Its lives in habitats with {}, currently in {}".format(self.name, self.scientificname, self.status, self.population,self.generalhabitat,self.place)

# ---------------------------- 1.2 open cached file and export raw data as dict -----------------------------
with open(SPECIESJS) as f_species:
    species_ls=[]
    species_dr=json.load(f_species)
species_class_ls=[]

# ---------------------------- 1.3 have species into class object and save in a class list with 10 in a group -----------------------------
for each in species_dr:
    spc_class=species(each,species_dr[each]["Status"],species_dr[each]["Population"],species_dr[each]["Scientific Name"],species_dr[each]["Height"],species_dr[each]["Weight"],species_dr[each]["Length"],species_dr[each]["Habitats"],species_dr[each]["Place"],species_dr[each]["General Habitat"])
    species_class_ls.append(spc_class)
### as there are 100 wildlifes in WWF species list which will not be easily changed, I have the grouping method in this way. Though it may still need revision if in future days, things change
### but at that time it should be easily known :)
species_list_inten=[]
species_list_inten.append(species_class_ls[0:10])
species_list_inten.append(species_class_ls[10:20])
species_list_inten.append(species_class_ls[20:30])
species_list_inten.append(species_class_ls[30:40])
species_list_inten.append(species_class_ls[40:50])
species_list_inten.append(species_class_ls[50:60])
species_list_inten.append(species_class_ls[60:70])
species_list_inten.append(species_class_ls[70:80])
species_list_inten.append(species_class_ls[80:90])
species_list_inten.append(species_class_ls[90:])

# ---------------------------- 1.4 find the average population for each species if raw data is provided -----------------------------
### In raw data, expressions like "around 1,200 - 1,900 in the wild" makes it difficult to provide users with a straightforward idea about the Population
### Therefore, here I keep only the number (if there are more than one number, I will count the average) to make a rough comparison, not for accuracy
for each_species in species_dr:
    #### when "to" used instead of "-", change "to" to "-":
    if "to" in species_dr[each_species]["Population"]:
        new_popu_res=popu_info.replace("to","-")
        species_dr[each_species]["Population"]=new_popu_res
    #### when "+" is used inside, count the number only:
    elif "+" in species_dr[each_species]["Population"]:
        new_popu_res=popu_info.replace("+","")
        species_dr[each_species]["Population"]=new_popu_res
    #### when "hundred thousand" is used inside, use an avg of 500,000
    elif "hundred thousand" in species_dr[each_species]["Population"]:
        new_value_1=species_dr[each_species]["Population"].replace("hundred thousand","00,000")
        zero_ind=new_value_1.index("00,000")
        no_space_afternum= species_dr[each_species]["Population"][:zero_ind] + "" + species_dr[each_species]["Population"][zero_ind+1:]
        species_dr[each_species]["Population"]=no_space_afternum

        ls_convert=["one","two","three","four","five","six","seven","eight","nine","ten"]
        ls_convert_int=["1","2","3","4","5","6","7","8","9","10"]
        for every_num in ls_convert:
            if every_num in species_dr[each_species]["Population"]:
                ind_num=ls_convert.index(every_num)
                ##### get rid of the space after every_num first
                new=species_dr[each_species]["Population"].replace(every_num,ls_convert_int[ind_num])
                species_dr[each_species]["Population"]=new
            else:
                species_dr[each_species]["Population"]="500,000"
    elif "million" in species_dr[each_species]["Population"]:
        new_value_1=species_dr[each_species]["Population"].replace("million","000,000")
        zero_ind=new_value_1.index("000,000")
        no_space_afternum= species_dr[each_species]["Population"][:zero_ind] + "" + species_dr[each_species]["Population"][zero_ind+1:]
        species_dr[each_species]["Population"]=no_space_afternum

        ls_convert=["one","two","three","four","five","six","seven","eight","nine","ten"]
        ls_convert_int=["1","2","3","4","5","6","7","8","9","10"]
        for every_num in ls_convert:
            if every_num in species_dr[each_species]["Population"]:
                ind_num=ls_convert.index(every_num)
                ##### get rid of the space after every_num first
                new=species_dr[each_species]["Population"].replace(every_num,ls_convert_int[ind_num])
                species_dr[each_species]["Population"]=new
            else:
                species_dr[each_species]["Population"]="5,000,000"
    else:
        pass
    #### create a new key in each's dic called AvgPopulation
    popu_info=species_dr[each_species]["Population"]

    if " - " in popu_info:
        new_popu_info=popu_info.replace(" - ","-")
        popu_res=new_popu_info.split()
    elif " -" in popu_info:
        new_popu_info=popu_info.replace(" -","-")
        popu_res=new_popu_info.split()
    elif "- " in popu_info:
        new_popu_info=popu_info.replace("- ","-")
        popu_res=new_popu_info.split()
    elif " – " in popu_info:
        new_popu_info=popu_info.replace(" – ","-")
        popu_res=new_popu_info.split()
    elif "– " in popu_info:
        new_popu_info=popu_info.replace("– ","-")
        popu_res=new_popu_info.split()
    elif " –" in popu_info:
        new_popu_info=popu_info.replace(" –","-")
        popu_res=new_popu_info.split()
    else:
        popu_res=popu_info.split()


    num_ls_2=["0","1","2","3","4","5","6","7","8","9"]
    #### situation 01: if "-" inside:
    for every in popu_res:
        if "None" in species_dr[each_species]["Population"]:
            species_dr[each_species]["AvgPopulation"]="None"
        elif "extinct" in species_dr[each_species]["Population"]:
            species_dr[each_species]["AvgPopulation"]="None"
        elif "Unknown" in species_dr[each_species]["Population"]:
            species_dr[each_species]["AvgPopulation"]="None"
        else:
            pass

    for every in popu_res:
        for each in num_ls_2:
            if each in every:
                if "-" in every:
                    nums=[]
                    new_every=every.replace("-"," ")
                    all_nums=new_every.split()
                    new_nums=[]
                    for each in all_nums:
                        if "," in each:
                            new_each=each.replace(",","")
                            new_nums.append(new_each)
                        else:
                            new_nums.append(each)
                    sum=0
                    for every_popu in new_nums:
                        sum+=int(every_popu)
                    avg=sum/len(new_nums)
                    species_dr[each_species]["AvgPopulation"]=avg
                elif "–" in every:
                    nums=[]
                    new_every=every.replace("–"," ")
                    all_nums=new_every.split()
                    new_nums=[]
                    for each in all_nums:
                        if "," in each:
                            new_each=each.replace(",","")
                            new_nums.append(new_each)
                        else:
                            new_nums.append(each)
                    sum=0
                    for every_popu in new_nums:
                        sum+=int(every_popu)
                    avg=sum/len(new_nums)
                    species_dr[each_species]["AvgPopulation"]=avg
                else:
                    sum=0
                    num_ls=[]
                    if "," in every:
                        # ind=popu_res.index(item)
                        new_item=every.replace(",","")
                        num_ls.append(new_item)
                    else:
                        pass
                    for each in num_ls:
                        sum+=int(each)
                        avg=sum/len(num_ls)
                    species_dr[each_species]["AvgPopulation"]=avg
                break
            else:
                pass

# >>>>>>>>>>>>>>>>>> 1. END <<<<<<<<<<<<<<<<<







########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########







# >>>>>>>>>>>>>>>>>> 2. Generate Population Plot <<<<<<<<<<<<<<<<<

# ---------------------------- 2.1 classify species into different conservation status -----------------------------
### As there are too many species here (over 70 of them have population data), it is hard to display all in a single chart
### Thus, I decide to give users options to view the average populations based on species' conservation status
### For instance, if user input "Vulnerable" status, those wildlifes' average population with conservation status of "Vulnerable" will appear in a barchart, with x-axis representing their names, and y-axis representing the average population

conserv_status={}
for each in species_dr:
    if species_dr[each]["AvgPopulation"] != "None":
        if species_dr[each]["Status"] not in conserv_status:
            conserv_status[species_dr[each]["Status"]]={each:species_dr[each]["AvgPopulation"]}
        else:
            conserv_status[species_dr[each]["Status"]][each]=species_dr[each]["AvgPopulation"]

# ---------------------------- 2.2 define function to generate population plot based on the input conservation status -----------------------------

def plot_population(cns_status):
    species_nm=[]
    avg_popu=[]
    for each in conserv_status[cns_status]:
        species_nm.append(each)
        avg_popu.append(conserv_status[cns_status][each])
    data = [go.Bar(
            x=species_nm,
            y=avg_popu
    )]
    fname=cns_status+": Average Population"
    py.plot(data, filename=fname)
    return None

# >>>>>>>>>>>>>>>>>> 2. END <<<<<<<<<<<<<<<<<





########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########






# >>>>>>>>>>>>>>>>>> 3. Generate Location Map <<<<<<<<<<<<<<<<<
# ---------------------------- 3.1 have a json file to store site location information -----------------------------

CACHE_FNAME = "species_site.json"
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def make_request_with_cache(request_url):
    unique_indent = request_url
    ## if the current url exists in cache file, load it and return the request results so no 2nd request is needed
    if unique_indent in CACHE_DICTION:
        # print ("Get cached data ... ...")
        return CACHE_DICTION[unique_indent]
    ## if not, make a new request first, save the request results into cache file before use return to end the process and ouput the request text
    else:
        # print ("Make a new request ... ...")
        req_result=requests.get(unique_indent)
        CACHE_DICTION[unique_indent]=req_result.text
        cache_json = json.dumps(CACHE_DICTION)
        with open(CACHE_FNAME,"w") as fw:
            fw.write(cache_json)
            fw.close()
        return CACHE_DICTION[unique_indent]

def get_loc_of_site(site):
    site_name=site.replace(" ","+")
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    API_KEY=secrets.google_places_key
    full_url=base_url+site_name+"&key="+str(API_KEY)
    loc_info=make_request_with_cache(full_url)
    loc = json.loads(loc_info)['results']
    if loc:
        geometry=loc[0]['geometry']
        location=geometry['location']
        lat=float(location['lat'])
        lng=float(location['lng'])
        return [lat,lng]
    else:
        return "sorry! no location information is found :("

# ---------------------------- 3.2 get location information with the help of Google Map -----------------------------
### The geolocation (latitude and longitude) found here is based on a rough description inside the raw place data (refer to db to see "Place")
### Thus, you may find different species occured in a same latitude & longitude combination, which means they have similar habitatsself.
### wildlifes' habitat is larger than a single location point!

spe_nm_loc_ori={}
spe_nm_loc={}
for each in species_dr:
    each_latlng=get_loc_of_site(species_dr[each]["Place"])
    spe_nm_loc_ori[each]=each_latlng
# print (spe_nm_loc)
print (".....................................")
print ("Species without location information:")
count_noloc=1
for every in spe_nm_loc_ori:
    if spe_nm_loc_ori[every] != "sorry! no location information is found :(":
        lat_num=spe_nm_loc_ori[every][0]
        lon_num=spe_nm_loc_ori[every][1]
        loc_ls=(lat_num,lon_num)
        if loc_ls in spe_nm_loc:
            update=spe_nm_loc[loc_ls]+"; "+every
            spe_nm_loc[loc_ls]=update
        else:
            spe_nm_loc[loc_ls]=every
    else:
        output=str(count_noloc)+". "+str(every)
        print (output)
        count_noloc+=1
print (".....................................")
# ---------------------------- 3.3 define function to generate location map with plotly -----------------------------
def plot_speciesloc():
    lat_all=[]
    lon_all=[]
    name_all=[]

    for each in spe_nm_loc:
        lat_all.append(each[0])
        lon_all.append(each[1])
        name_all.append(spe_nm_loc[each])

    data = Data(
            [ Scattermapbox(
            lat = lat_all,
            lon = lon_all,
            text = name_all,
            mode = 'markers',
            marker = dict(
                size = 20,
                symbol="circle",
                color="rgb(27, 167, 132)"
            ))])
    #### find max range
    min_lat = 10000
    max_lat = -10000
    min_lon = 10000
    max_lon = -10000

    for each in lat_all:
        each_f = float(each)
        if each_f < min_lat:
            min_lat = each_f
        if each_f > max_lat:
            max_lat = each_f
    for each in lon_all:
        each_f = float(each)
        if each_f < min_lon:
            min_lon = each_f
        if each_f > max_lon:
            max_lon = each_f

    center_lat = (max_lat+min_lat) / 2
    center_lon = (max_lon+min_lon) / 2
    max_range = max(abs(max_lat - min_lat), abs(max_lon - min_lon))
    padding = max_range * .10
    lat_axis = [min_lat - padding, max_lat + padding]
    lon_axis = [min_lon - padding, max_lon + padding]

    layout = dict(
            geo = dict(
                scope='world',
                showland = True,
                landcolor = "rgb(229, 229, 229)",
                countrycolor = "rgb(255, 255, 255)" ,
                coastlinecolor = "rgb(255, 255, 255)",
                lataxis = {'range': lat_axis},
                lonaxis = {'range': lon_axis},
                center= {'lat': center_lat, 'lon': center_lon },
                countrywidth = 3,
                subunitwidth = 3
            ),
        )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='Multiple Mapbox')
    return None

# >>>>>>>>>>>>>>>>>> 3. END <<<<<<<<<<<<<<<<<






########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########






# >>>>>>>>>>>>>>>>>> 4. save all data into a db document <<<<<<<<<<<<<<<<<
try:
    # print ("connect to local sql file...")
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
except:
    print ("error")

# ---------------------------- 4.1  check database before create tables -----------------------------
check_spc='''
    DROP TABLE IF EXISTS 'Species';
'''
cur.execute(check_spc)

check_infovis='''
    DROP TABLE IF EXISTS 'InfoVis';
'''
cur.execute(check_infovis)

# ---------------------------- 4.2  create 2 tables, one with raw data from website and one with data for information visualizing part (include average population and location)  -----------------------------
create_table_spc='''
    CREATE TABLE Species(
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        'Name' TEXT,
        'Status' TEXT,
        'Population' TEXT,
        'ScientificName' TEXT,
        'Height' TEXT,
        'Weight' TEXT,
        'Length' TEXT,
        'Habitats' TEXT,
        'Place' TEXT,
        'GeneralHabitat' TEXT
    )
'''
cur.execute(create_table_spc)

create_table_infovis='''
    CREATE TABLE InfoVis(
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        'Name' TEXT,
        'AvgPopulation' TEXT,
        'LocLatitude' TEXT,
        'LocLongitude' TEXT
    )
'''
cur.execute(create_table_infovis)

# ---------------------------- 4.3  insert raw data into 1st table -----------------------------
insert_species='''
    INSERT INTO Species (Name,Status,Population,ScientificName,Height,Weight,Length,Habitats,Place,GeneralHabitat) VALUES (?,?,?,?,?,?,?,?,?,?);
'''
species_ls=[]
for each in species_dr:
    species_ls.append((each,species_dr[each]['Status'],species_dr[each]['Population'],species_dr[each]['Scientific Name'],species_dr[each]["Height"],species_dr[each]["Weight"],species_dr[each]["Length"],species_dr[each]["Habitats"],species_dr[each]["Place"],species_dr[each]["General Habitat"]))
for each in species_ls:
    cur.execute(insert_species,each)
conn.commit()

# ---------------------------- 4.4  insert visualizing information into 2nd table-----------------------------
insert_infovis='''
    INSERT INTO InfoVis (Name,AvgPopulation,LocLatitude,LocLongitude) VALUES (?,?,?,?);
'''
info_ls_all={}
for each in species_dr:
    info_ls_each={}
    info_ls_each["avgpopu"]=species_dr[each]["AvgPopulation"]
    for every in spe_nm_loc_ori:
        if every == each:
            if spe_nm_loc_ori[every] != "sorry! no location information is found :(":
                info_ls_each["loclat"]=spe_nm_loc_ori[every][0]
                info_ls_each["loclon"]=spe_nm_loc_ori[every][1]
            else:
                info_ls_each["loclat"]="N/A"
                info_ls_each["loclon"]="N/A"
    info_ls_all[each]=info_ls_each
for each_spe in info_ls_all:
    popu=str(info_ls_all[each_spe]["avgpopu"])
    lat=str(info_ls_all[each_spe]["loclat"])
    lon=str(info_ls_all[each_spe]["loclon"])
    spe_tp=(each_spe,popu,lat,lon)
    cur.execute(insert_infovis,spe_tp)
conn.commit()
conn.close()



# >>>>>>>>>>>>>>>>>> 4. END <<<<<<<<<<<<<<<<<





########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########
########## ........................ ヾ(･∀･*)♪ﾟ ............................ ##########





# >>>>>>>>>>>>>>>>>> 5. User Interaction <<<<<<<<<<<<<<<<<
if __name__ == "__main__":
    print ("ヾ(･∀･*)♪ﾟ Hello! What do you want to know about wildlife? (enter'help' to see all instructions)")
    userinput=input('Enter command (or "help" for options):')
    while userinput != "exit":
        if userinput == "help":
            serinput=input('''
                1. learn about a specific species
                    intro: you can learn about species' brief information, 10 as a group, there are 100 in total
                    valid input: to begin viewing information about species, please enter "list species", after that, enter a number from 1-10 to see 10 species introduction at a time.


                2. species_population
                    intro: generate a bar chart of all species' population based on the conservation status input
                    valid input: to begin viewing population, please enter "population", after seeing "population data is ready", input a conservation status (status name only) as listed below:
                                    - Vulnerable
                                    - Endangered
                                    - Near Threatened
                                    - Critically Endangered
                                    - Least Concern

                3. species_map
                    intro: generate a world map with all species with location information inside. not specific loc but a more genral one.
                    valid input: please enter "map" to view the result
                4. exit
                    exits the program
                5. help
                    lists available commands (these instructions)
            ''')
            userinput=input('Enter command (or "help" for options):')
        elif userinput == "population":
            print ("population data is ready.")
            userinput_2=input('Please enter conservation status:')
            print ("wait for a moment... plotly is working hard to generate plot ... ... ")
            plot_population(userinput_2)
            userinput=input('Enter command (or "help" for options):')
        elif userinput == "map":
            print ("wait for a moment... plotly is working hard to generate plot ... ... ")
            plot_speciesloc()
            userinput=input('Enter command (or "help" for options):')
        elif userinput == "list species":
            print ("species data is ready.")
            userinput_2=input('Please enter a number to view species list (10 species included)')
            results=species_list_inten[int(userinput_2)-1]
            count=1
            for each in results:
                print (str(count)+".")
                print (each.__str__())
                print ("-------------")
                count+=1
            userinput=input('Enter command (or "help" for options):')
        else:
            print (" (*ﾟДﾟ*) I don't understand what you said. Please refer to help document and try again")
            userinput=input('Enter command (or "help" for options):')
    print ("Have a good day! Bye! ヾ(･∀･*)♪ﾟ")
    quit()

# >>>>>>>>>>>>>>>>>> 5. END <<<<<<<<<<<<<<<<<
