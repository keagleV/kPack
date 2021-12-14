from math import pi


class Item:
	'''
		This class implements the Item class to represent the items
	'''

	def __init__ (self):

		
		# Type of the item
		self.itemType=str()

		# Parameters of the item
		self.itemParam=None

		# Weigth of the item. Specifically for the container, the weight
		# represents the capcity of it.
		self.itemWeight=int()

		# Value of the item
		self.itemValue=int()

		# The Area of the item
		self.area=int()


		# Item center point
		self.center = {
		'x': 0,
		'y': 0
		}


		# Item rotation angle
		self.rotAngle=0


	def set_item_type(self,itemType):

		'''
			This function sets the type of the item
		'''
		self.itemType=itemType

	def get_item_type(self):

		'''
			This function returns the type of the item
		'''
		return self.itemType

			
	def set_item_param(self,itemParam):

		'''
			This function sets the parameters of the item
		'''
		self.itemParam=itemParam


	def get_item_param(self):

		'''
			This function returns the parameters of the item
		'''
		return self.itemParam


	def set_item_weight(self,itemWeight):

		'''
			This function sets the weight of the item
		'''
		self.itemWeight=itemWeight


	def get_item_weight(self):

		'''
			This function returns the weigth of the item
		'''
		return self.itemWeight


	def set_item_value(self,itemValue):

		'''
			This function sets the itemValue of the item
		'''
		self.itemValue=itemValue


	def get_item_value(self):

		'''
			This function returns the value of the item
		'''
		return self.itemValue


	def set_item_area(self):

		'''
			This function sets the area of the object
		'''
		self.area=self.itemParam.get_area()


	def get_item_area(self):

		'''
			This function returns the area of the object
		'''

		return self.area


	def set_item_center_point(self,x,y):
		'''
			This function sets the center of the item
		'''
		self.center['x']=x
		self.center['y']=y


	def get_item_center_point(self):

		'''
			This function returns the center point's coordinates
		'''
		return (self.center['x'],self.center['y'])



	def set_item_rotation_angle(self,rotAngle):
		'''
			This function sets the rotation angle of the item
		'''
		self.rotAngle=rotAngle


	def get_item_rotation_angle(self):

		'''
			This function returns the rotation angle of the item
		'''
		return self.rotAngle







class CircleParams:

	'''
		This class implements the circles' parameters class
	'''
	def __init__(self):

		# Circle Radius
		self.radius=int()


	def set_radius(self,radius):
		'''
			This function sets the radius of the circle
		'''
		self.radius=radius

	def get_radius(self):

		'''
			This function returns the radius of the circle
		'''
		return self.radius

	def get_area(self):
		'''
			This function returns the area of the object based on its 
			parameters
		'''
		return self.radius * self.radius * pi


class SquareParams:

	'''
		This class implements the squares' parameters class
	'''
	def __init__(self):

		# Sqaure side
		self.side=int()


	def set_side(self,side):
		'''
			This function sets the side of the square
		'''
		self.side=side

	def get_side(self):

		'''
			This function returns the side of the square
		'''
		return self.side


	def get_area(self):
		'''
			This function returns the area of the object based on its 
			parameters
		'''
		return (self.side)**2



	
class RtiParams:

	'''
		This class implements the right trianlge isolesce' parameters class
	'''
	def __init__(self):

		# rti side
		self.side=int()


	def set_side(self,side):
		'''
			This function sets the side of the rti
		'''
		self.side=side

	def get_side(self):

		'''
			This function returns the side of the rti
		'''
		return self.side


	def get_area(self):
		'''
			This function returns the area of the object based on its 
			parameters
		'''
		return ((self.side)**2)/2



