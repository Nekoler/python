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
p8 = numpy.array([0]*4*2589).reshape((2589,1,4))
p9 = numpy.array([0]*4*7111).reshape((1,7111,4))

a1 = numpy.hstack((p0,p8,p1,p8,p2,p8,p3))
a2 = numpy.hstack((p4,p8,p5,p8,p6,p8,p7))
a3 = numpy.vstack((a1,p9,a2))

img = Image.fromarray(numpy.uint8(a3))
img.save('')
