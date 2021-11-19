import time
import math
import Constants as tMaths
from guizero import App, Drawing

# temporary drawing things =====================
w = 600
h = 600
app = App(width=w, height=h)
drawing = Drawing(app, width=w, height=h)
# temporary drawing things =====================

def trans(x): # Used for drawing items in nice places on the screen
    return ((x + 20) * 5) 

class Unit():
  def __init__(self, kind, number, x, y, theta,morale,length):
    self.type = kind  # what type of soldier
    self.number = number  # amount of men
    self.theta = theta  #rotation of the unit
    self.x = x
    self.y = y
    self.morale = morale
    self.length = length 
    self.setupUnit()
    self.updateRot()
    self.movement = [0,0]

  def setupUnit(self):
    #maths bullshit DO NOT TOUCH
    self.height = 200/self.length #area
    self.alpha = math.atan(self.length/self.height)
    self.beta = math.atan(self.height/self.length)
    self.diagonal = ((self.height**2)/4+(self.length**2)/4)**(1/2)
    
  def updateRot(self):
    self.a1 = [
        self.x + self.diagonal**(1 / 2) * math.cos(self.theta - self.alpha),
        self.y + self.diagonal**(1 / 2) * math.sin(self.theta - self.alpha)
    ]
    self.a2 = [
        self.x + self.diagonal**(1 / 2) * math.cos(self.theta + self.alpha),
        self.y + self.diagonal**(1 / 2) * math.sin(self.theta + self.alpha)
    ]
    self.b1 = [
        self.x + self.diagonal**(1 / 2) * math.cos(self.theta + self.alpha+2*self.beta),
        self.y + self.diagonal**(1 / 2) * math.sin(self.theta + self.alpha+2*self.beta)
    ]
    self.b2 = [
        self.x + self.diagonal**(1 / 2) * math.cos(self.theta + 3*self.alpha+2*self.beta),
        self.y + self.diagonal**(1 / 2) * math.sin(self.theta + 3*self.alpha+2*self.beta)
    ]
    print('cos')
    print(self.theta + 3*self.alpha+2*self.beta)
    print(self.x + self.diagonal**(1 / 2) * math.cos(self.theta + 3*self.alpha+2*self.beta),self.x + self.diagonal**(1 / 2) * tMaths.cos(self.theta + 3*self.alpha+2*self.beta))

  def rotateCW(self,beta): #clockwise
    desire = self.theta + beta
    if math.fabs(self.theta-desire)<math.pi/12:
      self.theta = desire
      self.updateRot()
      return(True)
    else:
      self.theta = self.theta + math.pi / 12
      self.updateRot()
      return(False)
    
  def rotateCCW(self,beta):#counterclockwise
    desire = self.theta - beta
    if math.fabs(self.theta-desire)<math.pi/12:
      self.theta = desire
      self.updateRot()
      return(True)
    else:
      self.theta = self.theta - math.pi / 12
      self.updateRot()
      return(False)


  def translate(self, i, j):
    incX = i-self.x
    incY = j-self.y
    magnitude = (incX**2+incY**2)**(1/2)
    incX = incX/magnitude
    incY = incY/magnitude
    if math.fabs(self.x-i)<incX:
      self.x = i
      return(True)
    else:
      self.a1[0] = self.a1[0] + incX
      self.a1[1] = self.a1[1] + incY
      self.a2[0] = self.a2[0] + incX
      self.a2[1] = self.a2[1] + incY
      self.b1[0] = self.b1[0] + incX
      self.b1[1] = self.b1[1] + incY
      self.b2[0] = self.b2[0] + incX
      self.b2[1] = self.b2[1] + incY
      self.x = self.x + incX
      self.y = self.y + incY
      return(False)

  def moveTo(self,a,b):
    gamma = (self.y-b[1])/((self.x**2+self.y**2)**(1/2)*(b[0]**2+b[1]**2)**(1/2))
    if self.rotateCW(gamma):
      if self.translate(a[0],a[1]):
        delta = (a[1]-b[1])/((a[0]**2+a[1]**2)**(1/2)*(b[0]**2+b[1]**2)**(1/2))
        if self.rotateCW(delta):
          self.movement = [0,0]
  
class Player(Unit): #extends unit
  def drawUnit(self):
    drawing.polygon(trans(self.a1[0]),trans(self.a1[1]),trans(self.a2[0]),trans(self.a2[1]),trans(self.b1[0]),trans(self.b1[1]),trans(self.b2[0]),trans(self.b2[1]), color="blue", outline=True, outline_color="black")

class Enemy(Unit): #extends unit
  def drawUnit(self):
    drawing.polygon(trans(self.a1[0]),trans(self.a1[1]),trans(self.a2[0]),trans(self.a2[1]),trans(self.b1[0]),trans(self.b1[1]),trans(self.b2[0]),trans(self.b2[1]), color="red", outline=True, outline_color="black")


def init():
  units = []
  units.append(Player('Infantry', 1000, 10, 10, 0,100,25))
  units.append(Enemy('Infantry', 1000, 0, 0, 0,100,15))
  units[0].rotateCW(math.pi/2)
  units[1].rotateCCW(math.pi/6)
  return(units)

def update(units):
  for i in range(len(units)):
    if units[i].movement!=[0,0]:
      units[i].moveTo(units[i].movement[0],units[i].movement[1])
  return()

def render(units):
  for i in range(len(units)):
    units[i].drawUnit()

def collision(unit1,unit2):
  return()

def main():
  iterator = 0
  units = init()
  # game loop
  while iterator<5:
    iterator+=1
    timing = time.perf_counter()
    timing2 = time.perf_counter()
    while time.perf_counter()-timing2 < 0.1 :
      update(units)
    render(units)
    if time.perf_counter() - timing < 1:
      time.sleep(0.5)
 
main()
