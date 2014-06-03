from ranking import *

## TODO: abstract and refactor so that each dataset can be independent and pulled easily for testing

####################   RULES   #####################
RULES = []

#from system Z paper
p = Expr('Penguin')
b = Expr('Bird')
a = Expr('Arctic')
f = Expr('Fly')
w = Expr('Wings')
m = Expr('Mobile')
#added
c = Expr('Canadian') 
r = Expr('Red') # irrelevant feature not appearing in RULES

RULES.append(p >> b) # penguins are birds
RULES.append(b >> f) # birds fly
RULES.append(p >> ~f)# penguins do not fly
RULES.append(p >> a) # penguing live in the arctic
RULES.append(b >> w) # birds have wings
RULES.append(f >> m) # animals that fly are mobile
# added
RULES.append(c >> f) # Canadian animals usually fly

# for B1
"""
p = Expr('Penguin')
b = Expr('Bird')
a = Expr('Animal')
f = Expr('Fly')
c = Expr('Crane')
r = Expr('Rabbit')
# add for B2
t = Expr('Bat')

RULES.append(b >> f) #birds fly
RULES.append(p >> b) #penguins are birds
RULES.append(p >> ~f)#penguins do not fly
RULES.append(a >> ~f) #animals normally do not fly
RULES.append(b >> a) #birds are animals
RULES.append(p >> b) #animals normally do not fly
RULES.append(r >> a) #rabbis are animals
RULES.append(c >> b) #cranes are birds
#add for B2
RULES.append(t >> a) #bats are animals
RULES.append(t >> f) #bats normally fly
"""

# for B3
"""
q = Expr('Quakers')
p = Expr('Pacifist')
r = Expr('Republican')
a = Expr('Alice')
b = Expr('Ben')
# add for B4
h = Expr('Hawks')
v = Expr('Political Active')
c = Expr('Cindy')

RULES.append(q >> p) #quakers are normally pacifists
# RULES.append(r >> ~p) #republicans are normally not pacifists #exclude for B4
RULES.append(a >> q)#Alice is quaker
RULES.append(a >> ~r) #Alice is not republican
RULES.append(b >> r) #Ben is republican
RULES.append(b >> ~q) #Ben is not quaker
# add for B4
RULES.append(r >> h) #republicans are normally hawks
RULES.append(p >> v) #pacifists are normally politically active
RULES.append(h >> v) #hawks are normally politically active
RULES.append(p >> ~h) #pacifists are not hawks
RULES.append(c >> h) #Cindy is hawk
"""

# for A1 - A7
"""
a = Expr('A')
b = Expr('B')
c = Expr('C')
h = Expr('Heavy')
t = Expr('OnTable')
r = Expr('Red')

RULES.append(a >> h)#A is heavy
#RULES.append(b >> h) #B is heavy
RULES.append(h >> t)#heavy blocks are normally located on the table
RULES.append(a >> ~t) #A is not on the table
#RULES.append(b >> r) #B is red
#add for A3
#RULES.append(b >> ~r) #B is not red
#RULES.append(h >> r) #heavy blocks are normally red
RULES.append(c >> h) #C is heavy
"""

"""
# bear
b = Expr('Bear')
d = Expr('Dangerous')
t = Expr('Teddies')
h = Expr('Honey')
f = Expr('Fat')

RULES.append(b >> d) #bears are dangerous
RULES.append(t >> b) #teddies are bear
RULES.append(t >> ~d) #teddies are not dangerous
RULES.append(b >> h) #bears like honey
RULES.append((t & f) >> d) #fat teddies are typically dangerous
"""

#####################   QUERYING   #####################
#queries
QUERIES = []
SENTS = []

#from paper
# 0-entailed
QUERIES.append((b & p) >> f)
SENTS.append('do penguin-birds fly?')
QUERIES.append(f >> p)
SENTS.append('are animals that fly typically penguins?')
QUERIES.append(b >> p)
SENTS.append('are birds typically penguins?')
QUERIES.append((p & a) >> b)
SENTS.append('are penguins that live in the arctic birds?')

# 1-entailed
QUERIES.append(~b >> ~p)
SENTS.append('are non-bird animals typically not penguins?')
QUERIES.append(~f >> ~b)
SENTS.append('are animals that do not fly typically not birds?')
QUERIES.append(b >> m)
SENTS.append('are birds typically mobile?')
QUERIES.append(~m >> ~b)
SENTS.append('are animals that are not mobile typically not birds?')
QUERIES.append((p & ~w) >> b)
SENTS.append('are non-winged penguins birds?')
#adding a query with irrelevant
QUERIES.append((b & r) >> f)
SENTS.append('do red birds fly?')

#undecided
QUERIES.append(p >> w)
SENTS.append('do pengins have wings?')
QUERIES.append((p & ~a) >> b)
SENTS.append('are penguins that do not live in the arctic birds?')
QUERIES.append((p & ~a) >> w)
SENTS.append('do penguins that do not live in the arctic have wings?')
QUERIES.append(f >> b)
SENTS.append('are flying animals birds?')
QUERIES.append((c & p) >> f)
SENTS.append('do Canadian penguins fly?')

#for B1
"""
QUERIES.append(r >> f)
SENTS.append('do rabbits fly?')
QUERIES.append(c >> f)
SENTS.append('do cranes fly?')
QUERIES.append(p >> f)
SENTS.append('do penguins fly?')
#add for B2
QUERIES.append(t >> f)
SENTS.append('do bats fly?')
"""

#for B3
"""
QUERIES.append(a >> p)
SENTS.append('Alice is quaker but not republican, is she pacifist?')
#QUERIES.append(b >> p) #exclude for B4
#SENTS.append('is Ben pacifist?')
#add for B4
QUERIES.append(b >> h)
SENTS.append('Ben is republican but not quaker, is he hawk?')
QUERIES.append(b >> v)
SENTS.append('is Ben active?')
QUERIES.append(a >> v)
SENTS.append('Alice is quaker but not republican, is she active?')
QUERIES.append(c >> v)
SENTS.append('Cindy is hakw, is she active?')
"""

#for A1 - A7
"""
#QUERIES.append(b >> t)
#SENTS.append('is B on the table?')
#add for A3
#QUERIES.append(a >> r)
#SENTS.append('is A red?')
QUERIES.append(a >> t)
SENTS.append('is A on the table?')
QUERIES.append(c >> t)
SENTS.append('is C on the table?')
"""

#bear
"""
QUERIES.append((t & d & ~h) >> b)
SENTS.append('are dangerous teddies that do not like honey typically bears?')
QUERIES.append(t >> h)
SENTS.append('do teddies like honey?')
QUERIES.append(b >> f)
SENTS.append('are bears typically fat?')
"""

#ENTAILMENTS
zero_entail(RULES, QUERIES, SENTS)
print
one_entail(RULES, QUERIES, SENTS)
print
me_entail(RULES, QUERIES, SENTS)
print
me_entail2(RULES, QUERIES, SENTS)
