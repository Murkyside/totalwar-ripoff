# new code for shaun. This is much better and should actually work
import math # If you don't want to import the math module, send me a message and I'll send you some code to replace it
def rotate(points,theta): # takes the array points in the form [a1x,a1y,a2x,a2y,a3x,a3y,a4x,a4y] and theta being the angle or rotation you want the rectangle to have in radians. to get from degrees to radians mutiply your angle by (pi/180)
  # this finds the centre of your rectangle which will serve as our centre of rotation
  x = (points[0]+points[2]+points[4]+points[6])/4
  y = (points[1]+points[3]+points[5]+points[7])/4 

  for i in range(0,len(points),2):
    points[i] = (points[i] - x) * math.cos(theta) - (points[i+1] - y) * math.sin(theta) + x
    points[i+1] = (points[i] - x) * math.cos(theta) + (points[i+1] - y) * math.sin(theta) + y
  return(points) # returns points in the same way it received points
