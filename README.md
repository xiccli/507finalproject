# 507finalproject


Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.
Brief user guide, including how to run the program and how to choose presentation options.




***Project Goal*** </br>
This project aims at collecting 100 wildlife species data from WWF webiste.</br>

Here, interactive command line prompt together with plotly are applied to help generate visualizing information about some of these data.</br>




***NOTE: please run part1.py before you use test.py***</br>




***1. Data Source Used****</br>
The data source I use now are information in website pages of WWF. Specific url of each species detailed information can be found in species catalog inside the WWF website. (basic url:https://www.worldwildlife.org/).</br>


***2. Tools/Additional Information Needed to Run the Program Successfully****</br>
No API key or client secret is needed to get initial raw data. But when dealing with data, you will need a **Google Map API** to get geolocation information. A secrets.py file is provided to store Google Map API (check secrets.py).</br>

Some modules including Plotly.py will be used to generate visualizing result, please check "requirements.txt" or part1.py/part2.py to see if you have those modules installed.</br>


***3. How it works?****</br>
There are 3 python documents in this project. </br>

**finalproj_part1.py** is used for crawling and scrapping wildlife species data from WWF website, which will only need to be used at the very beginning once.</br>

**finalproj_part2.py** is used for data processing and create interactive environment for users. You can play with it. </br>

*When you run finalproj_part1.py or finalproj_part2.py for the 1st time, it may take some time. maybe you can get some coffee from coffee machine :)*

**finalproj_test.py** is a testing document to check if data collecting, processing, and presenting work well. </br>

Main functions used here including: "plot_speciesloc" and "plot_population" which are used in generating plots. A class is also defined called "species".</br>

***4. How to use it?****</br>
You need to run **finalproj_part1.py** first to get raw data from website. After that, you can choose either to play with finalproj_part2.py or run finalproj_test.py directly to see if everything works well and learn about wildlife :)</br>

***5. What are the final outputs?*** </br>
If you choose *list species* </br>
you may get a result in terminal looks like: </br>
![listofspecies](https://raw.githubusercontent.com/xiccli/507finalproject/master/outputs_sample/listspecies.png)
</br>
</br>

If you choose *map* </br>
you will need to wait for a moment and a map will be generated in browser: </br>
![speciesmap](https://raw.githubusercontent.com/xiccli/507finalproject/master/outputs_sample/map.png)
</br>
</br>
If you choose *population* </br>
similar to map, but this time you will see a bar chart: </br>
![barchartofpopulation](https://raw.githubusercontent.com/xiccli/507finalproject/master/outputs_sample/population.png)

</br>
</br>
If everything goes smoothly, you will also find a database in file, which includes 2 tables and they will look like:</br>
![database](https://github.com/xiccli/507finalproject/blob/master/outputs_sample/database1.png?raw=true)

If users input something wrong, they will see:
![wrongmsg](https://raw.githubusercontent.com/xiccli/507finalproject/master/outputs_sample/errormsg.png)


Thanks! :)
