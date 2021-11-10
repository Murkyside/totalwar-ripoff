import math

class Unit():

  def __init__(self,kind,number,x,y,theta):
    self.type = kind # what type of soldier
    self.number = number # how many men are still in the unit
    self.x = x
    self.y = y
    self.theta = theta #this is the rotation of the unit
    
  def rotate(self,direction):
    # rotate soldiers by 30 degrees, amount depends on input
    # special numbers - 63.435 & 116.565: DO NOT CHANGE
    a1 = [5**(1/2)*math.sin(self.theta-63.435), 5**(1/2)*math.cos(self.theta-63.435)]
    a2 = [5**(1/2)*math.sin(self.theta+63.435), 5**(1/2)*math.cos(self.theta+63.435)]
    b1 = [5**(1/2)*math.sin(self.theta+116.565), 5**(1/2)*math.cos(self.theta+116.565)]
    b2 = [5**(1/2)*math.sin(self.theta+243.435), 5**(1/2)*math.cos(self.theta+243.435)]
    print(a1,a2,b1,b2)
    


  def translate(self, i, j):

    return()

test = Unit('Infantry',1000,10,10,0)
test.rotate(0)

#oi kaylem: a1, a2, b1, b2 are the corners of the rectangle
#https://stackoverflow.com/questions/306316/determine-if-two-rectangles-overlap-each-other



def main():
  print('hello')
