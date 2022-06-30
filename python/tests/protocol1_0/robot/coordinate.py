# from cmath import acos, cos, pi, sin
from math import atan2,acos, cos, pi, sin


def coordinate():
   
   x = 1
   y = 0
   
   L1 = 1
   L2 = 1
   
   th2 = acos((x^2+y^2-L1^2-L2^2)/(2*L1*L2))
   th1 = atan2(y,x) - atan2(L2*sin(th2), L1+L2*cos(th2))

   theta1 = th1*180/pi
   theta2 = th2*180/pi
   
   print(theta1)
   print(theta2)


coordinate()
