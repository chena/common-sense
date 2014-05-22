# libraries used
import math
from logic import *
#-----------Global Variables----------
minterms=[]
dontcare=[]
varNum  =0


upperBound = 0
powersOfTwo = [1]
primeImps = []         #holds the prime imps but changes due to essential or row dominance
originalPrimeImps = [] #holds the prime imps without doing any change to it to be displayed to user
essential = []

#sort by length
#takes a list of lists and sort it according to length of lists
def __sortByLen(x,y):
 if len(x) > len(y):
  return 1
 elif len(x) < len(y):
  return -1
 else:
  return 0

#takes the two groups and check if they can be combined together or not
def __check(x,y):
 coveredLetter = x[0]^y[0]
 if coveredLetter not in powersOfTwo:
  return False
 for i in range(0,len(x)):
  r = x[i]^y[i]
  if r != coveredLetter:
   return False
 return True


def __getGroups(groups):
 usefulImp = [] # to hold the result (groups that could be formed)
 primeImp  = [] # to hold useful implicants
 isPrime = [True]*len(groups) # to till if this implicant was taken or not
 for i in range(0,len(groups)):
  for j in range(i,len(groups)):
   if __check(groups[i],groups[j])==True:
    isPrime[i] = False
    isPrime[j] = False
    group = sorted(groups[i]+groups[j])
    if group not in usefulImp:
     usefulImp.append(group)
 for i in range(0,len(isPrime)):
  if isPrime[i]==True:
   primeImp.append(groups[i])
 return usefulImp,primeImp

#gets prime implicants
def __getPrimeImps(groups):
 primeImps = []
 ans = groups
 while len(ans) > 0 :
  ans = __getGroups(ans)
  for i in ans[1]:
   primeImps.append(i)
  ans = ans[0] 
 return primeImps

#returns a string containing the chart
#input: primeImps....and minterms(without the dont care)
def __getChart(primeImps,minterms):
 maxlen =len(str(primeImps[0]))+len(__getName(primeImps[0]))
 if len(str(primeImps[-1]))+len(__getName(primeImps[-1])) > maxlen :
  maxlen =len(str(primeImps[-1]))+len(__getName(primeImps[-1]))
 chart = "minterms : ".ljust(maxlen) + " "*9
 for i in minterms:
  chart+=str(i)+" "*8
 chart+="\n"
 chart+="-"*((len(minterms))*8+maxlen+9) + "\n"
 for i in range(0,len(primeImps)):
  chart+=(str(primeImps[i]) + " " + __getName(primeImps[i])).ljust(maxlen+1) + " "*8
  for j in minterms:
   if j in primeImps[i]:
    chart+="*" + " "*(8+len(str(j))-1)
   else:
    chart+="-" + " "*(8+len(str(j))-1)
  chart+="\n"
 return chart

#essential primeImps
#removes the essential prime Imps from primeImps and returns them
def __essentialPrimeImps(minterms):
 global primeImps
 counter = []
 for i in range(0,len(minterms)):
  counter.append([0,0])
 essential = []
 for imp in range(0,len(primeImps)):
  for i in primeImps[imp]:
   try:
    index=minterms.index(i)
    counter[index][0] += 1
    counter[index][1] = imp 
   except:
    pass
 for i in range(0,len(counter)):
  if counter[i][0]==1:
   #del minterms[i-shift]
   for term in primeImps[counter[i][1]]:
    try:
     del minterms[minterms.index(term)]
    except:
     pass
   if primeImps[counter[i][1]] != []:
    essential.append(primeImps[counter[i][1]])
    primeImps[counter[i][1]] = [] 
    
 primeImps=[i for i in primeImps if len(i) != 0]
 return essential
   
#cost of solution in petric way
def __getCost(group):
 cost = 0
 for i in group:
  cost = cost + int((varNum-math.log(len(primeImps[i]))/math.log(2))) + 1
 return cost


#takes an expression and simplifies it
def __simplify(product):
 #product.sort(sortByLen)
 for i in range(0,len(product)-1): 
  for j in range(i+1,len(product)):
   if set(product[i]).issubset(product[j]):
    del product[j]
    __simplify(product)
    return

#generate petric expr for petric way
def __genPetricExp(primeImps):
 petricExpr = []
 for i in range(0,len(minterms)):
  cterm = [] # an and term in petric expr
  for j in range(0,len(primeImps)):
   if minterms[i] in primeImps[j]:
    cterm.append([j])
  petricExpr.append(cterm)
 return petricExpr

#petric brute force way
def __petric(terms):
 while len(terms) > 1:
  z=[]
  for i in terms[0]:
   for j in terms[1]:
    z.append(list(set(i+j)))
  del terms[0]
  del terms[0]
  z.sort(__sortByLen)
  __simplify(z)
  terms.insert(0,z)
 return terms


#sort petric by Cost
def __sortByCost(x,y):
 cx=__getCost(x) #cost of the first
 cy=__getCost(y) #cost of the second
 if cx > cy:
  return 1
 elif cx < cy:
  return -1
 else:
  return 0

#returns the name of a group in letters
def __getName(group):
 n = group[0]
 name = [0] * varNum
 j=1
 while n > 0:
  name[-1*j]=n%2
  n=n/2
  j+=1
 removeNum = int(math.log(len(group))/math.log(2))
 for i in range(0,len(name)):
  if name[i]==1:
   name[i] = varNames[i]
  else:
   name[i] = Expr('~', varNames[i])
 rm = []
 j = 1
 while len(rm) < removeNum:
  x=group[0]^group[j]
  if x in powersOfTwo:
   rm.append(int(math.log(x)/math.log(2)))
  j+=1
 res=[]
 for i in range(0,len(name)):
  if (varNum-(i+1)) not in rm:
   res.append(name[i])
 return res

#public method to get primeImps in numbers
def getPrimeImpsNum():
 global originalPrimeImps
 return originalPrimeImps

#public method to get primeImps in letters
def getPrimeImpsNames():
 global originalPrimeImps
 pImps=[]
 for i in originalPrimeImps:
  pImps.append(__getName(i))
 return pImps

#public method to get essential implicants names 
def getEssentialImpsNames():
 global essential
 eImps=[]
 for i in essential:
  eImps.append(__getName(i))
 return eImps
 
#public method to geordt essential implicants num
def getEssentialImpsNum():
 global essential
 return essential

#solver public method
def qm_solve(mintermsList,dontcareList,varList):
 global varNum
 global dontcare
 global minterms
 global upperBound
 global primeImps
 global originalPrimeImps
 global powersOfTwo
 global essential
 global varNames
 varNames = varList
 varNum = len(varList)
 dontcare = dontcareList
 minterms = mintermsList
 upperBound=2**varNum # according to number of variables
 minterms.sort()
 dontcare.sort()
 powersOfTwo=[1]
 while powersOfTwo[-1] < upperBound/2 :
  powersOfTwo.append(2**len(powersOfTwo))
 groups = sorted([[i] for i in minterms] + [[j] for j in dontcare])
 if len(groups) == 2**varNum :
  originalPrimeImps = []
  essential = []
  return
 primeImps = __getPrimeImps(groups)
 originalPrimeImps = primeImps[:]
 #get the essential terms
 #print "chart before taking essential :"
 #print __getChart(primeImps,minterms)
 essential = __essentialPrimeImps(minterms)
 answer=[]
 for i in essential:
  answer.append(__getName(i))
 if len(minterms)==0:
  return answer

 # if all ways failed or there are still minterms not covered do petric
 solutions = __petric(__genPetricExp(primeImps))[0] # the [0] is just to get the list inside the list
 solutions.sort(__sortByCost)
 cost = __getCost(solutions[0])
 for i in solutions:
  if __getCost(i) == cost:
   sol = []
   for j in i:
    #print str(primeImps[j]) + getName(primeImps[j])
    sol.append(__getName(primeImps[j]))
 return sol+answer
