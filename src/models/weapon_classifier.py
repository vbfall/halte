
import tensorflow as tf
from tensorflow import keras
# from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import RMSprop

# import foundations

class WeaponClassifierModel(object):

    def __init__(self, input_shape, hyperparameters, num_classes=4):
        print('Registering hyperparameters')
        self.hyper = hyperparameters

        print('Creating keras model...')
        self.model = keras.Sequential()

        print('Adding convolutions and/or flattening...')
        if self.hyper['conv_layers'] > 0:
            self.model.add(keras.layers.Conv2D(self.hyper['conv_filters'][0],
                                            self.hyper['conv_sizes'][0],
                                            activation=self.hyper['conv_activation'],
                                            input_shape=input_shape))
            if self.hyper['pooling']:
                self.model.add(keras.layers.MaxPooling2D((2, 2)))
            for n in range(1, self.hyper['conv_layers']):
                self.model.add(keras.layers.Conv2D(self.hyper['conv_filters'][n],
                                                self.hyper['conv_sizes'][n],
                                                activation=self.hyper['conv_activation']))
                if self.hyper['pooling']:
                    self.model.add(keras.layers.MaxPooling2D((2, 2)))
            self.model.add(keras.layers.Flatten())
        else:
            self.model.add(keras.layers.Flatten(input_shape=input_shape))

        print('Adding dense layers on top...')
        for n in range(0, self.hyper['dense_layers']):
            layer_size = self.hyper['dense_size'][n]
            self.model.add(keras.layers.Dense(layer_size,
                                            activation=self.hyper['dense_activation']))

        print('Final layer...')
        self.model.add(keras.layers.Dense(num_classes, activation='softmax'))

        print(self.model.summary())

    def train(self, train_dataset, opt=0, STEPS_PER_EPOCH=2):

        opt_array = ['adam',
            RMSprop(lr=self.hyper['learning_rate'], decay=self.hyper['decay'])
            ]

        print('Compiling model...')
        self.model.compile(optimizer=opt_array[opt],
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

        # log_dir = '../logs'
        # tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

        print('Training model...')
        self.model.fit(train_dataset,
                    steps_per_epoch=STEPS_PER_EPOCH,
                    epochs=self.hyper['num_epochs'],
                    # callbacks=[tensorboard_callback]
                    )


    def evaluate(self, test_dataset):
        predictions = self.model.predict(test_dataset, steps=1)

        test_loss, test_acc = self.model.evaluate(test_dataset, steps=1, verbose=2)
        print('Accuracy on test dataset: {}'.format(test_acc))
        # foundations.log_metric('Accuracy', float(test_acc))
