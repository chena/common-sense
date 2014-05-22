from collections import defaultdict
from logic import *
from qm import *
from numpy import log2
from math import log,ceil


"""
algorithm for generating the set of candidates with enough support
"""
def cand_aprior(itemsets):
   res = []
   i,j = 0,1
   while i<len(itemsets):
      while j<len(itemsets) and itemsets[i][:-1] == itemsets[j][:-1]: j += 1
      for r in range(i,j):
	for s in range(r+1, j):
	   res.append(itemsets[r]+itemsets[s][-1:])
      i = j
   return res


def cand_subset(candidates):
   res = []
   cand_dict = defaultdict(int)
   #print 'cand',candidates
   candidates = map(tuple, candidates)
   for trans in db:
      for cand in candidates:
	#print trans,cand
	if cand_dict[cand] < support and not set(cand)-set(trans): 
	   cand_dict[cand]+=1
	   if cand_dict[cand] >= support:
		res.append(cand)
   return res

"""
algorithm for frequency count of each candidate
"""
def cand_count(candidates):
   cand_dict = {}
   #cand_dict = defaultdict(int)
   candidates = map(tuple, candidates)
   for trans in db:
      for cand in candidates:
	#print trans,cand
        cand_dict.setdefault(cand,0)
	if not set(cand)-set(trans): 
	   cand_dict[cand]+=1
   
   for item,count in cand_dict.items():
      if count==len(data) or count < support: 
         nc.append(item)
         del cand_dict[item]
   return cand_dict

"""
returns the kb with complete assignment expression (include all variables)
"""
def full_kb(data, sym):
   ndata = defaultdict(float)
   for parts,p in data.items():
      nex = [v if v in parts else expr(~v) for v in sym]
      ndata[Expr('&', *nex)] = p
   return ndata

"""
computes the rank based on probability and parameter ep
"""
def rank(prob):
   return int(ceil(log2(prob)/log2(ep)))

"""
assign the rank value to each item in the dataset
"""
def prob_ranking():
   for r in data.keys():
      data[r].append(rank(data[r][0]))
   normal()
   
"""
normalize the ranking
"""
def normal():
   minr = min([r[1] for r in data.values()])
   for r in data:
      data[r][1] -= minr

"""
returns the approximate probability computed from rank value
"""
def app_prob(rank):
  return 1.0/(1.0 + ep**rank)

"""
"""
#def rule_rank(rule):


#####################################
db = []
support = 1
ep = 0.6

#setting data
data = []
nc = [] #null-conjunctions


a = Expr('a')
b = Expr('b')
c = Expr('c')
d = Expr('d')
e = Expr('e')
f = Expr('f')

#might need to sort logical var in each example first
data = defaultdict(float)

#data[a & b & c & d & e] = [0.5463]
#data[a & b & c & d] = [0.1944]
#data[a & c & d & e] = [0.1019]
#data[a & c & d] = [0.0833]
#data[a & b & c & e] = [0.0556]
#data[a & b & c] = [0.0185]

alpha = [a, b, c, d, e]
data[(a,b,c,d,e)] = [0.5463]
data[(a,b,c,d)] = [0.1944]
data[(a,c,d,e)] = [0.1019]
data[(a,c,d)] = [0.0833]
data[(a,b,c,e)] = [0.0556]
data[(a,b,c)] = [0.0185]

"""
alpha = [a,b,c]
data[(a,b,c)] = [0.1950]
data[(b,c)] = [0.1528]
data[(a,b)] = [0.1758]
data[(b,)] = [0.1378]
data[(a,c)] = [0.0408]
data[(c,)] = [0.1081]
data[(a,)] = [0.0519]
data[()] = [0.1378]
"""

"""
p = Expr('Penguin')
b = Expr('Bird')
f = Expr('Fly')
w = Expr('Wings')
alpha = [f, p, w, b] #fly, penguins, wings, birds
#data[()] = [0.05] #any non-bird non-winged animals do not fly(dog, table)
#data[(w,)] = [0.1] #sth winged and non-bird and don't fly (cockroach)
data[(w,b)] = [0.3]  #bird with wings that doesn't fly and is not penguin (duck)
data[(p,w,b)] = [0.05] #normal penguins
data[(f,w)] = [0.05] #non-birds objects with wings that fly(butterflies, planes)
data[(f,w,b)] = [0.6] #normal birds(crows, eagles)
"""

print "***********STEP 1: APPLY APRIOR ALGORITHM, GET NC************"

#item_dict = defaultdict(int)
item_dict = {}
for a in alpha: item_dict.setdefault(a,0)

#generate L1
for parts in data.keys():
   print parts
   #parts = conjuncts(ex)
   exp = [v if v in parts else expr(~v) for v in alpha]
   db.append(exp)
   for p in parts: item_dict[p] += 1

#find nc
#for item,count in item_dict.items():
for item in alpha:
   count = item_dict[item]
   if count==len(data) or count < support:
      del item_dict[item]
      if count==len(data):
	item = expr(~item)
      nc.append(item)
      
#print 'nc',nc
#print 'dict',item_dict.items()

#compute the subset closure
subset = [[item] for item in item_dict.keys()]

print "C1: %s" % (alpha) 
print "L1: %s" % (subset)
print

cand_dict = {}
ans = []
k = 2

while True:
#while len(subset)>0:
   pre_res = subset, cand_dict
   candidates = cand_aprior(subset)

   subset = cand_subset(candidates)
   if len(subset)==0:
      ans = pre_res
      break

   #enumerate all possible combinations from each candidate
   cand_set = []
   for can in candidates:
      cand_set += [mo for mo in enum_models(can,[],nc)]

   #count the occurences from data
   cand_dict = cand_count(cand_set)
   for cc in cand_dict.items(): print cc
   
   
   print "C%s: %s" % (k,candidates) 
   print "L%s: %s" % (k,subset)
   print
   k += 1

print 'APRIOR ANS:'
print ans[0]
for item in ans[1].items():print item
print 'FINAL NC: ',nc   
print 

###really only need the NC set
#basic_rules = []

print "***********STEP 2: GENERATE BASIC RULE SET************"
rules_dict = defaultdict(list)

#generate the set of basic rules
#step 1: go through each item in the null-conjunction set
#generate all possible rules
for nitem in nc:
   if not type(nitem)==tuple:
      t = Expr(True)
      if nitem.op=='~':	
	#basic_rules.append(t >> nitem.args[0])
	rules_dict[nitem.args[0]].append(t)
      else:
	#basic_rules.append(t >> ~nitem)
	rules_dict[~nitem].append(t)
   else: #tuple
      combo_set = choose(nitem)
      for c in combo_set:
 	lhs,rhs= c, list(set(nitem)-set(c))[0]
	if(len(lhs) > 1): 
	   lhs = Expr('&', *lhs)
	else:
	   lhs = lhs[0]
	#print lhs,rhs
 	#basic_rules.append(lhs >> negation(rhs))
	rules_dict[negation(rhs)].append(lhs)

#step 2: go through each literal whose negation is not in nc and generate possible rules
rhs_set = set(alpha)-set([negation(c) for c in nc if type(c)!=tuple])

#for rhs,lhs_lst in rules_dict.items():

for rhs in rhs_set:
   lhs_lst = rules_dict[rhs]
   #if len(lhs_lst)==1 and lhs_lst[0]==Expr(True): 
   #   continue
   sym = list(alpha)
   nnc = list(nc)
   sym.remove(literal_symbol(rhs))
   for lhs in lhs_lst: nnc.append(lhs)
   models = enum_models(sym,[],nnc)
   for mo in models: rules_dict[rhs].append(mo)


print "BASIC RULE SET BEFORE QM"
for rhs,lhs_lst in rules_dict.items():
   for lhs in lhs_lst:
      if type(lhs)==list:
	if len(lhs)>1:
	   lhs = Expr('&', *lhs)
        else:
	   lhs = lhs[0]
      print expr(lhs >> rhs)
print 

print "***********STEP 3: APPLY QM ALGORITHM TO SIMPLIFY RULE SET************"
#step 3: after generating the basic rules, reduce the set using qm algorithm
for rhs,lhs_lst in rules_dict.items():
   #find groupings (items containing identical literal symbols)
   groups = grouping(lhs_lst)
   if not groups:continue
   #print rhs,groups.items()
   #group by identical literal_sym_set
   #then cal qm to reduce
   for sym,models in groups.items():
      dec_lst = []
      for mo in models:
	dec = m_dec(mo)
	dec_lst.append(dec)
      qm_out = qm_solve(dec_lst,[],sorted(sym))
      #print "qm out", qm_out
      if qm_out:
	for mo in models: rules_dict[rhs].remove(mo)
	for nmo in qm_out: rules_dict[rhs].append(nmo)
      #print qm_out

print "AFTER QM"
#default_rules = defaultdict(list)
default_rules = []
for rhs,lhs_lst in rules_dict.items(): 
   for lhs in lhs_lst:
      default_rules.append([(lhs,rhs),1,0]) #prob,rank
      if type(lhs)==list:
	if len(lhs)>1:
	   lhs = Expr('&', *lhs)
        else:
	   lhs = lhs[0]
      #default_rules[expr(lhs >> rhs)] = [1,0] #prob,rank
      print expr(lhs >> rhs)
print

print "***********STEP 4: ASSIGN RANKS TO EACH DEFAULT RULE************"
#step 4: rank each default rule based on the initial ranks assigned to each example in the dataset
prob_ranking()
#for r in data.items(): print r
#print
#for item in default_rules: print item

for item in default_rules:
   (lhs,rhs) = item[0][0],item[0][1]
   (nlhs, nrhs) = item[0][0], negation(item[0][1])
   print "lhs,rhs", lhs,rhs
   print "nlhs,nrhs", nlhs,nrhs
   var, nvar = [],[]
   if type(lhs)==list:
      var = list(lhs) 
      var.append(rhs)
   else: #probability is 1.0
      continue
   
   print "var",var
   models = enum_models(alpha, var, nc)
   print "models", len(models)
   if not models: continue
   for m in models: print m
   minr = 1e10
   for mo in models:
      key = tuple(order(mo, alpha))
      if len(key) < 2:continue
      print "pos",var,key,data[key]
      rank = data[key][1]
      if rank < minr: 
	minr = rank

   nvar = list(nlhs)
   nvar.append(nrhs)

   nmodels = enum_models(alpha, nvar, nc)
   print "nvar",nvar
   print "nmodels"
   for m in nmodels: print m
   nminr = 1e10
   for mo in nmodels:
      key = tuple(order(mo, alpha))
      if len(key) < 2:continue
      print "neg",nvar,key,data[key]
      rank = data[key][1]
      if rank < nminr:
	nminr = rank
   crank = abs(nminr-minr)
   item[1],item[2] = app_prob(crank),crank
   print "-------------------------------------------------------------"

for item in default_rules:
   lhs, rhs = item[0][0], item[0][1]
   if type(lhs)==list:
	if len(lhs)>1:
	   lhs = Expr('&', *lhs)
        else:
	   lhs = lhs[0]
   print "%s\t\t prob: %s, rank: %s" % (expr(lhs >> rhs), round(item[1],2), item[2])
   
