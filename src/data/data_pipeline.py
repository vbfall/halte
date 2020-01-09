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

        # split each class list
        train_list = []
        test_list = []
        for class_list in class_nested_list:
            class_train, class_test = train_test_split(class_list, train_size=train_split, random_state=SEED)
            train_list = train_list + class_train
            test_list = test_list + class_test

        # extract strings from paths (TF requires strings)
        train_list = [str(file_path) for file_path in train_list]
        test_list = [str(file_path) for file_path in test_list]
        print('Split dataset of {} samples into {} train samples and {} test samples'.format(self.image_count, len(train_list), len(test_list)))

        if (self.image_count == len(train_list) + len(test_list)):
            self.train_list = train_list
            self.test_list = test_list
            print('Train and test lists set')
        else:
            print('Data count mismatch; train and test lists not set')


    def load_dataset(self, dataset_paths=None, IMG_WIDTH=256, IMG_HEIGHT=None):
        print('Loading dataset...')
        self.IMG_WIDTH = IMG_WIDTH
        if IMG_HEIGHT:
            self.IMG_HEIGHT = IMG_HEIGHT
        else:
            self.IMG_HEIGHT = IMG_WIDTH
        print('Will resize images to ({}, {})'.format(self.IMG_WIDTH, self.IMG_HEIGHT))

        if not dataset_paths:
            print('Dataset not specified, will use train list as default.')
            dataset_paths = self.train_list

        if dataset_paths:
            print('Loading paths.')
            file_list_ds = tf.data.Dataset.from_tensor_slices(dataset_paths)
            print('Mapping preprocessing.')
            labeled_ds = file_list_ds.map(self._process_path, num_parallel_calls=AUTOTUNE)
            return labeled_ds
        else:
            print('Dataset not split into train / test. Please specify dataset to load or provide split.')
            return None


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
