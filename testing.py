from ranking import *
from dataset import *

datasets = [Penguin(), WingedAnimal(), Nixon(), Table(), Bear()]

for dataset in datasets:
	#ENTAILMENTS
	zero_entail(dataset.rules, dataset.queries.keys(), dataset.queries.values())
	print
	one_entail(dataset.rules, dataset.queries.keys(), dataset.queries.values())
	print
	me_entail(dataset.rules, dataset.queries.keys(), dataset.queries.values())
	print
	me_entail2(dataset.rules, dataset.queries.keys(), dataset.queries.values())