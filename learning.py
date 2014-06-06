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