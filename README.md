# 507finalproject

***Project Goal*** </br>
This project aims at collecting 100 wildlife species data from WWF webiste.

Here, interactive command line prompt together with plotly are applied to help generate visualizing information about some of these data.

***How to use it?*** </br>

In this project, you will need to have a Google Map API Key to generate species' map. you can put it into **secrets.py** file </br>

You can also find all modules needed in **requirements.py**. </br>

There are 3 python documents in this project. </br>

**finalproj_part1.py** is used for crawling and scrapping wildlife species data from WWF website, which will only need to be used at the very beginning once. </br>

**finalproj_part2.py** is used for data processing and create interactive environment for users. You can play with it. </br>

**finalproj_test.py** is a testing document to check if data collecting, processing, and presenting work well. </br>

***What are the final outputs in interactive prompt?*** </br>
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
If everything goes smoothly, you will also find a database in file, which includes 2 tables and they will look like: </br>
![database1](https://raw.githubusercontent.com/xiccli/507finalproject/master/outputs_sample/database1.png)

![database2](https://raw.githubusercontent.com/xiccli/507finalproject/master/outputs_sample/database2.png)

If users input something wrong, they will see:
![wrongmsg](https://raw.githubusercontent.com/xiccli/507finalproject/master/outputs_sample/errormsg.png)


Thanks! :)
