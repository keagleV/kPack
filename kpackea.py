from logger import Logger
from random import choices
from random import choice
from random import randint
from random import shuffle
from random import uniform
from collections import namedtuple


class EvolAlgoParams:

	'''
		This class implements the parameters of the evolution algorithm.
	'''

	def __init__(self):

		# Population size
		self.populationSize=100

		# Number of tries to select an object
		self.objectSelectionTries=1000
		self.objectAdditionTries=1000
		# Number of tries to set up the initial population
		self.initPopSetupTries=1000

		# Mating probability
		self.mateProb=0.7

		# Mutation probability
		self.mutProb=0.5

		# Mutation add action probability
		self.mutAddProb=0.4

		# Mutation remove action probability
		self.mutRemovProb=0.2

		# Mutation modify action probability
		self.mutModProb= 0.4
		



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


	def generate_initial_population(self,objects,containerObj,containerObjParams):
		'''
			This function generates the initial population for the
			EA algorithm
		'''
		
		# Initial population
		initialPopulation=[]

		for i in range(self.eaParams.populationSize):
			initialPopulation.append(self.pack_objects(objects,containerObj,containerObjParams))


		self.logger.log_message("Initial Population Created With {0} Objects".format(len(initialPopulation)),"INF")


		return initialPopulation


	def pack_objects(self,objects , containerObj , containerObjParams ):
		'''
			This function generates a solution for the packing problem and packs a set of
			objects to the container
		'''

		# Total weight of the container
		containerWeight=containerObjParams.get_item_weight()

		# Total area of the container
		containerArea=containerObjParams.get_item_area()

		# Total number of objects
		numberOfObjects=len(objects.keys())-1

		# Calculate number of solutions per item
		numSolutionsPerItem = self.eaParams.populationSize // numberOfObjects




		# Total weight of the objects in the container
		weightOfObjects=0 

		# Total area of the objects in the container
		areaOfObjects=0

		# Total value of the objects in the container
		valueOfObjects=0

		# List of objects that are in the container. Elements of 
		# this list are as (itemCode,Obj)
		objectsInContainer=[]



		for i in range(self.eaParams.initPopSetupTries):


			# Check for the early termination:
			# 1. The container is full
			# 2. No remaining objects

			if (weightOfObjects==containerWeight) or \
					( numberOfObjects == len(objectsInContainer) ):
					break

			# Select an object from the set of objects that are 
			# not in the container. Note that objectsInContainer is list of tuples, in which, item codes
			# are the first element of each of the tuples


			# Item code of the new object
			itemCode= choice([i for i in range(1,numberOfObjects+1) if i not in [e[0] for e in objectsInContainer] ])

			# Parameters of the new object
			newObjectParams = objects[itemCode]

			# Adding the newObject
			newObject = self.check_add_object_to_container(containerObj,containerObjParams,weightOfObjects,objectsInContainer,newObjectParams )

			if newObject:

			# # Check if this object can be placed in the container due
			# # to its weight and the weight of the existing objects.
			# # If so, discard the object and take the next object.
				# newObjectWeight=objects[itemCode].get_item_weight()
			# if weightOfObjects + newObjectWeight  > containerWeight:
			# 	continue


			# # First create an shape for the object.
			# newObject=None


			# # Manipulate the selected item so that it satisfies the placement rule
			# for j in range(self.eaParams.objectSelectionTries):

			# 	# Choose a random placement and a random rotation for the object
			# 	newObjCPX,newObjCPY=self.shapeGeo.get_random_point_from_shape(containerObj)
			# 	newObjRotation=randint(0,360)
			# 	objects[itemCode].set_item_center_point(newObjCPX,newObjCPY)
			# 	objects[itemCode].set_item_rotation_angle(newObjRotation)


			# 	if objects[itemCode].get_item_type()=='circle':
			# 		newObject=self.shapeGeo.create_circle(centerX=newObjCPX,centerY=newObjCPY,radius=objects[itemCode].get_item_param().get_radius())

			# 	elif objects[itemCode].get_item_type()=='square':
			# 		newObject=self.shapeGeo.create_square(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)

			# 	elif objects[itemCode].get_item_type()=='rti':
			# 		newObject=self.shapeGeo.create_rti(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)

			# 	# TODO 
			# 	# elif objects[itemCode].get_item_type()=='ellipse':
			# 	# 	newObject=self.shapeGeo.create_ellipse(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)




			# 	# Check if the object ovelaps the continer.

			# 	# If it overlaps, continue and select another position and rotation
			# 	if self.shapeGeo.check_shape_overlap(containerObj,newObject):
			# 		continue

			# 	# Check if the object overlaps the objects in the container
			# 	overlapStatus=0
			# 	for objTuple in objectsInContainer:
			# 		if self.shapeGeo.check_shape_overlap(objTuple[1],newObject):
			# 			overlapStatus=1
			# 			break

			# 	# If no overlap detected, add the object to the container/
			# 	# If so, try again with the object.
			# 	if not overlapStatus:
					
				# Adding the object to the container
				objectsInContainer.append((itemCode,newObject))

				# Updating the total weight of the objects in the container
				weightOfObjects += newObjectParams.get_item_weight()

				# Updating the total area of the objects in the container
				areaOfObjects+= newObjectParams.get_item_area()

				# Updating the total value of the objects in the container
				valueOfObjects += newObjectParams.get_item_value()

					# break


		# Return the pack of objects alongside the total weight and total area
		# of the objects in the container.

		return  [ objectsInContainer , weightOfObjects, valueOfObjects , containerArea - areaOfObjects ]


	def get_fittest_solution(self,population):

		'''
			This function will return the fittest solution(s) in the population
		'''

		# First find the maximum value in the solutions

		maxVal= max( [sol[2] for sol in population] )


		candidates = [ sol for sol in population if sol[2]==maxVal]


		if len(candidates) > 1:

			print("multiple candidate")
			
			# Find the minimum remaining area between these candidates

			minRemainArea=min( [sol[3] for sol in candidates] ) 

		
			candidates= [ sol for sol in candidates if sol[3]==minRemainArea ]

		return candidates



	def check_add_object_to_container(self,containerObj,containerObjParams,currObjectsWeight,objectsInContainer,newObjParams):
		'''
			This function will try to add a new object to the container. If it was successfull, it returns the created object,
			if not, it returns None
		'''

		# Check if this object can be placed in the container due
		# to its weight and the weight of the existing objects.
		# If so, discard the object and take the next object.
		newObjectWeight= newObjParams.get_item_weight()

		if currObjectsWeight + newObjectWeight  > containerObjParams.get_item_weight():
			return None


		# First create an shape for the object.
		newObject=None


		# Manipulate the selected item so that it satisfies the placement rule
		for j in range(self.eaParams.objectAdditionTries):

			# Choose a random placement and a random rotation for the object
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

			# TODO 
			# elif objects[itemCode].get_item_type()=='ellipse':
			# 	newObject=self.shapeGeo.create_ellipse(centerX=newObjCPX,centerY=newObjCPY,side=newObjParams.get_item_param().get_side(),rotation=newObjRotation)




			# Check if the object ovelaps the continer.

			# If it overlaps, continue and select another position and rotation
			if self.shapeGeo.check_shape_overlap(containerObj,newObject):
				continue

			# Check if the object overlaps the objects in the container
			overlapStatus=0
			for objTuple in objectsInContainer:
				if self.shapeGeo.check_shape_overlap(objTuple[1],newObject):
					overlapStatus=1
					break

			# If no overlap detected, add the object to the container/
			# If so, try again with the object.
			if not overlapStatus:
				
				return newObject
				# # Adding the object to the container
				# objectsInContainer.append((itemCode,newObject))

				# # Updating the total weight of the objects in the container
				# weightOfObjects += newObjectWeight

				# # Updating the total area of the objects in the container
				# areaOfObjects+= objects[itemCode].get_item_area()

				# # Updating the total value of the objects in the container
				# valueOfObjects += objects[itemCode].get_item_value()
		return None



	def get_random_object(self,objects,itemCodeBlackList):

		'''
			This function will select a random object. This random object will be filtered
			by the itemCodeBlackList.
		'''

		# List of all itemCodes
		itemCodes = [code for code in objects.keys() if code !=0]


		# Selecting a random itemCode and filter with itemCodeBlackList
		randomItemCode= choice([i for i in range(1,len(itemCodes)+1) if i not in itemCodeBlackList ])


		return randomItemCode



	def calculate_fitness_value(self,population,objects):
		'''
			This function will calculate the fitness value of the solutions of the 
			generation.

			The fitness value is a combination of the total value of the objects in
			the container and the remaining area of the container.
		'''

		# Container's total area
		containerArea= objects[0].get_item_area()

		for solution in population:


			''' 
			Each solution is a list of elements in which:
			 	First element: List of objects in the container
			    Second element: Total weight of objects in the container
				Third element: Total value of objects in the container
				Forth element: Remaining area in the container

			'''

			# For each solution, we have to calculate the total value of the objects 
			# in the solution and the remaining area of the container.

			# Total value of the objects in the container
			totalValueOfObjects=0

			# Total area of the objects in the container
			totalAreaOfObjects=0


			for obj in solution[0]:

				# obj[0] is the object's itemCode

				totalValueOfObjects += objects[obj[0]].get_item_value()

				totalAreaOfObjects += objects[obj[0]].get_item_area()



			# Updating the solution
			solution[2] = totalValueOfObjects
			solution[3] = containerArea - totalAreaOfObjects

			















		# containerObjParams=objects[0]

		# # Container center point coordinates
		# containerCpX,containerCpY=containerObjParams.get_item_center_point()

		# # Creating the object of the container based on its parameters
		# containerObj=None

		# if containerObjParams.get_item_type()=='circle':
		# 	containerObj=self.shapeGeo.create_circle(centerX=containerCpX,centerY=containerCpY,radius=containerObjParams.get_item_param().get_radius())

		# elif containerObjParams.get_item_type()=='square':
		# 	containerObj=self.shapeGeo.create_circle(centerX=containerCpX,centerY=containerCpY,side=containerObjParams.get_item_param().get_side(),rotation=containerObjParams.get_item_rotation_angle())



		# # Initial Population
		# initialPopultion=[]

		# # Total weight of the container
		# containerWeight=containerObjParams.get_item_weight()

		# # Total number of objects
		# numberOfObjects=len(objects.keys())-1


		# # Calculate number of solutions per item
		# numSolutionsPerItem = self.eaParams.populationSize // numberOfObjects


		# # 
		# for itemCode in range(1,numberOfObjects+1):


		# 	# First create an shape for the object.
		# 	newObject=None
			
		# 	# Per item solution for the new object
		# 	newObjectSolCount=0


		# 	# Manipulate the selected item so that it satisfies the placement rule
		# 	for j in range(self.eaParams.objectSelectionTries):

		# 		# Choose a random placement and a random rotation for the object
		# 		newObjCPX,newObjCPY=self.shapeGeo.get_random_point_from_shape(containerObj)
		# 		newObjRotation=randint(0,360)
		# 		objects[itemCode].set_item_center_point(newObjCPX,newObjCPY)
		# 		objects[itemCode].set_item_rotation_angle(newObjRotation)



		# 		if objects[itemCode].get_item_type()=='circle':
		# 			newObject=self.shapeGeo.create_circle(centerX=newObjCPX,centerY=newObjCPY,radius=objects[itemCode].get_item_param().get_radius())

		# 		elif objects[itemCode].get_item_type()=='square':
		# 			newObject=self.shapeGeo.create_square(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)

		# 		elif objects[itemCode].get_item_type()=='rti':
		# 			newObject=self.shapeGeo.create_rti(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)

		# 		# TODO 
		# 		# elif objects[itemCode].get_item_type()=='ellipse':
		# 		# 	newObject=self.shapeGeo.create_ellipse(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)

		# 		# If it overlaps, continue and select another position and rotation
		# 		if self.shapeGeo.check_shape_overlap(containerObj,newObject):
		# 			continue

		# 		# Append the object to the initial population
		# 		initialPopultion.append((itemCode,newObject))

		# 		# Increment the solution counter for this object
		# 		newObjectSolCount+=1

		# 		if newObjectSolCount== numSolutionsPerItem:
		# 			break


		# # Check if we have created the adequate population or not.

		# self.logger.log_message("Initial Population Created With {0} Objects".format(len(initialPopultion)),"INF")


		# # we have to add more objects to the initial population
		# if len(initialPopultion) != self.eaParams.populationSize:

		# 	numberOfRemainingItems=self.eaParams.populationSize-len(initialPopultion)


		# 	self.logger.log_message("Needing {0} Objects To Fulfill The Population".format(numberOfRemainingItems),"INF")


		# 	# for i in range(self.eaParams.populationSize - len(initialPopultion)):



		# 	for i in range(self.eaParams.initPopSetupTries):


		# 		# Select an object from the set of objects that are 
		# 		# not in the container. Note that objectsInContainer is list of tuples, in which, item codes
		# 		# are the first element of each of the tuples

		# 		itemCode= choice([i for i in range(1,numberOfObjects+1) ])

				
		# 		# Manipulate the selected item so that it satisfies the placement rule
		# 		for j in range(self.eaParams.objectSelectionTries):

					
		# 			# Choose a random placement and a random rotation for the object
		# 			newObjCPX,newObjCPY=self.shapeGeo.get_random_point_from_shape(containerObj)
		# 			newObjRotation=randint(0,360)
		# 			objects[itemCode].set_item_center_point(newObjCPX,newObjCPY)
		# 			objects[itemCode].set_item_rotation_angle(newObjRotation)


				
		# 			# First create an shape for the object.
		# 			newObject=None
		# 			if objects[itemCode].get_item_type()=='circle':
		# 				newObject=self.shapeGeo.create_circle(centerX=newObjCPX,centerY=newObjCPY,radius=objects[itemCode].get_item_param().get_radius())

		# 			elif objects[itemCode].get_item_type()=='square':
		# 				newObject=self.shapeGeo.create_square(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)

		# 			elif objects[itemCode].get_item_type()=='rti':
		# 				newObject=self.shapeGeo.create_rti(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)

		# 			# TODO 
		# 			# elif objects[itemCode].get_item_type()=='ellipse':
		# 			# 	newObject=self.shapeGeo.create_ellipse(centerX=newObjCPX,centerY=newObjCPY,side=objects[itemCode].get_item_param().get_side(),rotation=newObjRotation)




		# 			# Check if the object ovelaps the continer.

		# 			# If it overlaps, continue and select another position and rotation
		# 			if self.shapeGeo.check_shape_overlap(containerObj,newObject):
		# 				continue

					

				
		# 			# Adding the object to the container
		# 			initialPopultion.append((itemCode,newObject))

		# 			# Decrement the number of remaining objects 
		# 			numberOfRemainingItems-=1
		# 			break
					

		# 		if numberOfRemainingItems == 0:
		# 			break
	


	def select_from_population(self,population):
		'''
			This function will select solutions from the population
		'''

		# List of solutions' values
		listOfSolsValues=[]

		# List of solution's remaining area
		listOfSolsAreas=[]


		for solution in population:
			listOfSolsValues.append(solution[2])
			listOfSolsAreas.append(solution[3])



		# Weight vector for the selection
		selectionVector=[]

		''' 
			Weight vector is defined as follows:

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

		# Normalizing values vector. Multiplication constant is 10.
		listOfSolsValues = [10*(val+1) for val in listOfSolsValues ]


		# Normalizing area vector
		listOfSolsAreas = [ (area+1) for area in listOfSolsAreas ]

		for (value, area) in zip(listOfSolsValues, listOfSolsAreas):
			selectionVector.append(value+1/area)



		# Now return a selection of the population based on the weight vector.
		selectedParents = choices(population,weights=selectionVector,k=len(population))
		
		# Return a shuffled form of the selected parents
		shuffle(selectedParents)
		
		return selectedParents



	def mate_population(self,population,containerObj):
		'''
			This function will mate the parents of the population, and generates the
			offsprings
		'''

		# List of parents that were are mated
		parentsNotMated=[]

		# List of new Offsprings
		newOffsprings=[]

		

		# self.shapeGeo.split_shape_with_crossing_line(population[0][0][0][1])

		# exit(0)
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
				containerSegments = self.shapeGeo.split_shape_with_crossing_line(containerObj)


				# List of objects that are in parent 1 and are in the first segment 
				parent1ObjectsSeg1 = []

				# List of objects that are in parent 1 and are in the second segment 
				parent1ObjectsSeg2 = []

				# List of objects that are in parent 2 and are in the first segment 
				parent2ObjectsSeg1 = []

				# List of objects that are in parent 1 and are in the second segment 
				parent2ObjectsSeg2 = []


				for obj in parent1Objects:


					if containerSegments[0].contains(obj[1]):
						parent1ObjectsSeg1.append(obj)

					elif containerSegments[1].contains(obj[1]):
						parent1ObjectsSeg2.append(obj)


				for obj in parent2Objects:

					if containerSegments[0].contains(obj[1]):
						parent2ObjectsSeg1.append(obj)

					elif containerSegments[1].contains(obj[1]):
						parent2ObjectsSeg2.append(obj)

				offspring1=[ *parent1ObjectsSeg1, *parent2ObjectsSeg2 ]
				offspring2=[ *parent1ObjectsSeg2 , *parent2ObjectsSeg1 ]
				


				# Remove duplicate items, #TODODODODODODOd
				# offspring1=list(set(offspring1))
				# offspring2=list(set(offspring2))



				# We append the new offsprings in the format of:
				# objectsInContainer , weightOfObjects, valueOfObjects , containerArea - areaOfObjects				
				newOffsprings.append( [offspring1,0,0,0] )
				newOffsprings.append( [offspring2,0,0,0] )


			else:
				# Add the previous parents without any change
				parentsNotMated.append(population[i])
				parentsNotMated.append(population[i+1])


		return (parentsNotMated,newOffsprings)



	def perform_mutation(self,containerObj,containerObjParams,objects,newOffsprings):
		'''
			This function will perform mutation on the popul
		'''

		# List of offsprings after mutation
		offsprings=[]

		for offs in newOffsprings:

			if uniform(0,1) <= self.eaParams.mutProb:

				# Choose an action
				action =  choices(["add","remove","modify"],weights=[self.eaParams.mutAddProb ,self.eaParams.mutRemovProb,self.eaParams.mutModProb  ],k=1)[0]


				if action == "add":


					# First find the itemCode of the objects int the solution which are going
					# to be filtered in the "add" action.
					itemsInContainer = [ x[0] for x in offs[0]  ]

					itemCode = self.get_random_object(objects,itemsInContainer)

					# Parameters of the new object
					newObjectParams = objects[itemCode]

					# Adding the newObject
					newObject = self.check_add_object_to_container(containerObj,containerObjParams,offs[1],offs[0], newObjectParams )

					if newObject:
						offs[0].append((itemCode,newObject))
					else:
						print("FAILED ADDING")

				elif action == "remove":

					if len(offs[0])!=0:

						# Select a random object to be deleted.
						objectToBeDeleted = choice(offs[0])

						# Removing the object from the list
						offs[0].remove(objectToBeDeleted)

				elif action == "modify":
					pass



			else:
				offsprings.append(offs)
