import tensorflow as tf
import numpy as np
import pathlib
import os
from sklearn.model_selection import train_test_split

SEED = None
SEED = 42

AUTOTUNE = tf.data.experimental.AUTOTUNE

class DataPipeline(object):
    # Assumes data directory structure: data_path_string/class/sample.jpb

    def __init__(self, data_path_string):
        print('\nInitializing data pipeline')

        print('---------------------------')
        print('Currently using TF {}'.format(tf.__version__))
        print('Eager execution? {}'.format(tf.executing_eagerly()))
        print('---------------------------')

        print('Grabbing images from {}'.format(data_path_string))
        self.data_dir = pathlib.Path(data_path_string)

        self.image_count = len(list(self.data_dir.glob('*/*.jpg')))
        self.class_names = np.array([item.name for item in self.data_dir.glob('*')])
        print('Found {} images in {} classes'.format(self.image_count, len(self.class_names)))

        self.train_list = None
        self.test_list = None


    def split_data(self, train_split=0.8):
        print('Splitting dataset')
        # Grab list of all files
        class_nested_list = []
        for c in self.class_names:
            class_list = list(self.data_dir.glob(c+'/*'))
            class_nested_list.append(class_list)

        train_list, test_list = self._split_nested_lists(class_nested_list, train_split)
        print('Split dataset of {} samples into {} train samples and {} test samples'.format(self.image_count, len(train_list), len(test_list)))

        self.train_list = [str(file_path) for file_path in train_list]
        self.test_list = [str(file_path) for file_path in test_list]

        if (self.image_count != len(self.train_list) + len(self.test_list)):
            print('Data count mismatch; please check')


    def _split_nested_lists(self, nested_list, train_split):
        # split each class list
        train_list = []
        test_list = []
        for sub_list in nested_list:
            sub_train, sub_test = train_test_split(sub_list, train_size=train_split, random_state=SEED)
            train_list = train_list + sub_train
            test_list = test_list + sub_test
        return train_list, test_list


    def load_dataset(self, train=True, IMG_WIDTH=256, IMG_HEIGHT=None):
        print('Loading dataset...')
        self.IMG_WIDTH = IMG_WIDTH
        if IMG_HEIGHT:
            self.IMG_HEIGHT = IMG_HEIGHT
        else:
            self.IMG_HEIGHT = IMG_WIDTH
        print('Will resize images to ({}, {})'.format(self.IMG_WIDTH, self.IMG_HEIGHT))

        if not self.train_list:
            print('Dataset not split into train / test. Please provide split then retry.')
            return None
        else:
            if train:
                print('Loading train dataset.')
                dataset_paths = self.train_list
            else:
                print('Loading test dataset.')
                dataset_paths = self.test_list
            file_list_ds = tf.data.Dataset.from_tensor_slices(dataset_paths)

            print('Mapping preprocessing.')
            labeled_ds = file_list_ds.map(self._process_path, num_parallel_calls=AUTOTUNE)
            return labeled_ds


    def prepare_for_training(self, ds, cache=True, shuffle_buffer_size=1000, batch_size=32):
      # If this is a small dataset, only load it once, and keep it in memory.
      # use `.cache(filename)` to cache preprocessing work for datasets that don't
      # fit in memory.
        if cache:
            if isinstance(cache, str):
                ds = ds.cache(cache)
            else:
                ds = ds.cache()

        ds = ds.shuffle(buffer_size=shuffle_buffer_size)
        # Repeat forever
        ds = ds.repeat()
        ds = ds.batch(batch_size)
        # `prefetch` lets the dataset fetch batches in the background while the model
        # is training.
        ds = ds.prefetch(buffer_size=AUTOTUNE)
        return ds


    def _process_path(self, file_path):
        label = self._get_label(file_path)
        # load the raw data from the file as a string
        img = tf.io.read_file(file_path)
        img = self._decode_img(img)
        return img, label

    def _get_label(self, file_path):
        # convert the path to a list of path components
        parts = tf.strings.split(file_path, os.path.sep)
        # The second to last is the class-directory
        return tf.argmax(tf.cast(parts[-2] == self.class_names, dtype=tf.float32))

    def _decode_img(self, img, channels=3):
        # convert the compressed string to a 3D uint8 tensor
        img = tf.image.decode_jpeg(img, channels=channels)
        # Use `convert_image_dtype` to convert to floats in the [0,1] range.
        img = tf.image.convert_image_dtype(img, tf.float32)
        # resize the image to the desired size.
        return tf.image.resize(img, [self.IMG_WIDTH, self.IMG_HEIGHT])
