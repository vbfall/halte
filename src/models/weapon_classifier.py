
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import RMSprop

# import foundations

class WeaponClassifierModel(object):

    def __init__(self, input_shape, hyperparameters, num_classes=4):
        print('Registering hyperparameters')
        self.hyper = hyperparameters
        print('Creating keras model...')

        self.model = keras.Sequential()
        # Add convs
        for n in range(0, self.hyper['conv_layers']):
            x = 1

        # get interface shape
        if self.hyper['conv_layers'] > 0:
            self.model.add(keras.layers.Flatten())
        else:
            self.model.add(keras.layers.Flatten(input_shape=input_shape))

        # add dense layers
        for n in range(0, self.hyper['dense_layers']):
            layer_size = self.hyper['dense_size'][n]
            self.model.add(keras.layers.Dense(layer_size, activation=self.hyper['dense_activation']))

        self.model.add(keras.layers.Dense(num_classes, activation='softmax'))


    def train(self, train_dataset, STEPS_PER_EPOCH=2, epochs=3):

        opt = RMSprop(lr=self.hyper['learning_rate'], decay=self.hyper['decay'])

        print('Compiling model...')
        # self.model.compile(optimizer='adam',
        self.model.compile(optimizer=opt,
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

        print('Training model...')
        self.model.fit(train_dataset, steps_per_epoch=STEPS_PER_EPOCH, epochs=epochs)


    def evaluate(self, test_dataset):
        predictions = self.model.predict(test_dataset, steps=1)

        test_loss, test_acc = self.model.evaluate(test_dataset, steps=1, verbose=2)
        print('Accuracy on test dataset: {}'.format(test_acc))
        # foundations.log_metric('Accuracy', float(test_acc))
