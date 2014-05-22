from logic import *
from collections import defaultdict

#####################   FUNCTIONS   #####################
"""
returns a knowledge base object with the given set of rules
"""
def gen_kb(rset):
   rules = list(rset)
   kb = PropKB()
   #add each rule to the knowledge base
   for r in rules: kb.tell(r)
   return kb

"""
Consistency test: while the kb is nonempty, assign rank 0 to all rules that can be tolerated by all other rules in the kb. Remove these rules, increment rank and repeat the process.
"""
def consistency(rset):
   rules = list(rset)
   kb = gen_kb(rset)
   #dictionary of rule mapping to its rank
   kb_dict = defaultdict(int)
   consistent = True
   #initialize the rank
   rank = 0

   #determine if each rule can be tolerated by all other rules in the KB
   while len(kb.clauses) > 0 and consistent:
      bclause = Expr('&', *kb.clauses)
      rlist = []
      ritems = []
      for r in rules:
         lhs, rhs = r.args
         sent = lhs & rhs & bclause
         res = dpll_satisfiable(sent)
         if res:
	    conset = conjuncts(to_cnf(r))
	    rlist += conset
	    ritems.append(r)
      #assign ranks to rules that are tolareted and remove them from the KB
      if rlist:
         for r in ritems: rules.remove(r)
         for c in rlist: kb.retract(c)
         #ranked_kb.append(rlist)
         for r in rlist: kb_dict[r] = rank
         rank += 1
      else:
         consistent = False
   if consistent:
      #for r,k in kb_dict.items():
      #   print r,k
      return kb_dict
   else:
      #print "Inconsistent!"
      return

"""
Rank function: perform binary search on the set of rules R to find the lowest Z(r) such that there is a model for r that does not falsify any rule r' with priority Z(r') >= Z(r)
"""
def bin_rank(lst, qry, bottom, top):
   if top <= bottom: return bottom
   mid = (top + bottom)/2
   bclause = Expr('&', *lst[mid:])
   lhs, rhs = qry.args
   sent = lhs & rhs & bclause
   res = dpll_satisfiable(sent)
   if res:
      #print res
      return bin_rank(lst, qry, bottom, mid-1)
   else:
      #print "Inconsistent!"
      #print sent
      #print lst[mid]
      return bin_rank(lst, qry, mid+1, top)

"""
returns the negation of the given rule
"""
def neg(rule):
   lhs,rhs = rule.args
   if rhs.op=='~':
      return expr(lhs >> literal_symbol(rhs)) #double negation
   return expr(lhs >> ~rhs) 


"""
returns the set of rules the given model falsifies
"""
def falsify(model, rules):
   fset = []
   bclause = Expr('&', *model)
   for r in rules:
      sent = to_cnf(r) & bclause 
      if not dpll_satisfiable(sent): fset.append(r)
   return fset

"""
ME algorithm: enumerate all models, and compute the rank for each model. Return the ranked model set
"""
def me_rank(ranked_kb, symbols):
   kblist = ranked_kb.items()
   #enumerate all possible models using truth table
   mset = enum_models(symbols)
   #for model in mset: print model
   """
   #find rules tolerated by all other rules
   zero_items = []
   for item in kblist:
      if item[1]==0: zero_items.append(item[0])
      else: break
   print zero_items
   """
   #iterate over all models, find the set of rules falsified by each model and calculate its rank
   #ranked_mset = defaultdict(int)
   mlist = []
   for model in mset:
      flst = falsify(model, ranked_kb.keys())

      rank = sum([1+ranked_kb[r] for r in flst])
      #ranked_mset[Expr('&', *model)] = rank
      mlist.append((set(model), rank))
   #return ranked_mset
   mlist.sort(key=lambda item: item[1])
   return mlist


#####################   ENTAILMENT APPROACHES   #####################

"""
Approach 1: 0 Entail function- returns the results of a set of queries using 0-entailment algorithm 
"""
def zero_entail(rset, qryset, sentset):
   print "**********************0-entailments**********************"
   qrules = list(rset)
   n = 1
   for qry,question in zip(qryset, sentset):
      qrules.append(qry)
      res = consistency(qrules)
      qrules.pop()
      qrules.append(neg(qry))
      nres = consistency(qrules)
      qrules.pop()
      ans = "I don't know"
      if res and not nres: ans = "Yes"
      elif  not res and nres: ans = "No"
      print 'query%s: %s %s' % (n,question,ans)
      n+=1

"""
Approach 2: 1 Entail function- returns the results of a set of queries using 0-entailment algorithm 
"""
def one_entail(rset, qryset, sentset):
   print "**********************1-entailments**********************"
   ranked_kb = consistency(rset)
   kblist = ranked_kb.items()
   kblist.sort(key=lambda item: item[1])
   clist = [item[0] for item in kblist]
   n = 1
   for qry,question in zip(qryset, sentset):
      nqry = neg(qry)

      ind = bin_rank(clist, qry, 0, len(kblist)-1)
      #one more satisfiability test, checking if the model entails all rules of rank k(r)
      sind = [item[1] for item in kblist].index(kblist[ind][1])
      bclause = Expr('&', *clist[sind:])
      lhs, rhs = qry.args
      sent = lhs & rhs & bclause
      res = dpll_satisfiable(sent)
      rank = kblist[ind][1]
      if not res: rank += 1
      #print "rank of rule is ", rank

      ind = bin_rank(clist, nqry, 0, len(kblist)-1)
      sind = [item[1] for item in kblist].index(kblist[ind][1])
      bclause = Expr('&', *clist[sind:])
      lhs, rhs = nqry.args
      sent = lhs & rhs & bclause
      res = dpll_satisfiable(sent)
      nrank = kblist[ind][1]
      if not res: nrank += 1
      #print "rank of neg rule is ", rank
      ans = "I don't know"
      if rank < nrank: ans = "Yes"
      elif  rank > nrank: ans = "No"
      #print rank, nrank
      print 'query%s: %s %s' % (n,question,ans)
      n+=1

"""
Approach 3: max entropy- returns the results of a set of queries using max-entropy algorithm 
"""
def me_entail(rset, qryset, sentset, incr=True):
   print "**********************ME-entailment**********************"
   #get the ranked list using consistency-test
   ranked_kb = consistency(rset)
   bclause = Expr('&', *ranked_kb.keys())
   symbols = prop_symbols(bclause)
   ranked_m = me_rank(ranked_kb, symbols) 
   mlist = [m[0] for m in ranked_m]
   #for item in mlist: print item

   #get the ranks of each default rule
   n = 1
   for rule in rset:
      lhs, rhs = rule.args
      var = conjuncts(lhs) + conjuncts(rhs)
      models = enum_models(symbols, var)

      min_rank = len(models)
      for m in models:
         ind = mlist.index(m)
         rank = ranked_m[ind][1]
         if rank < min_rank:
	    min_rank = rank         
      pos_rank = min_rank      

      nqry = neg(rule)
      lhs, rhs = nqry.args
      var = conjuncts(lhs) + conjuncts(rhs)
      models = enum_models(symbols, var)
      min_rank = len(models)
      for m in models:
         ind = mlist.index(m)
         rank = ranked_m[ind][1]
         if rank < min_rank:
	    min_rank = rank   
      neg_rank = min_rank
      rank = neg_rank - pos_rank
      print 'ruls %s: %s, rank: %s' % (n, rule, rank)
      n += 1

   #find the minimal verifying model for the qry and its negation, then compare their ranks 
   n = 1
   for qry,question in zip(qryset, sentset):
      lhs, rhs = qry.args
      var = conjuncts(lhs) + conjuncts(rhs)
      models = enum_models(symbols, var)

      min_rank = len(models)
      for m in models:
         ind = mlist.index(m)
         rank = ranked_m[ind][1]
         if rank < min_rank:
	    min_rank = rank         
      pos_rank = min_rank      

      nqry = neg(qry)
      lhs, rhs = nqry.args
      var = conjuncts(lhs) + conjuncts(rhs)
      models = enum_models(symbols, var)
      min_rank = len(models)
      for m in models:
         ind = mlist.index(m)
         rank = ranked_m[ind][1]
         if rank < min_rank:
	    min_rank = rank   
      neg_rank = min_rank
      #print pos_rank, neg_rank
      ans = "I don't know"
      if pos_rank < neg_rank: ans = "Yes"
      elif  pos_rank > neg_rank: ans = "No"
      print 'query%s: %s %s' % (n,question,ans)
      n+=1

"""
Approach 3: max entropy- returns the results of a set of queries using max-entropy algorithm, use sum of all ranks of models instead of only the min. verifying model
"""
def me_entail2(rset, qryset, sentset, incr=False):
   print "**********************ME-entailment (Version 2)**********************"
   #get the ranked list using consistency-test
   ranked_kb = consistency(rset)
   #generate the ranked model set
   bclause = Expr('&', *ranked_kb.keys())
   symbols = prop_symbols(bclause)
   ranked_m = me_rank(ranked_kb, symbols) 
   #for item in ranked_m: print item
   mlist = [m[0] for m in ranked_m]
   #for item in mlist: print item
   
   #get the ranks of each default rule
   n = 1
   for rule in rset:
      lhs, rhs = rule.args
      var = conjuncts(lhs) + conjuncts(rhs)
      models = enum_models(symbols, var)       
      #for m in models: print m, ranked_m[mlist.index(m)][1]
      pos_rank = sum([ranked_m[mlist.index(m)][1] for m in models])
      #print
      nqry = neg(rule)
      lhs, rhs = nqry.args
      var = conjuncts(lhs) + conjuncts(rhs)
      models = enum_models(symbols, var)
      #for m in models: print m, ranked_m[mlist.index(m)][1]
      neg_rank = sum([ranked_m[mlist.index(m)][1] for m in models])
      #print pos_rank, neg_rank, "diff is", neg_rank - pos_rank
      rank = neg_rank - pos_rank
      #print pos_rank, neg_rank, "diff is", neg_rank - pos_rank, "sum is", neg_rank + pos_rank
      #print 'confidence level is:', float(neg_rank - pos_rank)/neg_rank
      print 'rule %s: %s, rank: %s' % (n, rule, rank)
      n += 1

   ans = ''
   #find the minimal verifying model for the qry and its negation, then compare their ranks 
   n = 1
   for qry,question in zip(qryset, sentset):
      lhs, rhs = qry.args
      var = conjuncts(lhs) + conjuncts(rhs)
      models = enum_models(symbols, var)       
      #for m in models: print m, ranked_m[mlist.index(m)][1]
      pos_rank = sum([ranked_m[mlist.index(m)][1] for m in models])
      #print
      nqry = neg(qry)
      lhs, rhs = nqry.args
      var = conjuncts(lhs) + conjuncts(rhs)
      models = enum_models(symbols, var)
      #for m in models: print m, ranked_m[mlist.index(m)][1]
      neg_rank = sum([ranked_m[mlist.index(m)][1] for m in models])
      #print pos_rank, neg_rank, "diff is", neg_rank - pos_rank
      ans = "I don't know"
      if pos_rank < neg_rank: ans = "Yes"
      elif  pos_rank > neg_rank: ans = "No"
      print 'query%s: %s %s' % (n,question,ans)
      n+=1
   
   #if last query can be answered, it is learned
   #return 1 if verified, 0 if falsified, -1 if unknown
   if ans=='Yes': return 1
   elif ans=='No': return 0
   else: return
   
