import mnist
import numpy

test_images = mnist.test_images()
test_labels = mnist.test_labels()

digit_data = [b''] * 10

for i in range(test_images.shape[0]):
    print(i)
    image = test_images[i] > 127
    data = numpy.packbits(image).tobytes('C')
    digit_data[int(test_labels[i])] += data

for digit in range(10):
    f = open('digit_' + str(digit) + '.data', 'wb')
    f.write(digit_data[digit])
    f.close()
