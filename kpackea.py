from logger import Logger
from random import choices
from random import choice
from random import randint
from random import shuffle
from random import uniform
from copy import deepcopy
from collections import namedtuple

import matplotlib.pyplot as plt


class EvolAlgoParams:

	'''
		This class implements the parameters of the evolution algorithm.
	'''

	def __init__(self):

		# Population size
		self.populationSize=50

		# Number of tries to select an object
		self.objectAdditionTries=1000

		# Number of tries to set up a solution
		self.initSolSetupTries=10

		# Mating probability
		self.mateProb=0.7

		# Mutation probability
		self.mutProb=0.9

		# Mutation add action probability
		self.mutAddProb=0.8

		# Mutation remove action probability
		self.mutRemovProb=0.05

		# Mutation modify action probability
		self.mutModProb= 0.15

		# Normalizing constant for the total values of solutions
		self.valueNormConst = 1000

		# Mutation adding item try scaling factor
		self.mutAddItemScale=2

		# Mutation modifying item try scaling factor
		self.mutModItemScale=2

		# Try factor for putting items on the boundary in the mating phase
		self.mateItemBoundaryScale=2



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


	# Done
	def initial_filtering(self,objects):
		'''
			This function filters out some of the objects that cannot be
			placed in the container in any condition. Such conditions are

			1- the weight of the object exceeds the container's weight
			2- the area of the object exceeds the container's area
		'''

		# Total number of objects is the total number of keys in the objects 
		# dictionary except the first one which is the container.
		totalNumObjects = len(objects.keys())-1 # -1 is to exclude the container

		# Total weight of the container
		containerWeight= objects[0].get_item_weight()

		# Total area of the container
		containerArea= objects[0].get_item_area()

		# Number of deleted objects after the filtering for logging purposes
		numOfDeletedObjects=0

		for k,v in list(objects.items()):
			
			# Skip the container
			if k==0:
				continue

			# Check for the weight and area of the item and if it is possible, filter the item
			if (v.get_item_weight() > containerWeight) or (v.get_item_area() > containerArea):
				
				# Deleting that item from the dictionary of items
				objects.pop(k)

				numOfDeletedObjects+=1


		# TODO better code ?
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



	'''

		DONE


	'''

	def generate_initial_population(self,objects,containerObj,containerObjParams):
		'''
			This function generates the initial population for the EA algorithm. 

			Each population, is a set of solutions. Each solution, is a container
			with a random selection and placement of items inside it.


			Each solution is a list of items as follows:
				[ e1, e2, e3, e4, e5]

					e1: List of all items inside the container. Each item is represented by a tuple of (Item's Code, Item's Geometric Object, Item's Parameter)
					e2: Total weight of the items inside the container.
					e3: Total value of the items inside the container.
					e4: Remaining area in the container after the placement of the items.
					e5: Fitness value of the current combination and placement of the items in the container.
		'''
		
		self.logger.log_message("Trying Generating Initial Population With {0} Solutions".format(self.eaParams.populationSize),"INF")


		# Initial population
		initialPopulation=[]

		# Loop in the count of the population size parameter, to create the population
		for i in range(self.eaParams.populationSize):
			initialPopulation.append(self.pack_objects(objects,containerObj,containerObjParams))


		self.logger.log_message("Initial Population Created With {0} Objects".format(len(initialPopulation)),"INF")


		return initialPopulation


	def pack_objects(self, objects , containerObj , containerObjParams ):
		'''
			This function generates a solution for the packing problem and packs a set of
			objects in to the container.
		'''

		# Total weight of the container
		containerWeight=containerObjParams.get_item_weight()

		# Total area of the container
		containerArea=containerObjParams.get_item_area()

		
		# Total number of objects
		numberOfObjects=len(objects.keys())-1




		# Total weight of the objects in the container
		weightOfObjects=0 

		# Total area of the objects in the container
		areaOfObjects=0

		# Total value of the objects in the container
		valueOfObjects=0

		# List of objects that are in the container. Elements of 
		# this list are as (Item's code,Item's geometrical object, Item's parameters)
		objectsInContainer=[]



		for i in range(self.eaParams.initSolSetupTries):

			# Check for the early termination of this setup which can be:
			# 	1. The container is full
			# 	2. No remaining objects to choose and put inside the container

			if (weightOfObjects==containerWeight) or \
					( numberOfObjects == len(objectsInContainer) ):
					break

			# Select an object from the set of objects that are not in the container. 

			# Note that objectsInContainer is list of tuples, in which, item codes are the
			# first element of each of the tuples.


			# Item code of the new object
			itemCode= choice([i for i in range(1,numberOfObjects+1) if i not in [e[0] for e in objectsInContainer] ])

			# Parameters of the new object.
			newObjectParams = (objects[itemCode])

			# Try adding the new object to the container
			newObjectTuple = self.try_adding_object_to_container(containerObj,containerObjParams,weightOfObjects,objectsInContainer,newObjectParams)



			# If addition was successfull, then add the newly created object to the container
			# as a tuple of (Item's code, Item's geometrical object, Item's geometrical parameter)
			if newObjectTuple:

		
				# Adding the object to the container
				objectsInContainer.append((itemCode,newObjectTuple[0],newObjectTuple[1]))

				# Updating the total weight of the objects in the container
				weightOfObjects += newObjectParams.get_item_weight()

				# Updating the total area of the objects in the container
				areaOfObjects+= newObjectParams.get_item_area()

				# Updating the total value of the objects in the container
				valueOfObjects += newObjectParams.get_item_value()



		''' 
			Return the pack of objects alongside the total weight and total area of the objects 
			alonside the fitness value as the last element which is -1 at first.
		'''
		return  [ objectsInContainer , weightOfObjects, valueOfObjects , containerArea - areaOfObjects , -1 ]



	def try_adding_object_to_container(self,containerObj,containerObjParams,currObjectsWeight,objectsInContainer,newObjParams,scalingFator=1):
		'''
			This function will try to add a new object to the container. 

			If the addition it successfull, it returns the created object, otherwise , it returns None
		'''

		''' 
			Check if this object can be placed in the container due to its weight and 
			the weight constraint on the container. If it possible, Then try to choose random
			geometrical parameters for it to place it inside the container such that, it does
			not intersects with the container or any other item inside the container.

			It is obvious that it may be impossible to place an item since its geometrical
			parameters are chosen randomly. So, this process should be controlled by some
			thresholds of trying.
		'''

		newObjectWeight= newObjParams.get_item_weight()

		# If adding of the new objects causes exceeding the container's weight, then return None
		if currObjectsWeight + newObjectWeight  > containerObjParams.get_item_weight():
			return None



		# First create an shape for the object
		newObject=None


		# Manipulate the item so that it satisfies the placement policies
		for j in range(self.eaParams.objectAdditionTries//scalingFator):

			# Choose a random placement and a random rotation for the object

			# Choosing a random point inside the container as the center point of the object
			newObjCPX,newObjCPY=self.shapeGeo.get_random_point_from_shape(containerObj)
			newObjRotation=randint(0,360)
			newObjParams.set_item_center_point(newObjCPX,newObjCPY)
			newObjParams.set_item_rotation_angle(newObjRotation)


			if newObjParams.get_item_type()=='circle':
				newObject=self.shapeGeo.create_circle(centerX=newObjCPX,centerY=newObjCPY,radius=newObjParams.get_item_param().get_radius())

			elif newObjParams.get_item_type()=='square':

				newObject=self.shapeGeo.create_square(centerX=newObjCPX,centerY=newObjCPY,side=newObjParams.get_item_param().get_side(),rotation=newObjRotation)

			elif newObjParams.get_item_type()=='rti':
				newObject=self.shapeGeo.create_rti(centerX=newObjCPX,centerY=newObjCPY,side=newObjParams.get_item_param().get_side(),rotation=newObjRotation)

			elif newObjParams.get_item_type()=='ellipse':
				newObject=self.shapeGeo.create_ellipse(centerX=newObjCPX,centerY=newObjCPY,semiAxisX=newObjParams.get_item_param().get_semi_x(),semiAxisY=newObjParams.get_item_param().get_semi_y(),rotation=newObjRotation)




			''' 
				Check if the object ovelaps the continer or not. To check that, we can simply check
				whether the object is inside the container or not. If yes, it means that it does not
				overlap with the container.

			'''

			# If it overlaps, continue and select another position and rotation
			if not self.shapeGeo.check_shape_inside_other(containerObj,newObject):
				continue



			# Check if the new object overlaps with the objects residing in the container
			overlapStatus=0
			
			for objTuple in objectsInContainer:
				
				if self.shapeGeo.check_shape_overlap(objTuple[1],newObject):
					overlapStatus=1
					break

			# If no overlap detected, return the object with its parameter to the
			# packaging function. However, if overlap is detected, try again with the another position and rotation.
			if not overlapStatus:
				return (newObject,newObjParams)
				
		

		# If the threshold exceeds, return None which indicates that, the algorithm 
		# cannot place the new object.
		return None


	# Done
	def get_best_fitness_of_population(self,population):
		'''
			This function returns the best fitness value between the solutions of the population
		'''
		return  max( [sol[4] for sol in population] )


	# Done
	def get_fittest_solution(self,population):

		'''
			This function will return the fittest solution(s) in the population
		'''

		# First find best fitness value between the solutions of the population
		bestFitness = self.get_best_fitness_of_population(population)


		return  [ sol for sol in population if sol[4]==bestFitness]


	# DONE
	def get_random_object(self,objects,itemCodeBlackList):

		'''
			This function will select a random object. This random object will be filtered
			by the itemCodeBlackList.
		'''

		# List of all itemCodes except the container object which has the itemCode of 0.
		itemCodes = [code for code in objects.keys() if code !=0]


		# Check if any other object is left or not. If not, return -1
		if len(itemCodes) == len(list(set(itemCodeBlackList))):
			return -1

		# Selecting a random itemCode and filter with itemCodeBlackList and return it
	
		return choice([ i for i in itemCodes if i not in list(set(itemCodeBlackList)) ])
		

	# Done
	def calculate_fitness_value(self,population,objects):
		'''
			This function will calculate the fitness value of the solutions of the 
			generation.

			The fitness value is a combination of the total value of the objects in
			the container and the remaining area of the container.
		'''


		# List of solutions' values
		listOfSolsValues=[]

		# List of solution's remaining area
		listOfSolsAreas=[]


		for solution in population:
			listOfSolsValues.append(solution[2])
			listOfSolsAreas.append(solution[3])

		''' 
			Fitnesses of solutions are defined as follows:

				1). Normalizing values in the listOfSolsValues
				2). Normalizing values in the listOfSolsAreas
				3). Adding values of the two lists as (value(i) + 1/area(i) )


			Normalizing the listOfSolsValues:

				1). Add 1 to each element of the listOfSolsValues to adjust them
					beggining from 1.

				2). Multiply each element by a constant, to bring each element to a 
					secure zone.

			Normalizing the listOfSolsAreas:

				1). Add 1 to each element of the listOfSolsValues to adjust them
					beggining from 1.

		'''	

		# Normalizing values vector.
		listOfSolsValues = [ self.eaParams.valueNormConst *(val+1) for val in listOfSolsValues ]


		# Normalizing area vector
		listOfSolsAreas = [ (area+1) for area in listOfSolsAreas ]



		# Updating the fitness value of the solutions

		index=0
		for (value, area) in zip(listOfSolsValues, listOfSolsAreas):
			population[index][4]=(value+1/area)
			index+=1

	

	# Done
	def select_from_population(self,population):
		'''
			This function has implemented the selection portion of the EA algorithm and
			will select solutions based on their fitness value from the population. At the end
			it will shuffle the selected solutions.
		'''

		

		# Weight vector for the selection which is based on the fitness value
		selectionWeightVector=[]

		for solution in population:
			selectionWeightVector.append(solution[4])

		


		# Now return a selection of the population based on the weight vector.
		selectedParents = choices(population,weights=selectionWeightVector,k=len(population))
		


		# Return a shuffled form of the selected parents
		shuffle(selectedParents)
		


		return selectedParents



	# Done
	def mate_population(self,containerObj,containerObjParams,objects,population):
		'''
			This function has implemented the combination portion of the EA algorithm and 
			will mate the solutions of the population, and generate the possible offsprings
		'''

		# List of parents that won't be mated
		parentsNotMated=[]

		# List of new Offsprings resulted from the mating
		newOffsprings=[]



		# Select parents two by two and mate them based on the mating probability
		for i in range(0,len(population),2):

			# Mating should be performed
			if uniform(0,1) <= self.eaParams.mateProb:

				# List of offspeings resulting from mating the parents
				offspring1=[]
				offspring2=[]


				parent1 = population[i]
				parent2 = population[i+1]


				# List of objects in each parent
				parent1Objects = parent1[0]
				parent2Objects = parent2[0]


				# Split the container to two segments
				containerSegments ,line= self.shapeGeo.split_shape_with_crossing_line(containerObj)


				# List of objects that are in parent 1 and are in the first segment of the container
				parent1ObjectsSeg1 = []

				# List of objects that are in parent 1 and are in the second segment of the container
				parent1ObjectsSeg2 = []

				# List of objects that are in parent 2 and are in the first segment of the container
				parent2ObjectsSeg1 = []

				# List of objects that are in parent 1 and are in the second segment of the container
				parent2ObjectsSeg2 = []


				# List of objects that are on the crossing boundary in the first parent
				parent1ObjectsObBoundary=[]

				# List of objects that are on the crossing boundary in the second parent
				parent2ObjectsObBoundary=[]



				for obj in parent1Objects:

					if containerSegments[0].contains(obj[1]):
						parent1ObjectsSeg1.append(obj)

					elif containerSegments[1].contains(obj[1]):
						parent1ObjectsSeg2.append(obj)

					else:
						parent1ObjectsObBoundary.append(obj)


				for obj in parent2Objects:

					if containerSegments[0].contains(obj[1]):
						parent2ObjectsSeg1.append(obj)

					elif containerSegments[1].contains(obj[1]):
						parent2ObjectsSeg2.append(obj)

					else: 
						parent2ObjectsObBoundary.append(obj)


				# Creating the list of objects in the offsprings
				offspring1=[ *parent1ObjectsSeg1, *parent2ObjectsSeg2 ]
				offspring2=[ *parent2ObjectsSeg1 , *parent1ObjectsSeg2 ]

				

				# Removing duplicate items in the offspring1
				offspring1ItemCodes=[]
				for tup in offspring1:
					'''
						If the item code was previously put in the container, it means, 
						we have duplicate items. Otherwise, we consider this as a new item in
						the offspring
					'''
					if tup[0] in offspring1ItemCodes:
						offspring1.remove(tup)
					else:
						offspring1ItemCodes.append(tup[0])

				
				# Removing duplicate items in the offspring2
				offspring2ItemCodes=[]
				for tup in offspring2:

					'''
						If the item code was previously put in the container, it means, 
						we have duplicate items. Otherwise, we consider this as a new item in
						the offspring
					'''
					if tup[0] in offspring2ItemCodes:
						offspring2.remove(tup)
					else:
						offspring2ItemCodes.append(tup[0])


				# Calculate the total values, weight, and area of the objects in each offspring
				offspring1TotalWeight=0
				offspring1TotalValue=0 
				offspring1TotalArea=0

				offspring2TotalWeight=0
				offspring2TotalValue=0 
				offspring2TotalArea=0



				for tup in offspring1:
					offspring1TotalWeight+= tup[2].get_item_weight()
					offspring1TotalValue+= tup[2].get_item_value()
					offspring1TotalArea+= tup[2].get_item_area()

				for tup in offspring2:
					offspring2TotalWeight+= tup[2].get_item_weight()
					offspring2TotalValue+= tup[2].get_item_value()
					offspring2TotalArea+= tup[2].get_item_area()



				# Deciding what to do with objects on the boundary crossing line
				for objTuple in parent1ObjectsObBoundary:

					# Try adding to the second parent if only it is not in the second parent
					# to avoid having duplicate items in the container
					if not ( objTuple[0] in offspring2ItemCodes ) :


						obj = self.try_adding_object_to_container(containerObj,containerObjParams,offspring2TotalWeight,offspring2, objTuple[2] ,self.eaParams.mateItemBoundaryScale )


						# If the addition was successful, add the object to the second offspring and
						# update the total weight, value and the area of the objects in the container of 
						# the second offspring
						if obj:	
							offspring2.append((objTuple[0],obj[0],obj[1]))
							offspring2TotalWeight += obj[1].get_item_weight()
							offspring2TotalValue+=obj[1].get_item_value()
							offspring2TotalArea+= obj[1].get_item_area()


				for objTuple in parent2ObjectsObBoundary:

					# Try adding to the first parent if only it is not in the first parent
					# to avoid having duplicate items in the container
					if not (objTuple[0] in offspring1ItemCodes ) :

						obj = self.try_adding_object_to_container(containerObj,containerObjParams,offspring1TotalWeight,offspring1, objTuple[2] ,self.eaParams.mateItemBoundaryScale )


						# If the addition was successful, add the object to the first offspring and
						# update the total weight, value and the area of the objects in the container of 
						# the first offspring
						if obj:	
							offspring1.append((objTuple[0],obj[0],obj[1]))

							offspring1TotalWeight += obj[1].get_item_weight()
							offspring1TotalValue+=obj[1].get_item_value()
							offspring1TotalArea+=obj[1].get_item_area()

				

				# We append the new offsprings in the format of:
				# objectsInContainer , weightOfObjects, valueOfObjects , containerArea - areaOfObjects	
				newOffsprings.append( [offspring1,offspring1TotalWeight ,offspring1TotalValue ,containerObjParams.get_item_area() - offspring1TotalArea,-1] )
				newOffsprings.append( [offspring2,offspring2TotalWeight,offspring2TotalValue,containerObjParams.get_item_area() - offspring2TotalArea,-1] )


			else:
				# Mating will not be performed and the these two parents should be left unchnaged
				parentsNotMated.append(population[i])
				parentsNotMated.append(population[i+1])


		return (parentsNotMated,newOffsprings)


	# Done
	def perform_mutation(self,containerObj,containerObjParams,objects,newOffsprings):
		'''
			This function has imlemented the mutation part of the EA algorithm and
			will perform mutation on the offsprings created in the solution mating phase.
		'''

		# List of offsprings after mutation
		offsprings=[]

		for offs in newOffsprings:

			if uniform(0,1) <= self.eaParams.mutProb:

				# Choose an action
				action =  choices(["add","remove","modify"],weights=[self.eaParams.mutAddProb ,self.eaParams.mutRemovProb,self.eaParams.mutModProb  ],k=1)[0]


				if action == "add":


					# First find the itemCode of the objects int the solution which are going
					# to be filtered in the "add" action. We have to care about not adding items
					# to the solution, that have been added to the container before.
					itemsInContainer = [ itemTupe[0] for itemTupe in offs[0]  ]
					
					# Get a random object for the addition
					itemCode = self.get_random_object(objects,itemsInContainer)

					# If itemcode is not -1, it means that we have objects that 
					# we can add to the container. Otherwise, it means that we have no
					# object left to add to the container.
					if itemCode != -1: 

						# Parameters of the new object
						newObjectParams =  objects[itemCode]

						# Adding the newObject
						newObject= self.try_adding_object_to_container(containerObj,containerObjParams,offs[1],offs[0], newObjectParams, self.eaParams.mutAddItemScale )


						if newObject:
							# If addition is possible, add the new object and update the total weight,
							# value, and area of the objects in the container
							offs[0].append((itemCode,newObject[0],newObject[1]))
							offs[1]+=newObjectParams.get_item_weight()
							offs[2]+=newObjectParams.get_item_value()
							offs[3]-=newObjectParams.get_item_area()

						#TODO total weight
						


				elif action == "remove":

					# Only perform deletion on an offspring that has objects inside itself
					if len(offs[0])!=0:

						# Select a random object to be deleted.
						objectToBeDeleted = choice(offs[0])

						# Parameters of the seleted object
						selectedObjParams = objectToBeDeleted[2]

						# Removing the object from the list
						offs[0].remove(objectToBeDeleted)

						# Updating the total weight, value, and area of the container
						# after removing the selected item
						offs[1]-=selectedObjParams.get_item_weight()
						offs[2]-=selectedObjParams.get_item_value()
						offs[3]+=selectedObjParams.get_item_area()

						# TODO total weight

				elif action == "modify":


					# Only perform modification on an offspring that has objects inside itself

					if len(offs[0])!=0:

						# Select a random object to be modified.
						objectToBeModified = choice(offs[0])

						# ItemCode of the selected object
						selectedObjItemcode = objectToBeModified[0]

						# Parameters of the seleted object
						selectedObjParams = objectToBeModified[2]

						# Remove the object from the container before performing modification
						offs[0].remove(objectToBeModified)


						# Modify the object and check if it can be added to the container or not
						newObjectTuple = self.try_adding_object_to_container(containerObj,containerObjParams, offs[1] - selectedObjParams.get_item_weight() ,offs[0], selectedObjParams,self.eaParams.mutModItemScale )



						if newObjectTuple:
								# If the modified object was successful and passed the placements plicies, 
								# put it back to the container with new geometrical parameters
								offs[0].append((selectedObjItemcode,newObjectTuple[0],newObjectTuple[1]))


						else:
							# Object modification did not satisify the placements rules, and 
							# so it has to be put back without any change to the container.
							offs[0].append(objectToBeModified)




			else:
				offsprings.append(offs)


	def draw(self,shapes,line):
		plt.plot(*line.xy,c='green')
		for shape in shapes:

			x, y = shape.exterior.xy

			plt.plot(x,y,c="black")

		plt.show()
