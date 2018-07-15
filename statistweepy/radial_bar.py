# author : Arief Anbiya (anbarief@live.com)
# Algorithm for the radial bar chart.

import numpy
sqrt = numpy.sqrt
cos = numpy.cos
sin = numpy.sin
pi =  numpy.pi
import matplotlib
import matplotlib.pyplot as plt

def rbar(ax, index, radii, radius, col, label, bar_width = 5, textsize = 7):

   x = [-radius+i*0.01 for i in range(2*100*radius + 1)]
   y_upper = [sqrt(radius**2 - i**2) for i in x]
   y_lower = [-y for y in y_upper]

   ax.plot(x, y_upper, color = 'k')
   ax.plot(x, y_lower, color = 'k')

   n = len(index)
   dr = float(1)/float(n)

   indicator = 1
   
   for idx in range(n):
       rx = (radius+radii[idx])*cos(dr*index[idx]*2*pi)
       ry = (radius+radii[idx])*sin(dr*index[idx]*2*pi)
       ax.plot([radius*cos(dr*index[idx]*2*pi), rx], \
            [radius*sin(dr*index[idx]*2*pi), ry], \
               lw = bar_width, color = col[idx])

       deg = (float(1)/float(2*pi))*(dr*index[idx]*2*pi)*360
       lab = label[idx]
       if dr*index[idx]*2*pi >= 0.5*pi and  dr*index[idx]*2*pi <= 1.5*pi:
           deg = deg + (float(1)/float(2*pi))*pi*360

       if idx%2 == 0:
           tx = (radius+radii[idx] + 5)*cos(dr*index[idx]*2*pi)
           ty = (radius+radii[idx] + 5)*sin(dr*index[idx]*2*pi)
           ax.text(tx, \
               ty, \
               lab, weight = 'bold', ha = 'center'\
               , size = textsize
               )
           ax.plot([tx, rx], [ty, ry], lw = 1)
       else:
           indicator *= -1
           if indicator == 1:
               tx = (radius - 5)*cos(dr*index[idx]*2*pi)
               ty = (radius - 5)*sin(dr*index[idx]*2*pi)
           else:
               tx = (radius - 15)*cos(dr*index[idx]*2*pi)
               ty = (radius - 15)*sin(dr*index[idx]*2*pi)
               
           ax.text(tx, \
               ty, \
               lab, weight = 'bold', ha = 'center'\
               #rotation = deg)
                , size = textsize
               )
           ax.plot([tx, rx], [ty, ry], lw = 1)
           
   ax.set_aspect('equal')
