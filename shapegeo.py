from shapely.geometry.point import Point
from shapely.geometry import LineString
from shapely.affinity import rotate
from shapely.affinity import scale
from shapely.geometry import Polygon
from shapely.ops import split
from random import uniform
from random import choice
from math import tan



# class ShapeParameters:
# 	'''
# 		This class has implemented the shape's parameters in the case of this project
# 	'''
# 	def __init__(self,centerX,centerY,radius,side):
# 		self.centerY=centerY
# 		self.centerX=centerX
# 		self.radius=radius
# 		self.side=side





class ShapeGeo:
	'''
		This class has implemented the necessary functionalities required
		to draw shapes and manipulate them.
	'''



	# def create_object(self,objectType, objectParameters):
	# 	'''
	# 		This function will create an object based on the given parameters
	# 		and returns the objects.
	# 	'''

	# 	if objectType == 'circle':
	# 		pass

	# 	elif objectType == 'square':
	# 		pass

	# 	elif objectType == 'rti':
	# 		pass

	# 	elif objectType == 'ellipse':
	# 		pass




	def create_circle(self,centerX=0,centerY=0,radius=1):

		'''
			This function creates a circle and returns the its object.
			
			By default, if no argument is specified, point (0,0) and radius 1
			will be used.
		'''

		centerPoint = Point(centerX, centerY)
		
		circle = centerPoint.buffer(radius)

		return circle



	def create_square(self,centerX=0,centerY=0,side=1,rotation=0):
		'''
			This function creates a square and returns the its object.
			
			By default, if no argument is specified, point (0,0), side 1, and rotation 0
			will be used.
		'''

		square=Polygon([ (centerX-side/2,centerY+side/2),
						 (centerX-side/2,centerY-side/2),
						 (centerX+side/2,centerY-side/2),
						 (centerX+side/2,centerY+side/2) ])

		# Applying the rotation 
		rotatedSquare = rotate(square, rotation, (centerX,centerY))


		return rotatedSquare


	def create_rti(self,centerX=0,centerY=0,side=1,rotation=0):
		'''
			This function creates a right triangle isosceles and returns the its object.
			
			By default, if no argument is specified, point (0,0), side 1, and rotation 0
			will be used.

			** The center is the point that has 90 degree angle
		'''
		rti=Polygon([ (centerX,centerY),
						 (centerX,centerY+side),
						 (centerX+side,centerY)] )


		# Applying the rotation 
		rotatedRti= rotate(rti, rotation, (centerX,centerY))


		return rotatedRti


	def create_ellipse(self,centerX=0,centerY=0,semiAxisX=10,semiAxisY=12,rotation=0):
		'''
			This function creates a ellipse and returns the its object.
			
			By default, if no argument is specified, point (0,0), semi-axis values (10,12), and rotation 0
			will be used.


			SOURCE: https://gis.stackexchange.com/questions/243459/drawing-ellipse-with-shapely
		'''

		#TODO check correctness

		ellipse = ((centerX, centerY),(semiAxisX,semiAxisY),rotation)

		# Let create a circle of radius 1 around center point:
		circ = Point(ellipse[0]).buffer(1)

		# Let create the ellipse along x and y:
		ell  = scale(circ, int(ellipse[1][0]), int(ellipse[1][1]))

		# Let rotate the ellipse (clockwise, x axis pointing right):
		ellr = rotate(ell,ellipse[2])

		# If one need to rotate it clockwise along an upward pointing x axis:
		elrv = rotate(ell,90-ellipse[2])
		# According to the man, a positive value means a ant

		return elrv


	def check_shape_overlap(self,shape1 , shape2):

		'''
			This function checks whether two shapes overlap or not.
		'''
		return shape1.intersects(shape2)

	

	def check_shape_inside_other(self,shape1, shape2):
		'''
			This function checks whether shape2 is inside the shape1
		'''
	
		return shape1.contains(shape2)


	def get_random_point_from_shape(self,shape):

		'''
			This function will randomly select a point inside a shape
			and returns it
		'''
		min_x, min_y, max_x, max_y = shape.bounds

		x = uniform(min_x, max_x)
		x_line = LineString([(x, min_y), (x, max_y)])
		x_line_intercept_min, x_line_intercept_max = x_line.intersection(shape).xy[1].tolist()
		y =  uniform(x_line_intercept_min, x_line_intercept_max)


		return (x,y)



	def split_shape_with_crossing_line(self,shape):
		'''
			This function splits the given shape by a random crossing line, and
			returns the segments created by the crossing line
		'''


		# First get one random point inside the shape

		p1 = self.get_random_point_from_shape(shape)


		# TODO
		# Then we have to choose a random slope for the line. We omit the lines with 
		# slop infinity which are caused by the degrees of 90 and 270.
		lineSlope= 	 tan ( choice([i for i in range(0,360) if i not in [ 90 , 270 ] ]) )



		# Then we have to extend the line crossing the p1 with the calculated slope
		#, such that, it intersects	the shape. For that, we will used extra points 
		# which have the x coordinates of x_max+1 and x_min-1. We will use the line 
		# equation to calculate the corresponding y values.

		min_x, min_y, max_x, max_y = shape.bounds


		# Line equation to drive two more secure points to draw the crossing line.
		yMaxOnLine = lineSlope * (  (max_x+1) - p1[0]  ) + p1[1]

		yMinOnLine = lineSlope * (  (min_x-1) - p1[0]  ) + p1[1]


		# Now two points are ready to create the crossing line
		crossLinePoints= [(max_x+1 , yMaxOnLine ), (min_x-1,yMinOnLine)]


		# Defining the cross line
		crossLine =  LineString ( crossLinePoints )


		# List of shapes resulting from the segmentation
		shapes = list(split(shape,crossLine).geoms)


		return shapes,crossLine


