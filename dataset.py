import abc
from logic import *

"""
Base class for all datasets
"""
class Dataset(object):
	__metaclass__  = abc.ABCMeta

	def __init__(self):
		self.rules = []
		self.queries = {}
		self.setup()
	
	@abc.abstractmethod
	def set_items(self):
		"""
		Define the items for thie dataset
		"""

	@abc.abstractmethod
	def set_rules(self):
		"""
		Define the rules for this dataset
		"""

	@abc.abstractmethod
	def set_queries(self, queries):
		"""
		Define the quries for this dataset
		"""

	def setup(self):
		self.set_items()
		self.set_rules()
		self.set_queries()

class Penguin(Dataset):
	def set_items(self):
		self.p = Expr('Penguin')
		self.b = Expr('Bird')
		self.a = Expr('Arctic')
		self.f = Expr('Fly')
		self.w = Expr('Wings')
		self.m = Expr('Mobile')
		#added
		self.c = Expr('Canadian') 
		self.r = Expr('Red') # irrelevant feature not appearing in rules

	def set_rules(self):
		self.rules.append(self.p >> self.b) # penguins are birds
		self.rules.append(self.b >> self.f) # birds fly
		self.rules.append(self.p >> ~self.f)# penguins do not fly
		self.rules.append(self.p >> self.a) # penguing live in the arctic
		self.rules.append(self.b >> self.w) # birds have wings
		self.rules.append(self.f >> self.m) # animals that fly are mobile
		# added
		self.rules.append(self.c >> self.f) # Canadian animals usually fly

	def set_queries(self):
		# 0-entailed
		self.queries[(self.b & self.p) >> self.f] = 'do penguin-birds fly?'
		self.queries[self.f >> self.p] = 'are animals that fly typically penguins?'
		self.queries[self.b >> self.p] = 'are birds typically penguins?'
		self.queries[(self.p & self.a) >> self.b] = 'are penguins that live in the arctic birds?'
		# 1-entailed
		self.queries[~self.b >> ~self.p] = 'are non-bird animals typically not penguins?'
		self.queries[~self.f >> ~self.b] = 'are animals that do not fly typically not birds?'
		self.queries[self.b >> self.m] = 'are birds typically mobile?'
		self.queries[~self.m >> ~self.b] = 'are animals that are not mobile typically not birds?'
		self.queries[(self.p & ~self.w) >> self.b] = 'are non-winged penguins birds?'
		self.queries[(self.b & self.r) >> self.f] = 'do red birds fly?'
		# undecided
		self.queries[self.p >> self.w] = 'do pengins have wings?'
		self.queries[(self.p & ~self.a) >> self.b] = 'are penguins that do not live in the arctic birds?'
		self.queries[(self.p & ~self.a) >> self.w] = 'do penguins that do not live in the arctic have wings?'
		self.queries[self.f >> self.b] = 'are flying animals birds?'
		self.queries[(self.c & self.p) >> self.f] = 'do Canadian penguins fly?'


class WingedAnimal(Dataset):
	def set_items(self): 
		self.p = Expr('Penguin')
		self.b = Expr('Bird')
		self.a = Expr('Animal')
		self.f = Expr('Fly')
		self.c = Expr('Crane')
		self.r = Expr('Rabbit')
		# add for B2
		self.t = Expr('Bat')

	def set_rules(self):
		self.rules.append(self.b >> self.f) # birds fly
		self.rules.append(self.p >> self.b) #penguins are birds
		self.rules.append(self.p >> ~self.f) # penguins do not fly
		self.rules.append(self.a >> ~self.f) # animals normally do not fly
		self.rules.append(self.b >> self.a) # birds are animals
		self.rules.append(self.p >> self.b) # animals normally do not fly
		self.rules.append(self.r >> self.a) # rabbis are animals
		self.rules.append(self.c >> self.b) # cranes are birds
		#add for B2
		self.rules.append(self.t >> self.a) # bats are animals
		self.rules.append(self.t >> self.f) # bats normally fly

	def set_queries(self):
		self.queries[self.r >> self.f] = 'do rabbits fly?'
		self.queries[self.c >> self.f] = 'do cranes fly?'
		self.queries[self.p >> self.f] = 'do penguins fly?'
		self.queries[self.t >> self.f] = 'do bats fly?'

class Nixon(Dataset):
	def set_items(self):
		self.q = Expr('Quakers')
		self.p = Expr('Pacifist')
		self.r = Expr('Republican')
		self.a = Expr('Alice')
		self.b = Expr('Ben')
		# add for B4
		self.h = Expr('Hawks')
		self.v = Expr('Political Active')
		self.c = Expr('Cindy')

	def set_rules(self):
		self.rules.append(self.q >> self.p) # quakers are normally pacifists
		# RULES.append(r >> ~p) # republicans are normally not pacifists #exclude for B4
		self.rules.append(self.a >> self.q) # Alice is quaker
		self.rules.append(self.a >> ~self.r) # Alice is not republican
		self.rules.append(self.b >> self.r) # Ben is republican
		self.rules.append(self.b >> ~self.q) # Ben is not quaker
		# add for B4
		self.rules.append(self.r >> self.h) # republicans are normally hawks
		self.rules.append(self.p >> self.v) # pacifists are normally politically active
		self.rules.append(self.h >> self.v) # hawks are normally politically active
		self.rules.append(self.p >> ~self.h) # pacifists are not hawks
		self.rules.append(self.c >> self.h) # Cindy is hawk

	def set_queries(self):
		self.queries[self.a >> self.p] = 'Alice is quaker but not republican, is she pacifist?'
		self.queries[self.b >> self.h] = 'Ben is republican but not quaker, is he hawk?'
		self.queries[self.b >> self.v] = 'is Ben active?'
		self.queries[self.a >> self.v] = 'Alice is quaker but not republican, is she active?'
		self.queries[self.c >> self.v] = 'Cindy is hakw, is she active?'

class Table(Dataset):
	def set_items(self):
		self.a = Expr('A')
		self.b = Expr('B')
		self.c = Expr('C')
		self.h = Expr('Heavy')
		self.t = Expr('OnTable')
		self.r = Expr('Red')

	def set_rules(self):
		self.rules.append(self.a >> self.h) # A is heavy
		self.rules.append(self.h >> self.t) # heavy blocks are normally located on the table
		self.rules.append(self.a >> ~self.t) # A is not on the table
		self.rules.append(self.c >> self.h) # C is heavy

	def set_queries(self):
		self.queries[self.a >> self.t] = 'is A on the table?'
		self.queries[self.c >> self.t] = 'is C on the table?'

class Bear(Dataset):
	def set_items(self):
		self.b = Expr('Bear')
		self.d = Expr('Dangerous')
		self.t = Expr('Teddies')
		self.h = Expr('Honey')
		self.f = Expr('Fat')

	def set_rules(self):	
		self.rules.append(self.b >> self.d) # bears are dangerous
		self.rules.append(self.t >> self.b) # teddies are bear
		self.rules.append(self.t >> ~self.d) # teddies are not dangerous
		self.rules.append(self.b >> self.h) # bears like honey
		self.rules.append((self.t & self.f) >> self.d) # fat teddies are typically dangerous

	def set_queries(self):
		self.queries[(self.t & self.d & ~self.h) >> self.b] = 'are dangerous teddies that do not like honey typically bears?'
		self.queries[self.t >> self.h] = 'do teddies like honey?'
		self.queries[self.b >> self.f] = 'are bears typically fat?'



