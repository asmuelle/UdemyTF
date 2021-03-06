import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.datasets import mnist
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical


class MNIST:
    def __init__(self):
        # Load the data set
        (self.x_train, self.y_train), (self.x_test, self.y_test) = mnist.load_data()
        # Convert to float32
        self.x_train = self.x_train.astype(np.float32)
        self.y_train = self.y_train.astype(np.float32)
        self.x_test = self.x_test.astype(np.float32)
        self.y_test = self.y_test.astype(np.float32)
        # Reshape the x data to shape (num_examples, width, height, depth)
        self.x_train = np.expand_dims(self.x_train, axis=-1)
        self.x_test = np.expand_dims(self.x_test, axis=-1)
        # Save important data attributes as variables
        self.train_size = self.x_train.shape[0]
        self.test_size = self.x_test.shape[0]
        self.width = self.x_train.shape[1]
        self.height = self.x_train.shape[2]
        self.depth = self.x_train.shape[3]
        self.num_classes = 10
        # Reshape the y data to one hot encoding
        self.y_train = to_categorical(self.y_train, num_classes=self.num_classes)
        self.y_test = to_categorical(self.y_test, num_classes=self.num_classes)
        # Addtional class attributes
        self.scaler = None

    def get_train_set(self):
        return self.x_train, self.y_train

    def get_test_set(self):
        return self.x_test, self.y_test

    def data_augmentation(self, augment_size=5000):
        # Create an instance of the image data generator class
        image_generator = ImageDataGenerator(
            rotation_range=10,
            zoom_range=0.05,
            width_shift_range=0.05,
            height_shift_range=0.05,
            fill_mode='constant',
            cval=0.0,
        )
        # Fit the data generator
        image_generator.fit(self.x_train, augment=True)
        # Get random train images for the data augmentation
        rand_idxs = np.random.randint(self.train_size, size=augment_size)
        x_augmented = self.x_train[rand_idxs].copy()
        y_augmented = self.y_train[rand_idxs].copy()
        x_augmented = image_generator.flow(
            x_augmented, np.zeros(augment_size), batch_size=augment_size, shuffle=False
        ).next()[0]
        # Append the augmented images to the train set
        self.x_train = np.concatenate((self.x_train, x_augmented))
        self.y_train = np.concatenate((self.y_train, y_augmented))
        self.train_size = self.x_train.shape[0]

    def data_preprocessing(self, preprocess_mode="standard"):
        # Preprocess the data
        if preprocess_mode == "standard":
            self.scaler = StandardScaler()
        else:
            self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaler.fit(self.x_train.reshape(self.train_size, 784))
        self.x_train = self.scaler.transform(self.x_train.reshape(self.train_size, 784))
        self.x_test = self.scaler.transform(self.x_test.reshape(self.test_size, 784))
        self.x_train = self.x_train.reshape((self.train_size, self.width, self.height, self.depth))
        self.x_test = self.x_test.reshape((self.test_size, self.width, self.height, self.depth))
