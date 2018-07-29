# author : Arief Anbiya (anbarief@live.com)
# Algorithm for the radial bar chart.

import numpy
sqrt = numpy.sqrt
cos = numpy.cos
sin = numpy.sin
pi =  numpy.pi
import matplotlib
import matplotlib.pyplot as plt

def rbar_A(ax, radii, radius, col, label, bar_width = 5, text_size = 7):

   n = len(radii)
   indexs = range(n)

   x = [-radius+i*0.01 for i in range(2*100*radius + 1)]
   y_upper = [sqrt(radius**2 - i**2) for i in x]
   y_lower = [-y for y in y_upper]

   ax.plot(x, y_upper, color = 'k')
   ax.plot(x, y_lower, color = 'k')
   
   dr = float(1)/float(n)

   indicator = 1
   
   for index in indexs:

      rx = (radius+((1/50)*radius)*radii[index])*cos(dr*index*2*pi)
      ry = (radius+((1/50)*radius)*radii[index])*sin(dr*index*2*pi)

      cx = radius*cos(dr*index*2*pi)
      cy = radius*sin(dr*index*2*pi)
       
      ax.plot([cx, rx], \
              [cy, ry], \
              lw = bar_width, color = col[index])

      degree = (dr*index*2*pi)*360/(2*pi)

      ha_split = 'right'
      ha_text = 'left'
      degree_split = degree
      degree_freq = degree
      
      if 90 < degree < 270 :

         degree_split = -(180-degree)
         ha_split = 'left'
         
      split = label[index]

      Rx = (radius+((1/50)*radius)*max(radii))*cos(dr*index*2*pi)
      Ry = (radius+((1/50)*radius)*max(radii))*sin(dr*index*2*pi)
      
      text = ax.text(1.5*Rx, 1.5*Ry, split, ha = ha_split, va = 'center', rotation = degree_split, rotation_mode = 'anchor', size = text_size)
      text_freq = ax.text(1.15*rx, 1.15*ry, '('+str(radii[index])+')', ha = 'center', va = 'center', size = 0.8*text_size)
      
      ax.plot([rx, 1.5*Rx], \
              [ry, 1.5*Ry], \
              lw = 0.5, color = 'gray')
      
   ax.set_aspect('equal')

def rbar_B(ax, radii, radius, col, label, bar_width = 5, text_size = 7):

   n = len(radii)
   indexs = range(n)

   x = [-radius+i*0.01 for i in range(2*100*radius + 1)]
   y_upper = [sqrt(radius**2 - i**2) for i in x]
   y_lower = [-y for y in y_upper]

   ax.plot(x, y_upper, color = 'k')
   ax.plot(x, y_lower, color = 'k')

   dr = float(1)/float(n)

   indicator = 1
   
   for index in indexs:

      rx = (radius+((1/50)*radius)*radii[index])*cos(dr*index*2*pi)
      ry = (radius+((1/50)*radius)*radii[index])*sin(dr*index*2*pi)

      ax.plot([radius*cos(dr*indexs[index]*2*pi), rx], \
            [radius*sin(dr*indexs[index]*2*pi), ry], \
               lw = bar_width, color = col[index])

      deg = (float(1)/float(2*pi))*(dr*indexs[index]*2*pi)*360
      lab = label[index]

      if dr*indexs[index]*2*pi >= 0.5*pi and  dr*indexs[index]*2*pi <= 1.5*pi:

         deg = deg + (float(1)/float(2*pi))*pi*360

      if index%2 == 0:

         tx = (radius+radii[index] + (2/10)*radius)*cos(dr*indexs[index]*2*pi)
         ty = (radius+radii[index] + (2/10)*radius)*sin(dr*indexs[index]*2*pi)
  
      else:

         indicator *= -1
         if indicator == 1:

            tx = (radius + (1/20)*radius)*cos(dr*indexs[index]*2*pi)
            ty = (radius + (1/20)*radius)*sin(dr*indexs[index]*2*pi)

         else:

            tx = (radius - (1/10)*radius)*cos(dr*indexs[index]*2*pi)
            ty = (radius - (1/10)*radius)*sin(dr*indexs[index]*2*pi)
   
      ax.text(tx, \
               ty, \
               lab + ' ('+str(radii[index])+')', ha = 'center'\
               #rotation = deg)
                , size = text_size
               )

      ax.plot([tx, rx], [ty, ry], lw = 1)
           
   ax.set_aspect('equal')
