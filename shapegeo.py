from shapely.geometry.point import Point
from shapely.geometry import LineString
from random import uniform
from shapely.affinity import rotate
from shapely.affinity import scale
from shapely.geometry import Polygon


class ShapeGeo:
	'''
		This class has implemented the necessary functionalities required
		to draw shapes and manipulate them.
	'''


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

		return shape1.touches(shape2)


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