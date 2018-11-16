#!/usr/bin/env python

import rospy
import osmnx as ox

from road_info_osm_extract.msg import point 
from road_info_osm_extract.msg import points
from road_info_osm_extract.msg import pointsList

class map_extract:

	def __init__(self, node_name, place_name, publish_rate):
		
		#initialise class variables
		self._place_name = place_name
		self._ros_node_name = node_name
		self._road_info = pointsList()
		self._road_points = pointsList()
		self._publish_rate = publish_rate

		#create publisher to the topic "road_info"
		self._road_info_publisher = rospy.Publisher("road_info", pointsList, queue_size=100)
		self._road_points_publisher = rospy.Publisher("road_points", pointsList, queue_size=100)

		#create a node
		rospy.init_node(self._ros_node_name, anonymous=False)
		self._publish_rate = rospy.Rate(self._publish_rate) # 1hz

		#convert place in a map to a graph
		self._graph = ox.graph_from_place(self._place_name, network_type='drive')
		self._graph_proj = ox.project_graph(self._graph)

		#extract edges and nodes
		#edges define the geometry of the road
		#nodes define the start and end points of each road
		self._nodes, self._edges = ox.graph_to_gdfs(self._graph_proj, nodes=True, edges=True)

	def _publish_roads_data(self):

		self._parse_road_info()
		self._parse_road_points()

		while not rospy.is_shutdown():
		    
		    self._road_info_publisher.publish(self._road_info)
		    self._road_points_publisher.publish(self._road_points)
		    self._publish_rate.sleep()

	#parses the edges and nodes into readable lists
	def _parse_road_info(self):

		#loop through all roads or "edges"
		for i in range(0,len(self._edges)):

			pointXYstart = point()
			pointXYend = point()
			pointLatLonStart = point()
			pointLatLonEnd = point()
			pointLengthOneWay = point()

			pointXYstart.x = self._get_start_x(i)
			pointXYstart.y = self._get_start_y(i)

			pointXYend.x = self._get_end_x(i)
			pointXYend.y = self._get_end_y(i)

			pointLatLonStart.x = self._get_start_lat(i)
			pointLatLonStart.y = self._get_start_lon(i)

			pointLatLonEnd.x = self._get_end_lat(i)
			pointLatLonEnd.y = self._get_end_lon(i)

			pointLengthOneWay.x = self._get_edge_length(i)
			pointLengthOneWay.y = self._get_edge_direction(i)

			points_array = points()

			points_array.pt.insert(0, pointXYstart)
			points_array.pt.insert(1, pointXYend)
			points_array.pt.insert(2, pointLatLonStart)
			points_array.pt.insert(3, pointLatLonEnd)
			points_array.pt.insert(4, pointLengthOneWay)

			self._road_info.points_list.insert(i, points_array)

	def _parse_road_points(self):

		for i in range(0,len(self._edges)):

			x_points = self._edges[:].geometry[i].xy[0]
			y_points = self._edges[:].geometry[i].xy[1]

			points_xy = points()

			for xy in range(0,len(x_points)):

				point_xy = point()

				point_xy.x = x_points[xy]
				point_xy.y = y_points[xy]

				points_xy.pt.insert(xy, point_xy)

			self._road_points.points_list.insert(i, points_xy)

	#returns the x-coordinate of the start node
	def _get_start_x(self, edge_id):

		start_node_id = self._edges[:].u[edge_id]
		return self._nodes[:].x[start_node_id]

	#returns the y-coordinate of the start node
	def _get_start_y(self, edge_id):

		start_node_id = self._edges[:].u[edge_id]
		return self._nodes[:].y[start_node_id]

	#returns the x-coordinate of the end node
	def _get_end_x(self, edge_id):

		start_node_id = self._edges[:].v[edge_id]
		return self._nodes[:].x[start_node_id]

	#returns the y-coordinate of the end node
	def _get_end_y(self, edge_id):

		start_node_id = self._edges[:].v[edge_id]
		return self._nodes[:].y[start_node_id]

	#returns the latitude of the start node
	def _get_start_lat(self, edge_id):

		start_node_id = self._edges[:].u[edge_id]
		return self._nodes[:].lat[start_node_id]

	#returns the longitude of the start node
	def _get_start_lon(self, edge_id):

		start_node_id = self._edges[:].u[edge_id]
		return self._nodes[:].lon[start_node_id]

	#returns the latitude of the end node
	def _get_end_lat(self, edge_id):

		start_node_id = self._edges[:].v[edge_id]
		return self._nodes[:].lat[start_node_id]

	#returns the longitude of the end node
	def _get_end_lon(self, edge_id):

		start_node_id = self._edges[:].v[edge_id]
		return self._nodes[:].lon[start_node_id]

	#returns the length of the edge or road
	def _get_edge_length(self, edge_id):

		return self._edges[:].length[edge_id]

	#returns a boolean indicating whether a road is a one way or not
	def _get_edge_direction(self, edge_id):

		direction = self._edges[:].oneway[edge_id]
		direction = float(direction)
		return direction