from logger import *
from random import choice
from random import randint

class EvolAlgoParams:

	'''
		This class implements the parameters of the evolution algorithm.
	'''

	def __init__(self):

		# Population size
		self.populationSize=100

		# Number of tries to select an object
		self.objectSelectionTries=40

		# Number of tries to set up the initial population
		self.initPopSetupTries=10

		



class KpackEA:
	'''
		This class implements all the necessary function for the EA in the packing
		problem.
	'''
	def __init__(self,logger,eaParams,shapeGeo):

		# Logger handler
		self.logger=logger

		# EA parameters
		self.eaParams=eaParams

		# shapeGeo handler
		self.shapeGeo=shapeGeo

	def initial_filtering(self,objects):
		'''
			This function filters out some of the objects that cannot be
			placed in the container in any condition. Such conditions are

			1- the weight of the object exceeds the container's weight
			2- the area of the object exceeds the container's area
		'''


		totalNumObjects = len(objects.keys())-1 # -1 is to exclude the container

		containerWeight= objects[0].get_item_weight()

		containerArea= objects[0].get_item_area()

		# Number of deleted objects after the filtering
		numOfDeletedObjects=0

		for k,v in list(objects.items()):
			
			# Skip the container
			if k==0:
				continue

			# Check for the weight
			if (v.get_item_weight() > containerWeight) or (v.get_item_area() > containerArea):
				
				objects.pop(k)

				numOfDeletedObjects+=1


		# TODO
		# Updating the key values to adjust starting from 1
		startingKey=1
		for k,v in list(objects.items()):
			
			# Skip the container
			if k==0:
				continue

			objects.pop(k)
			objects[startingKey]=v
			startingKey+=1





		self.logger.log_message("{0}/{1} Objects Were Deleted During Filtering Process".format(numOfDeletedObjects,totalNumObjects),"INF")

			
		# Return the new dictionary of the objects
		return objects


	def generate_initial_population(self,objects):
		'''
			This function generates the initial population for the
			EA algorithm
		'''

		containerObjParams=objects[0]

		# Container center point coordinates
		containerCpX,containerCpY=containerObjParams.get_item_center_point()

		# Creating the object of the container based on its parameters
		containerObj=None

		if containerObjParams.get_item_type()=='circle':
			containerObj=self.shapeGeo.create_circle(centerX=containerCpX,centerY=containerCpY,radius=containerObjParams.get_item_param().get_radius())

		elif containerObjParams.get_item_type()=='square':
			containerObj=self.shapeGeo.create_circle(centerX=containerCpX,centerY=containerCpY,side=containerObjParams.get_item_param().get_side(),rotation=containerObjParams.get_item_rotation_angle())



		# Initial Population
		initialPopultion=[]

		# Total weight of the container
		containerWeight=containerObjParams.get_item_weight()

		# Total number of objects
		numberOfObjects=len(objects.keys())-1


		# Calculate number of solutions per item
		numSolutionsPerItem = self.eaParams.populationSize // numberOfObjects


		# 
		for itemCode in range(1,numberOfObjects+1):


			# First create an shape for the object.
			newObject=None
			
			# Per item solution for the new object
			newObjectSolCount=0


			# Manipulate the selected item so that it satisfies the placement rule
			for j in range(self.eaParams.objectSelectionTries):

				# Choose a random placement and a random rotation for the object
				newObjCPX,newObjCPY=self.shapeGeo.get_random_point_from_shape(containerObj)
				newObjRotation=randint(0,360)
				objects[itemCode].set_item_center_point(newObjCPX,newObjCPY)
				objects[itemCode].set_item_rotation_angle(newObjRotation)



				if objects[itemCode].get_item_type()=='circle':
					newObject=self.shapeGeo.create_circle(centerX=newObjCPX,centerY=newObjCPY,radius=objects[itemCode].get_item_param().get_radius())

				elif objects[itemCode].get_item_type()=='square':
					newObject=self.shapeGeo.create_square(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)

				elif objects[itemCode].get_item_type()=='rti':
					newObject=self.shapeGeo.create_rti(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)

				# TODO 
				# elif objects[itemCode].get_item_type()=='ellipse':
				# 	newObject=self.shapeGeo.create_ellipse(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)

				# If it overlaps, continue and select another position and rotation
				if self.shapeGeo.check_shape_overlap(containerObj,newObject):
					continue

				# Append the object to the initial population
				initialPopultion.append((itemCode,newObject))

				# Increment the solution counter for this object
				newObjectSolCount+=1

				if newObjectSolCount== numSolutionsPerItem:
					break


		# Check if we have created the adequate population or not.

		self.logger.log_message("Initial Population Created With {0} Objects".format(len(initialPopultion)),"INF")


		# we have to add more objects to the initial population
		if len(initialPopultion) != self.eaParams.populationSize:

			numberOfRemainingItems=self.eaParams.populationSize-len(initialPopultion)


			self.logger.log_message("Needing {0} Objects To Fulfill The Population".format(numberOfRemainingItems),"INF")


			# for i in range(self.eaParams.populationSize - len(initialPopultion)):



			for i in range(self.eaParams.initPopSetupTries):


				# Select an object from the set of objects that are 
				# not in the container. Note that objectsInContainer is list of tuples, in which, item codes
				# are the first element of each of the tuples

				itemCode= choice([i for i in range(1,numberOfObjects+1) ])

				
				# Manipulate the selected item so that it satisfies the placement rule
				for j in range(self.eaParams.objectSelectionTries):

					
					# Choose a random placement and a random rotation for the object
					newObjCPX,newObjCPY=self.shapeGeo.get_random_point_from_shape(containerObj)
					newObjRotation=randint(0,360)
					objects[itemCode].set_item_center_point(newObjCPX,newObjCPY)
					objects[itemCode].set_item_rotation_angle(newObjRotation)


				
					# First create an shape for the object.
					newObject=None
					if objects[itemCode].get_item_type()=='circle':
						newObject=self.shapeGeo.create_circle(centerX=newObjCPX,centerY=newObjCPY,radius=objects[itemCode].get_item_param().get_radius())

					elif objects[itemCode].get_item_type()=='square':
						newObject=self.shapeGeo.create_square(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)

					elif objects[itemCode].get_item_type()=='rti':
						newObject=self.shapeGeo.create_rti(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)

					# TODO 
					# elif objects[itemCode].get_item_type()=='ellipse':
					# 	newObject=self.shapeGeo.create_ellipse(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)




					# Check if the object ovelaps the continer.

					# If it overlaps, continue and select another position and rotation
					if self.shapeGeo.check_shape_overlap(containerObj,newObject):
						continue

					

				
					# Adding the object to the container
					initialPopultion.append((itemCode,newObject))

					# Decrement the number of remaining objects 
					numberOfRemainingItems-=1
					break
					

				if numberOfRemainingItems == 0:
					break


		self.logger.log_message("Initial Population Created With {0} Objects".format(len(initialPopultion)),"INF")
		return initialPopultion



			



