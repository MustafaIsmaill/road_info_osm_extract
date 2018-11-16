##**Road Info Extraction:**

road_info_osm_extract is a **ROS** package written in **Python** that extracts road information from a specified area in open street maps.

##**How to use the package:**

1. go to [Nominatim Open Street Maps application] (https://nominatim.openstreetmap.org/) and search the area that you want to extract information from, the application should highlight to you the exact area that will be downloaded according to your **search string**.  
2. copy your search string and go to the file "gps_road_estimation/road_info_osm_extract/scripts/extract_road_info.py" and assign the "place_name" variable to your search string.  
3. in the file "gps_road_estimation/road_info_osm_extract/scripts/extract_road_info.py", rename the "node_name" and change the "publish_rate" variables to match your needs (optional).  
4. from the terminal run the following command `$ roslaunch road_info_osm_extract road_info_osm_extract.launch`  
5. subscribe to the "/road_info" topic to receive the road information
6. subscribe to the "/road_points" topic to receive the XY points of the map

##**Package Inputs:**

1. name of place or area in a map  
2. name of ros node  
3. rate of publishing the road information in Hertz  

##**Package Outputs:**

. The package publishes two messages of the type **"pointsList"**. **pointsList** is a list of roads on the map, where each road has a list of all the available points on the road.  
. The first message is published on the topic **"/road_info"** and contains info about the road in **"point"** format. The road info has 5 points that are arranged as follows:  

Point 1. xy-coordinates of the start of the road  
Point 2. xy coordinates of the end of the road  
Point 3. latitude and longitude of the start of the road  
Point 4. latitude and longitude of the end of the road  
Point 5. is a tuple that has the length of the road as its first element and a boolean value that indicated whether the road in one-way or not as its second element (1 = one-way / 0 = two-way).  
**Example:**  
`road_info = [[(xStart, yStart),(xEnd, yEnd),(latStart, lonStart),(latEnd, lonEnd),(length, oneway)],[],[],...]`  

. The second message is published on the topic **"/road_points"** and contains all the xy coordinates of the points of each road.  
**Example:**  
`road_points = [[(x1, y1),(x2, y2),(x3, y3)],[(x1, y1),(x2, y2)],[],[],...]`  

##
