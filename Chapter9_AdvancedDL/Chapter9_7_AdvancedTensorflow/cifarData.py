from typing import Tuple

import tensorflow as tf


BATCH_SIZE = 128
IMG_SIZE = 160
IMG_DEPTH = 3
IMG_SHAPE = (IMG_SIZE, IMG_SIZE, IMG_DEPTH)
NUM_CLASSES = 10
AUTOTUNE = tf.data.experimental.AUTOTUNE


def build_preprocessing() -> tf.keras.Sequential:
    """Build the preprocessing model, to resize and rescale the images.

    Returns
    -------
    tf.keras.Sequential
        The preprocessing model
    """
    model = tf.keras.Sequential()
    model.add(
        tf.keras.layers.experimental.preprocessing.Resizing(
            height=IMG_SIZE,
            width=IMG_SIZE
        )
    )
    model.add(
        tf.keras.layers.experimental.preprocessing.Rescaling(
            scale=1.0 / 127.5,
            offset=-1.0
        )
    )
    return model


def build_data_augmentation() -> tf.keras.Sequential:
    """Build the data augmentation model, to random rotate,
    zoom and translate the images.

    Returns
    -------
    tf.keras.Sequential
        The preprocessing model
    """
    model = tf.keras.Sequential()
    model.add(
        tf.keras.layers.experimental.preprocessing.RandomRotation(
            factor=0.0625  # 10 pixels
        )
    )
    model.add(
        tf.keras.layers.experimental.preprocessing.RandomZoom(
            height_factor=0.0625,  # 10 pixels
            width_factor=0.0625  # 10 pixels
        )
    )
    model.add(
        tf.keras.layers.experimental.preprocessing.RandomTranslation(
            height_factor=0.0625,  # 10 pixels
            width_factor=0.0625  # 10 pixels
        )
    )
    return model


def prepare_Dataset(
    dataset: tf.data.Dataset,
    shuffle: bool = False,
    augment: bool = False
) -> tf.data.Dataset:
    """Prepare the dataset object with preprocessing and data augmentation.

    Parameters
    ----------
    dataset : tf.data.Dataset
        The dataset object
    shuffle : bool, optional
        Whether to shuffle the dataset, by default False
    augment : bool, optional
        Whether to augment the train dataset, by default False

    Returns
    -------
    tf.data.Dataset
        The prepared dataset
    """
    preprocessing_model = build_preprocessing()
    dataset = dataset.map(
        map_func=lambda x, y: (preprocessing_model(x), y),
        num_parallel_calls=AUTOTUNE
    )

    if shuffle:
        dataset = dataset.shuffle(buffer_size=1_000)

    dataset = dataset.batch(batch_size=BATCH_SIZE)

    if augment:
        data_augmentation_model = build_data_augmentation()
        dataset = dataset.map(
            map_func=lambda x, y: (data_augmentation_model(x), y),
            num_parallel_calls=AUTOTUNE
        )

    return dataset.prefetch(buffer_size=AUTOTUNE)


def get_dataset() -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
    """Generate the train, validation and test set

    Returns
    -------
    Tuple
        (train_dataset, validation_dataset, test_dataset)
    """
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    y_train = tf.keras.utils.to_categorical(
        y=y_train,
        num_classes=NUM_CLASSES
    )
    y_test = tf.keras.utils.to_categorical(
        y=y_test,
        num_classes=NUM_CLASSES
    )

    validation_size = x_train.shape[0] // 5
    train_dataset = tf.data.Dataset.from_tensor_slices(
        tensors=(x_train[:-validation_size], y_train[:-validation_size])
    )
    validation_dataset = tf.data.Dataset.from_tensor_slices(
        tensors=(x_train[-validation_size:], y_train[-validation_size:])
    )
    test_dataset = tf.data.Dataset.from_tensor_slices(
        tensors=(x_test, y_test)
    )

    train_dataset = prepare_Dataset(train_dataset, shuffle=True, augment=True)
    validation_dataset = prepare_Dataset(validation_dataset)
    test_dataset = prepare_Dataset(test_dataset)

    return train_dataset, validation_dataset, test_dataset


if __name__ == "__main__":
    train_dataset, validation_dataset, test_dataset = get_dataset()
