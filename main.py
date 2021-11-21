# Hey guys. Please make a github account, get added to the project and only contribute under the contributions branch
# see the document, discord, and plan file for instructions,resources and tasks. 
# rotation is totally shagged rn
import time # why is this a different colour?
import os # will need this later
import math # This may go soon
from guizero import App, Drawing # I want to get rid of this as soon as possible

# temporary drawing things =====================
w = 600
h = 600
app = App(width=w, height=h)
drawing = Drawing(app, width=w, height=h)
# temporary drawing things =====================

def trans(x): # Used for drawing items in nice places on the screen
  return ((x + 20) * 5) 
def invTrans(x): # Used for converting screen coords to logic coords
  return(x/5-20)

class Unit(): # some of these methods and variables should be protected/private + getters and setters are needed. However variables are not yet fully solidified. 
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
    # All these values can fluctuate upon the width of our unit changing and are used calculate the corners. Thus they must be recalculated when the unit is resized. 
    self.height = 200/self.length #all units have the same area (200 is our temporary arbitrary figure), therefore if we know the length we can find the height
    self.alpha = math.atan(self.length/self.height) # angle between the normal vector and the diagonal vector
    self.beta = math.atan(self.height/self.length) # angle between the tangent vector and the diagonal vector
    self.diagonal = ((self.height**2)/4+(self.length**2)/4)**(1/2) # length of the diagonal 
    
  def updateRot(self): # when the unit is rotated each of the corners must be rotated. This function is fairly straightforward. Note however that although alpha is limited to {alpha | 0 < alpha < pi/2, alpha e R}, theta's domain is unlimited meaning that we must either reset theta to within the range 0 - 2pi or account for that if we choose to implement our own maths functions
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

  def rotateCW(self,beta): # clockwise to beta
    # if we are less than one increment away then snap to rotation
    if math.fabs(self.theta-beta)<math.pi/12:
      self.theta = beta
      self.updateRot()# since we have rotated the unit the corners must be updated so that rendering and collision can be carried out corrrectly
      return(True) # tells moveTo whether unit has reached target or not
    else:
      self.theta = self.theta + math.pi / 12
      self.updateRot()# since we have rotated the unit the corners must be updated so that rendering and collision can be carried out corrrectly
      return(False) # tells moveTo whether unit has reached target or not
    
  def rotateACW(self,beta):# anti-clockwise to beta
    # if we are less than one increment away then snap to rotation
    if math.fabs(self.theta-beta)<math.pi/12:
      self.theta = beta
      self.updateRot()# since we have rotated the unit the corners must be updated so that rendering and collision can be carried out corrrectly
      return(True) # tells moveTo whether unit has reached target or not
    else:
      self.theta = self.theta - math.pi / 12
      self.updateRot() # since we have rotated the unit the corners must be updated so that rendering and collision can be carried out corrrectly
      return(False) # tells moveTo whether unit has reached target or not

  def rotate(self,omega): # shortest rotation to omega
    if self.theta < omega:
      if self.rotateCW(omega):
        return True
    else:
      if self.rotateACW(omega):
        return True
    return False

  def translate(self, i, j): # translate straight to (i j) in chunks of 1 at a time
    # find vector to target from position
    incX = i-self.x
    incY = j-self.y
    # find the magnitude of this vector
    magnitude = (incX**2+incY**2)**(1/2)
    #make it a unit vector
    incX = incX/magnitude # this is where speed modifiers would go
    incY = incY/magnitude
    #if we are less than one increment away then snap to position
    if math.fabs(self.x-i)<incX:
      self.x = i
      return(True) # tells moveTo whether unit has reached target or not
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
      return(False) # tells moveTo whether unit has reached target or not

  def updateLength(self,newLength):
    #if we are less than one increment away then snap to size
    if math.fabs(self.length - newLength) < 1:
      self.length = newLength
      return(True) # tells moveTo whether unit has reached target size or not
    elif self.length > newLength:
      self.length = self.length - 1
      return(False) # tells moveTo whether unit has reached target size or not
    else:
      self.length = self.length + 1
      return(False) # tells moveTo whether unit has reached target size or not

  def moveTo(self,a,b): # this is shit and it's too late for me to give a fuck
    print('boo')
    if self.phase == 0:
      if self.updateLength(((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)):
        self.phase = 1
      self.setupUnit()
      self.updateRot()
    elif self.phase == 1:
      gamma = math.acos((self.y-b[1])/(((self.x-b[0])**2+(self.y-b[1])**2)**(1/2)))
      #gamma = math.acos(math.fabs((math.cos(self.theta)*(self.x-a[0])+math.sin(self.theta)*(self.y-b[0]))/((math.cos(self.theta)**2+math.sin(self.theta)**2)**(1.2)*((self.x-a[0])**2+(self.y-b[0])**2)**(1/2))))
      print(gamma,self.theta)
      if self.rotate(gamma):
        print('hello!')
        self.phase = 2
    elif self.phase == 2:
      if self.translate((a[0]+b[0])/2,(a[1]+b[1])/2):
        self.phase = 3
    else:
      delta = math.acos((a[1]-b[1])/(((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)))-math.pi# I have no idea why i need to subtract pi, this doesn't work on paper no matter what I do but the computer is magic I guess
      if self.rotate(delta):
        self.movement = [0,0]
        self.phase = 0

class Player(Unit): #extends unit
  isSelected = None # the player can only control his own units
  def drawUnit(self): # I recon this is the best way of doing this feel free to disagree
    drawing.polygon(trans(self.a1[0]),trans(self.a1[1]),trans(self.a2[0]),trans(self.a2[1]),trans(self.b1[0]),trans(self.b1[1]),trans(self.b2[0]),trans(self.b2[1]), color="blue", outline=True, outline_color="black")
    drawing.line(trans(self.x),trans(self.y),trans(self.x+10*math.sin(self.theta)),trans(self.y+10*math.cos(self.theta)),color = 'black',width = 1)

class Enemy(Unit): #extends unit
  def drawUnit(self): # I recon this is the best way of doing this feel free to disagree
    drawing.polygon(trans(self.a1[0]),trans(self.a1[1]),trans(self.a2[0]),trans(self.a2[1]),trans(self.b1[0]),trans(self.b1[1]),trans(self.b2[0]),trans(self.b2[1]), color="red", outline=True, outline_color="black")


def init(): # bruv
  # units = [] # TODO: split units list into player list and enemy list
  playerUnits = []
  enemyUnits = []
  playerUnits.append(Player('Infantry', 1000, 10, 10, 0,100,25))
  enemyUnits.append(Enemy('Infantry', 1000, 0, 0, 0,100,15))
  playerUnits[0].rotateCW(math.pi/2)
  enemyUnits[0].rotateACW(math.pi/6)
  # units[0].movement = [[30,20],[50,20]]
  # units[1].movement = [[20,10],[40,11]]
  return(playerUnits, enemyUnits)

def update(playerUnits,enemyUnits):
  for i in range(len(playerUnits)):
    if playerUnits[i].movement!=[0,0]:
      playerUnits[i].moveTo(playerUnits[i].movement[0],playerUnits[i].movement[1])
  for i in range(len(enemyUnits)):
    if enemyUnits[i].movement!=[0,0]:
      enemyUnits[i].moveTo(enemyUnits[i].movement[0],enemyUnits[i].movement[1])

def render(playerUnits,enemyUnits):
  drawing.rectangle(0,0,w,h,color = 'white')
  for i in range(len(playerUnits)):
    playerUnits[i].drawUnit()
  for i in range(len(enemyUnits)):
    enemyUnits[i].drawUnit()

def unitCollision(unit1,unit2):
  return

def unitSelection(x,y):
  for i in range(len(playerUnits)):
    unit = [playerUnits[i].a1,playerUnits[i].a2,playerUnits[i].b1,playerUnits[i].b2]
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
    if collision:
      Player.isSelected = i
      return
  Player.isSelected = None


initialisation = init()
playerUnits = initialisation[0]
enemyUnits = initialisation[1]
iterator = 0
def main():
  global iterator
  global playerUnits
  global enemyUnits
  # game loop
  #while iterator<5:
  iterator+=1
  # timing = time.perf_counter()
  # timing2 = time.perf_counter()
  #while time.perf_counter()-timing2 < 0.1 :
  update(playerUnits,enemyUnits)
  render(playerUnits,enemyUnits)
  #if time.perf_counter() - timing < 1:
    #time.sleep(0.5)
  #print(iterator)
  print(Player.isSelected)


# This should probably be in it's own class or method or some shit but I dunno how these events work help ====================================
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
  if now - timeElapsed < 0.2:
    unitSelection(invTrans(event_data.x),invTrans(event_data.y))
  else:
    if Player.isSelected is not None:
      playerUnits[Player.isSelected].movement = (first,[invTrans(event_data.x),invTrans(event_data.y)])

drawing.when_left_button_pressed = startTimer
drawing.when_left_button_released = compareTimer

# ====================================


# more temporary drawing stuff ===================
# I wish shaun could hurry up and get a move on so I don't have to use this bullshit
drawing.repeat(500, main) 
app.display()
# more temporary drawing stuff ===================
