import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.datasets import mnist


# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

image = x_train[0]
image = image.reshape((28, 28))


def max_pooling(image):
    '''Max-Pooling Funktion definieren und auf ein Bild aus dem
    MNIST Dataset anwenden.
    2x2, max
    '''
    return image


pooling_image = max_pooling(image)

print(image.shape)
print(pooling_image.shape)

# Input und Outputbild des Pooling Layers mit imshow() ausgeben
plt.imshow(image, cmap="gray")
plt.show()

plt.imshow(pooling_image, cmap="gray")
plt.show()
