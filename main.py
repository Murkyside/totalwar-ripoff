import math
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

  def rotateCW(self,beta): #clockwise
    desire = self.theta + beta
    while self.theta < desire:
      self.theta = self.theta + math.pi / 12
      self.updateRot()
      print(self.theta)

  def rotateCCW(self,beta):#counterclockwise
    desire = self.theta - beta
    while self.theta > desire:
      self.theta = self.theta - math.pi / 12
      self.updateRot()

  def translate(self, i, j):
    print(i)
    self.a1[0] = self.a1[0] + i
    self.a1[1] = self.a1[1] + j
    self.a2[0] = self.a2[0] + i
    self.a2[1] = self.a2[1] + j
    self.b1[0] = self.b1[0] + i
    self.b1[1] = self.b1[1] + j
    self.b2[0] = self.b2[0] + i
    self.b2[1] = self.b2[1] + j
    self.x = self.x + i
    self.y = self.y + j

  def moveTo(self,a,b):
    gamma = (self.y-b[1])/((self.x**2+self.y**2)**(1/2)*(b[0]**2+b[1]**2)**(1/2))
    self.rotateCW(gamma)
    self.translate(a[0],a[1])
    delta = (a[1]-b[1])/((a[0]**2+a[1]**2)**(1/2)*(b[0]**2+b[1]**2)**(1/2))
    self.rotateCW(delta)

class Player(Unit): #extends unit
  def drawUnit(self):
    drawing.polygon(trans(self.a1[0]),trans(self.a1[1]),trans(self.a2[0]),trans(self.a2[1]),trans(self.b1[0]),trans(self.b1[1]),trans(self.b2[0]),trans(self.b2[1]), color="blue", outline=True, outline_color="black")
  

class Enemy(Unit): #extends unit
  def drawUnit(self):
    drawing.polygon(trans(self.a1[0]),trans(self.a1[1]),trans(self.a2[0]),trans(self.a2[1]),trans(self.b1[0]),trans(self.b1[1]),trans(self.b2[0]),trans(self.b2[1]), color="red", outline=True, outline_color="black")


def main():
  units = []
  units.append(Player('Infantry', 1000, 10, 10, 0,100,25))
  units.append(Enemy('Infantry', 1000, 0, 0, 0,100,15))
  units[0].rotateCW(math.pi/6)
  units[1].rotateCCW(math.pi/3)
  units[0].translate(50,10)
  units[0].moveTo([1,2],[200,30])
  for i in range(len(units)):
    units[i].drawUnit()
    print(units[i].length,units[i].height)
    print(units[i].alpha,units[i].beta)
    print(units[i].a1,units[i].a2,units[i].b1,units[i].b2)
  


main()
