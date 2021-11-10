import math
from guizero import App, Drawing

w = 600
h = 600

app = App(width=w, height=h)
drawing = Drawing(app, width=w, height=h)


def trans(x):
    return ((x + 20) * 5)

class Unit():
  def __init__(self, kind, number, x, y, theta):
    self.type = kind  # what type of soldier
    self.number = number  # how many men are still in the unit
    self.theta = theta  #this is the rotation of the unit
    self.x = x
    self.y = y
    self.a1 = [
        self.x + 5**(1 / 2) * math.cos(self.theta - 1.107),
        self.y + 5**(1 / 2) * math.sin(self.theta - 1.107)
    ]
    self.a2 = [
        self.x + 5**(1 / 2) * math.cos(self.theta + 1.107),
        self.y + 5**(1 / 2) * math.sin(self.theta + 1.107)
    ]
    self.b1 = [
        self.x + 5**(1 / 2) * math.cos(self.theta + 2.0344),
        self.y + 5**(1 / 2) * math.sin(self.theta + 2.0344)
    ]
    self.b2 = [
        self.x + 5**(1 / 2) * math.cos(self.theta + 4.2874),
        self.y + 5**(1 / 2) * math.sin(self.theta + 4.2874)
    ]

  def updateRot(self):
    self.a1 = [
        self.x + 5**(1 / 2) * math.cos(self.theta - 1.107),
        self.y + 5**(1 / 2) * math.sin(self.theta - 1.107)
    ]
    self.a2 = [
        self.x + 5**(1 / 2) * math.cos(self.theta + 1.107),
        self.y + 5**(1 / 2) * math.sin(self.theta + 1.107)
    ]
    self.b1 = [
        self.x + 5**(1 / 2) * math.cos(self.theta + 2.0344),
        self.y + 5**(1 / 2) * math.sin(self.theta + 2.0344)
    ]
    self.b2 = [
        self.x + 5**(1 / 2) * math.cos(self.theta + 4.2874),
        self.y + 5**(1 / 2) * math.sin(self.theta + 4.2874)
    ]

  def rotateCW(self):
    self.theta = self.theta + math.pi / 6
    self.updateRot()

  def rotateCCW(self):
    self.theta = self.theta - math.pi / 6
    self.updateRot()

  def translate(self, i, j):
    self.a1[0] = self.a1[0] + i
    self.a2[1] = self.a2[1] + j
    self.b1[0] = self.b1[0] + i
    self.b2[1] = self.b2[1] + j
    self.x = self.x + i
    self.y = self.y + j

class Player(Unit):
  def drawUnit(self):
    drawing.polygon(trans(self.a1[0]),trans(self.a1[1]),trans(self.a2[0]),trans(self.a2[1]),trans(self.b1[0]),trans(self.b1[1]),trans(self.b2[0]),trans(self.b2[1]), color="blue", outline=True, outline_color="black")
  

class Enemy(Unit):
  def drawUnit(self):
    drawing.polygon(trans(self.a1[0]),trans(self.a1[1]),trans(self.a2[0]),trans(self.a2[1]),trans(self.b1[0]),trans(self.b1[1]),trans(self.b2[0]),trans(self.b2[1]), color="red", outline=True, outline_color="black")


def main():
  units = []
  units.append(Player('Infantry', 1000, 10, 10, 0))
  units.append(Enemy('Infantry', 1000, 0, 0, 0))
  for i in range(len(units)):
    units[i].rotateCW()
    units[i].drawUnit()
  


main()
