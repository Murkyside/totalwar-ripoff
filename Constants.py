#everything the math module does we will do for ourselves here. It is current ~10x faster than math but has a domain of -pi to pi
pi = 3.141592653589
def sin(x):
  return(x-(x**3)/6+(x**5)/120-(x**7)/5040+(x**9)/362880)
def cos(x):
  return(1-x**2/2+x**4/24-x**6/720+x**8/40320)
def arctan(x):
  return(x-x**3/3+x**5/5-x**7/7+x**9/9)