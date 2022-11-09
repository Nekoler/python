import numpy
from PIL import Image

p0 = numpy.array(Image.open(''))
p1 = numpy.array(Image.open(''))
p2 = numpy.array(Image.open(''))
p3 = numpy.array(Image.open(''))
p4 = numpy.array(Image.open(''))
p5 = numpy.array(Image.open(''))
p6 = numpy.array(Image.open(''))
p7 = numpy.array(Image.open(''))
p8 = numpy.array(Image.open(''))
p9 = numpy.array(Image.open(''))
p10 = numpy.array([0]*4*2589).reshape((2589,1,4))
p11 = numpy.array([0]*4*8889).reshape((1,8889,4))

a1 = numpy.hstack((p0,p10,p1,p10,p2,p10,p3,p10,p4))
a2 = numpy.hstack((p5,p10,p6,p10,p7,p10,p8,p10,p9))
a3 = numpy.vstack((a1,p11,a2))

img = Image.fromarray(numpy.uint8(a3))
img.save('')
