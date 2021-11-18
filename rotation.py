# shit for shaun
import math
def rotate(a1,a2,b1,b2,theta): #a1, a2 etc. are coords of the rectangle these are arrays in the form[x,y]. theta is the rotation of the rectangle you want in radians 1 radian is pi/180 degrees gl
  
  
  #this can probably be majorly simplified but I just can't rn
  #It is also quite complicated due to the nature of the rectangle having to resize
  #Maths section =============================================================
  x = (a1[0]+a2[0]+b1[0]+b2[0])/2
  y = (a1[1]+a2[1]+b1[1]+b2[1])/2
  length = ((a1[0]+a2[0])**2+(a1[1]+a2[1]))**(1/2)

  height = 200/length #area
  alpha = math.atan(length/height)
  beta = math.atan(height/length)
  diagonal = ((height**2)/4+(length**2)/4)**(1/2)
  #Maths section =============================================================

  a1 = [
      x + diagonal**(1 / 2) * math.cos(theta - alpha),
      y + diagonal**(1 / 2) * math.sin(theta - alpha)
  ]
  a2 = [
      x + diagonal**(1 / 2) * math.cos(theta + alpha),
      y + diagonal**(1 / 2) * math.sin(theta + alpha)
  ]
  b1 = [
      x + diagonal**(1 / 2) * math.cos(theta + alpha+2*beta),
      y + diagonal**(1 / 2) * math.sin(theta + alpha+2*beta)
  ]
  b2 = [
      x + diagonal**(1 / 2) * math.cos(theta + 3*alpha+2*beta),
      y + diagonal**(1 / 2) * math.sin(theta + 3*alpha+2*beta)
  ]
  return(a1,a2,b1,b2)