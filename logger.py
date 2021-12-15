


class Logger:
	'''
		This class has implemented the logger functionality which is going
		to be used through the program
	'''

	def log_message(self,message,status):

		'''
			This function will log the message to the console
		'''

		print("[{0}] {1}".format(status,message))
