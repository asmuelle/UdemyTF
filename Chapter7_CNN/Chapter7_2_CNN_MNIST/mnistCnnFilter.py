import os
import time

import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import MaxPool2D
from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical


# Dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Cast to np.float32
x_train = x_train.astype(np.float32)
y_train = y_train.astype(np.float32)
x_test = x_test.astype(np.float32)
y_test = y_test.astype(np.float32)

# Reshape the images to a depth dimension
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)

# Dataset variables
train_size = x_train.shape[0]
test_size = x_test.shape[0]
width, height, depth = x_train.shape[1:]
num_features = width * height * depth
num_classes = 10

# Compute the categorical classes_list
y_train = to_categorical(y_train, num_classes=num_classes)
y_test = to_categorical(y_test, num_classes=num_classes)

# Save Path
dir_path = os.path.abspath("C:/Users/Jan/Dropbox/_Programmieren/UdemyTF/models/")
if not os.path.exists(dir_path):
    os.mkdir(dir_path)
mnist_model_path = os.path.join(dir_path, "mnist_model.h5")
# Log Dir
log_dir = os.path.abspath("C:/Users/Jan/Dropbox/_Programmieren/UdemyTF/logs/")
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
model_log_dir = os.path.join(log_dir, "model3")

# Model params
lr = 0.001
optimizer = Adam(lr=lr)
epochs = 10
batch_size = 256

# Define the DNN
input_img = Input(shape=x_train.shape[1:])

x = Conv2D(filters=32, kernel_size=5, padding='same')(input_img)
x = Activation("relu")(x)
x = Conv2D(filters=32, kernel_size=5, padding='same')(x)
x = Activation("relu")(x)
x = MaxPool2D()(x)

x = Conv2D(filters=64, kernel_size=5, padding='same')(x)
x = Activation("relu")(x)
x = Conv2D(filters=64, kernel_size=5, padding='same')(x)
x = Activation("relu")(x)
x = MaxPool2D()(x)

x = Flatten()(x)
x = Dense(units=128)(x)
x = Activation("relu")(x)
x = Dense(units=num_classes)(x)
y_pred = Activation("softmax")(x)

# Build the model
model = Model(inputs=[input_img], outputs=[y_pred])

# Compile and train (fit) the model, afterwards evaluate the model
model.summary()

model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])
model.fit(
    x=x_train,
    y=y_train,
    epochs=epochs,
    batch_size=batch_size,
    validation_data=(x_test, y_test),
)

score = model.evaluate(x_test, y_test, verbose=0)
print("Score: ", score)

# Kernels (Filter) weights
kernels = model.layers[1].get_weights()[0]
print(kernels.shape)

num_filters = kernels.shape[3]
subplot_grid = (num_filters // 4, 4)

fig, ax = plt.subplots(subplot_grid[0], subplot_grid[1], figsize=(20, 20))
ax = ax.reshape(num_filters)

for curr_filter_idx in range(num_filters):
    ax[curr_filter_idx].imshow(kernels[:, :, 0, curr_filter_idx], cmap="gray")

ax = ax.reshape(subplot_grid)
fig.subplots_adjust(hspace=0.5)
plt.show()
