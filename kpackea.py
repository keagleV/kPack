


class EvolAlgoParams:

	'''
		This class implements the parameters of the evolution algorithm.
	'''

	def __init__(self,):

		# Population size
		self.populationSize=100



class KpackEA:
	'''
		This class implements all the necessary function for the EA in the packing
		problem.
	'''


	def __init__ (self,objects):

		# Dictionary of all the objects
		self.objects=objects

	def initial_filtering(self):
		'''
			This function filters out some of the objects that cannot be
			placed in the container in any condition. Such conditions are

			1- the weight of the object exceeds the container's weight
			2- the area of the object exceeds the container's area
		'''
		pass


		





