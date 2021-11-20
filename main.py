import time
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
def invTrans(x):
  return(x/5-20)

class Unit():
  isSelected = None
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
    self.phase = 0

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
    print('beta: ',beta, 'theta: ',self.theta)
    if math.fabs(self.theta-beta)<math.pi/12:
      self.theta = beta
      self.updateRot()
      return(True)
    else:
      self.theta = self.theta + math.pi / 12
      self.updateRot()
      return(False)
    
  def rotateCCW(self,beta):#counterclockwise
    print('beta: ',beta, 'theta: ',self.theta)
    if math.fabs(self.theta-beta)<math.pi/12:
      self.theta = beta
      self.updateRot()
      return(True)
    else:
      self.theta = self.theta - math.pi / 12
      self.updateRot()
      return(False)

  def rotate(self,omega):
    if self.theta < omega:
      self.rotateCW(omega)
    else:
      self.rotateCCW(omega)

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

  def updateLength(self,newLength):
    if math.fabs(self.length - newLength) < 1:
      self.length = newLength
      return(True)
    elif self.length > newLength:
      self.length = self.length - 1
      return(False)
    else:
      self.length = self.length + 1
      return(False)

  def moveTo(self,a,b):
    if self.phase == 0:
      if self.updateLength(((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)):
        self.phase = 1
      self.setupUnit()
      self.updateRot()
    elif self.phase == 1:
      gamma = math.acos(math.fabs((math.cos(self.theta)*(self.x-a[0])+math.sin(self.theta)*(self.y-b[0]))/((math.cos(self.theta)**2+math.sin(self.theta)**2)**(1.2)*((self.x-a[0])**2+(self.y-b[0])**2)**(1/2))))
      if self.rotate(gamma):
        self.phase = 2
    elif self.phase == 2:

      if self.translate((a[0]+b[0])/2,(a[1]+b[1])/2):
        self.phase = 3
    else:
      delta = math.acos((a[1]-b[1])/(((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)))-math.pi#this is wrong
      if self.rotate(delta):
        self.movement = [0,0]
        self.phase = 0
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
  # units[0].movement = [[30,20],[50,20]]
  # units[1].movement = [[20,10],[40,11]]
  return(units)

def update(units):
  for i in range(len(units)):
    if units[i].movement!=[0,0]:
      units[i].moveTo(units[i].movement[0],units[i].movement[1])

def render(units):
  drawing.rectangle(0,0,w,h,color = 'white')
  for i in range(len(units)):
    units[i].drawUnit()

def unitCollision(unit1,unit2):
  return
def unitSelection(x,y):
  for i in range(len(units)):
    unit = [units[i].a1,units[i].a2,units[i].b1,units[i].b2]
    collision = False

    # go through each of the vertices, plus
    # the next vertex in the list
    next1 = 0;
    for current in range(len(unit)):

      #get next vertex in list
      #if we've hit the end, wrap around to 0
      next1 = current+1;
      if (next1 == len(unit)):
        next1 = 0

      # get the PVectors at our current position
      # this makes our if statement a little cleaner
      vc = unit[current];    # c for "current"
      vn = unit[next1];       # n for "next"

      # compare position, flip 'collision' variable
      # back and forth
      if ((vc[1] > y) != (vn[1] > y) and (x < (vn[0]-vc[0])*(y-vc[1]) / (vn[1]-vc[1])+vc[0])):
        collision = not collision
      print((vc[1] > y) != (vn[1] > y))
    if collision:
      Unit.isSelected = i
      return
  Unit.isSelected = None


units = init()
iterator = 0
def main():
  global iterator
  global units
  # game loop
  #while iterator<5:
  iterator+=1
  timing = time.perf_counter()
  timing2 = time.perf_counter()
  #while time.perf_counter()-timing2 < 0.1 :
  update(units)
  render(units)
  #if time.perf_counter() - timing < 1:
    #time.sleep(0.5)
  #print(iterator)
  print(Unit.isSelected)

def userInput():
  return

# def bruhhhhhhh():
#   try:
#     print('success')
#     units[Unit.isSelected].moveTo(drawing.when_left_button_pressed,drawing.when_left_button_released)
#   except TypeError: 
#     print('oops')


# drawing.when_mouse_dragged = bruhhhhhhh
# drawing.when_clicked = unitSelection

timeElapsed = 0
first = None
def startTimer(event_data):
  global timeElapsed
  global first
  timeElapsed = time.perf_counter()
  first = [invTrans(event_data.x),invTrans(event_data.y)]

def compareTimer(event_data):
  global timeElapsed
  global first
  now = time.perf_counter()
  if now - timeElapsed < 0.5:
    unitSelection(invTrans(event_data.x),invTrans(event_data.y))
  else:
    if Unit.isSelected is not None:
      units[Unit.isSelected].movement = (first,[invTrans(event_data.x),invTrans(event_data.y)])


drawing.when_left_button_pressed = startTimer
drawing.when_left_button_released = compareTimer




drawing.repeat(500, main) 
app.display()