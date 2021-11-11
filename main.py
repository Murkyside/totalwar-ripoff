import math
from guizero import App, Drawing

w = 600
h = 600

app = App(width=w, height=h)
drawing = Drawing(app, width=w, height=h)


def trans(x): # Used for drawing items in nice places on the screen
    return ((x + 20) * 5) 

class Unit():
  def __init__(self, kind, number, x, y, theta,morale,length):
    self.type = kind  # what type of soldier
    self.number = number  # how many men are still in the unit
    self.theta = theta  #this is the rotation of the unit
    self.x = x
    self.y = y
    self.morale = morale

    #maths bullshit DO NOT TOUCH
    self.length = length 
    self.height = 200/self.length #area
    self.alpha = math.atan(self.length/self.height)
    self.beta = math.atan(self.height/self.length)
    self.diagonal = ((self.height**2)/4+(self.length**2)/4)**(1/2)
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

  def rotateCW(self): #clockwise
    self.theta = self.theta + math.pi / 6
    self.updateRot()

  def rotateCCW(self):#counterclockwise
    self.theta = self.theta - math.pi / 6
    self.updateRot()

  def translate(self, i, j):
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
  units[0].rotateCW()
  units[1].rotateCCW()
  units[0].translate(50,10)
  for i in range(len(units)):
    units[i].drawUnit()
    print(units[i].length,units[i].height)
    print(units[i].alpha,units[i].beta)
    print(units[i].a1,units[i].a2,units[i].b1,units[i].b2)
  


main()
