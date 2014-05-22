from ranking import *
from collections import defaultdict

#learning algorithm
"""
KB = initial training data
FACTS/QUERIES = input data

step 1: given a KB with prior knowledge/examples, run the ranking algorithm to give an ordering for this set of default rules.
step 2: for each entry from the input data, determine if it is a question(query) or a statement(fact)
   - if it's a fact, add it to the KB
   - else it's a query, ask the KB to reason with it
   - if the KB knows the answer, add the resulting output rule to the KB
   - else the answer is undecided, add the query to the end of input data (for future)
*as more rules are added to the KB incrementally, it can answer more quries, becoming more intelligent.
"""

RULES = []
QUERIES = []
SENTS = []

#initial percepts
p = Expr('Penguin')
b = Expr('Bird')
a = Expr('Arctic')
f = Expr('Fly')
w = Expr('Wings')
m = Expr('Mobile')
c = Expr('Crane') #irrelevant feature not appearing in RULES
#statistical methods
ba = Expr('Bat')
bu = Expr('Butterfly')
s = Expr('Swallow')
e = Expr('Eagle')
pl = Expr('Plane')
ch = Expr('Chicken')
r = Expr('Rabbit')
fr = Expr('Frog')

h = Expr('Human')
eat = Expr('Eat')
jump = Expr('Jump')
"""
cr = Expr('Crow')
o = Expr('Owl')
d = Expr('Duck')
j = Expr('Jay')
"""

#default
RULES.append(p >> b) #penguins are birds
RULES.append(p >> ~f)#penguins do not fly
RULES.append(p >> w) #penguins have wings
#RULES.append(b >> f) #birds fly --> i want to learn this
#RULES.append(p >> a) #penguing live in the arctic
#RULES.append(b >> w) #birds have wings
RULES.append(e >> b) #eagles are birds
RULES.append(e >> f) #eagles fly

RULES.append(c >> f) #cranes fly
RULES.append(c >> b) #cranes are birds
RULES.append(e >> w) #eagles have wings
RULES.append(w >> f) #animals with wings typically fly
#RULES.append(b >> f) #birds typically fly


#from paper
"""
RULES.append(p >> b) #penguins are birds
RULES.append(p >> ~f)#penguins do not fly
RULES.append(b >> f) #birds fly
RULES.append(b >> w) #birds have wings
"""

"""
#statistical methods (try to conclude that "Birds normally fly")
RULES.append(ba >> f) #bats fly
RULES.append(ba >> ~b) #bats are not birds
RULES.append(bu >> f) #butterflies fly
RULES.append(bu >> ~b) #butterflies are not birds
RULES.append(c >> f) #cranes fly
RULES.append(c >> b) #cranes are birds
RULES.append(s >> f) #swallows fly
RULES.append(s >> b) #swallows are birds
RULES.append(ch >> b) #chickens are birds
RULES.append(ch >> f) #chickens fly
RULES.append(e >> b) #eagles are birds
RULES.append(e >> f) #eagles fly
RULES.append(fr >> ~b) #frogs are not birds
RULES.append(fr >> ~f) #frogs don't fly
RULES.append(r >> ~b) #rabbits are not birds
RULES.append(r >> ~f) #rabbits don't fly
#other properties
RULES.append(e >> eat) #eagles eat birds
RULES.append(fr >> eat) #frogs eat birds
RULES.append(h >> eat) #humans eat birds
RULES.append(h >> jump) #humans jump
RULES.append(r >> jump) #rabbits jump
RULES.append(fr >> jump) #frogs jump
#RULES.append(f >> m) #animals that fly are mobile
"""

#prob not useful?
#dictionary mapping from lhs of rule to possible rhs's (pos or neg) and frequency counts
#rdict = defaultdict(lambda: defaultdict(int))
#dictionary mapping from rhs of rue to possible lhs (conditions) and frequency counts
#ldict = defaultdict(lambda: defaultdict(int))

"""
for rule in RULES:
   lhs, rhs = rule.args
   rdict[lhs][rhs] += 1
   ldict[rhs][lhs] += 1

for k,v in rdict.items(): print k, v.items()
print
for k,v in ldict.items(): print k, v.items()
"""

"""
#0-entailed
QUERIES.append((b & p) >> f)
SENTS.append('do penguin-birds fly?')
QUERIES.append(f >> p)
SENTS.append('are animals that fly typically penguins?')
QUERIES.append(b >> p)
SENTS.append('are birds typically penguins?')
QUERIES.append((p & a) >> b)
SENTS.append('are penguins that live in the arctic birds?')

#1-entailed
QUERIES.append(~b >> ~p)
SENTS.append('are non-bird animals typically not penguins?')
QUERIES.append(~f >> ~b)
SENTS.append('are animals that do not fly typically not birds?')
#QUERIES.append(b >> m)
#SENTS.append('are birds typically mobile?')
#QUERIES.append(~m >> ~b)
#SENTS.append('are animals that are not mobile typically not birds?')
QUERIES.append((p & ~w) >> b)
SENTS.append('are non-winged penguins birds?')
#adding a query with irrelevant
QUERIES.append((b & c) >> f)
SENTS.append('do crane-birds fly?')
"""

#QUERIES.append(p >> b) 
#SENTS.append('are penguins birds?')
#QUERIES.append(p >> ~f)
#SENTS.append('do penguins not fly?')
#QUERIES.append(p >> w) 
#ENTS.append('do penguins have wings?')
#QUERIES.append(e >> b) 
#SENTS.append('are eagles birds?')
#QUERIES.append(e >> f) 
#SENTS.append('do eagles fly?')
#QUERIES.append(e >> w) 
#SENTS.append('do eagles have wings?')
#QUERIES.append(w >> f) 
#SENTS.append('do animals with wings typically fly?')
#QUERIES.append(c >> f) 
#SENTS.append('do cranes fly?')
#QUERIES.append(c >> b) 
#SENTS.append('are cranes birds?')
#added
QUERIES.append(b >> f)
SENTS.append('do birds fly?')

#entailment
one_entail(RULES, QUERIES, SENTS)
print
me_entail(RULES, QUERIES, SENTS)
print
me_entail2(RULES, QUERIES, SENTS)

#incremental
"""
i = 0
qrules = []
while i < len(RULES):
   rule = RULES[i]
   if not rule in qrules:
      qrules.append(RULES[i])
   else: print "I found out this myself!"
   learned = me_entail2(qrules, QUERIES, SENTS, True)
   if learned==1 and not rule in qrules:
      print rule
      print "im adding a rule" 
      qrules.append(rule)
   #elif learned==0: qrules.append(neg(rule))
   i += 1

print qrules
"""
