from Bee import bee 

class worker_bee(bee):

	# init une abeillee productrice
	def __init__(self,name = None, cost = 0, category = None, upgrade = [], prod = 0, bonus_fields = []):

		super().__init__(cost, name, category, upgrade)
		self._prod = prod
		self._bonus_fields = bonus_fields