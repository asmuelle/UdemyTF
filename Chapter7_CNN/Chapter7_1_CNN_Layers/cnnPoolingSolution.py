import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.datasets import mnist


# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

image = x_train[0]
image = image.reshape((28, 28))


def get_kernel_values(i, j, image):
    '''Max-Pooling Funktion definieren und auf ein Bild aus dem
    MNIST Dataset anwenden.
    '''
    kernel_values = image[i: i + 2, j: j + 2]
    return kernel_values


def max_pooling(image):
    '''Max-Pooling Funktion definieren und auf ein Bild aus dem
    MNIST Dataset anwenden.
    2x2, max
    '''
    # Setup output image as ndarray
    new_rows = image.shape[0] // 2
    new_cols = image.shape[1] // 2
    output = np.zeros(shape=(new_rows, new_cols), dtype=np.float32)
    # Compute the values
    for i in range(new_rows):
        for j in range(new_cols):
            kernel_values = get_kernel_values(2 * i, 2 * j, image)
            max_val = np.max(kernel_values.flatten())
            output[i][j] = max_val
    return output


pooling_image = max_pooling(image)

print(image.shape)
print(pooling_image.shape)

# Input und Outputbild des Pooling Layers mit imshow() ausgeben
plt.imshow(image, cmap="gray")
plt.show()

plt.imshow(pooling_image, cmap="gray")
plt.show()
