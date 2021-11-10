import math
from guizero import App, Drawing 

w = 600
h = 600

app = App(width=w, height=h)  
drawing = Drawing(app, width=w, height=h)

def trans(x):
  return((x+20)*5)



class Unit():

  def __init__(self,kind,number,x,y,theta):
    self.type = kind # what type of soldier
    self.number = number # how many men are still in the unit
    self.theta = theta #this is the rotation of the unit

  def updateRot(self):
    self.a1 = [5**(1/2)*math.cos(self.theta-1.107), 5**(1/2)*math.sin(self.theta-1.107)]
    self.a2 = [5**(1/2)*math.cos(self.theta+1.107), 5**(1/2)*math.sin(self.theta+1.107)]
    self.b1 = [5**(1/2)*math.cos(self.theta+2.0344), 5**(1/2)*math.sin(self.theta+2.0344)]
    self.b2 = [5**(1/2)*math.cos(self.theta+4.2874), 5**(1/2)*math.sin(self.theta+4.2874)]

  def rotateCW(self):
    self.theta = self.theta + math.pi/6
    self.updateRot()
    
  def rotateCCW(self):
    self.theta = self.theta - math.pi/6
    self.updateRot()

  def drawUnit(self):
    drawing.rectangle(trans(self.a1[0]),trans(self.a1[1]),trans(self.a1[0])+5,trans(self.a1[1])+5,color = 'red')
    drawing.rectangle(trans(self.a2[0]),trans(self.a2[1]),trans(self.a2[0])+5,trans(self.a2[1])+5,color = 'red')
    drawing.rectangle(trans(self.b1[0]),trans(self.b1[1]),trans(self.b1[0])+5,trans(self.b1[1])+5,color = 'red')
    drawing.rectangle(trans(self.b2[0]),trans(self.b2[1]),trans(self.b2[0])+5,trans(self.b2[1])+5,color = 'red')
    
  def translate(self, i, j):
    self.a1[0] = self.a1[0]+i
    self.a2[1] = self.a2[1]+j
    self.b1[0] = self.b1[0]+i
    self.b2[1] = self.b2[1]+j

test = Unit('Infantry',1000,10,10,0)
test.rotateCW()

#oi kaylem: a1, a2, b1, b2 are the corners of the rectangle
#https://stackoverflow.com/questions/306316/determine-if-two-rectangles-overlap-each-other



def main():
  print('hello')
