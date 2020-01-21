import tensorflow as tf

import src.models.pix2pix as pix2pix # U-Net upsampler is based on Google pix2pix model


class PersonFinder(object):
    # Defines a U-Net architecture model for image segmentation

    def __init__(self, hyperparameters):
        print('Registering hyperparameters')
        self.hyper = hyperparameters

        print('Creating keras model...')
        self.model = self.unet_model()

        self.model.compile(optimizer='adam',
                        loss='sparse_categorical_crossentropy',
                        metrics=['accuracy'])

        tf.keras.utils.plot_model(self.model, show_shapes=True)

        print(self.model.summary())



    def down_stack(self):
        print("Setting up down sampling stack")
        base_model = tf.keras.applications.MobileNetV2(
                    input_shape=self.hyper.get('input_shape', [128, 128, 3]),
                    include_top=False)

        print("Picking layers to activate")
        layer_names = [
            'block_1_expand_relu',  # 64x64
            'block_3_expand_relu',  # 32x32
            'block_6_expand_relu',  # 16x16
            'block_13_expand_relu', # 8x8
            'block_16_project',     # 4x4
        ]
        layers = [base_model.get_layer(name).output for name in layer_names]

        print("Creating pre-trained feature extraction model")
        down_stack = tf.keras.Model(inputs=base_model.input, outputs=layers)
        print("Fixing weights")
        down_stack.trainable = False

        return down_stack


    def up_stack(self):
        print("Setting up up sampling stack")
        up_stack = [pix2pix.upsample(512, 3),  # 4x4 -> 8x8
                    pix2pix.upsample(256, 3),  # 8x8 -> 16x16
                    pix2pix.upsample(128, 3),  # 16x16 -> 32x32
                    pix2pix.upsample(64, 3),   # 32x32 -> 64x64
                    ]
        return up_stack


    def unet_model(self):

        print("Setting up input layer")
        inputs = tf.keras.layers.Input(shape=self.hyper.get('input_shape', [128, 128, 3]))
        x = inputs

        down_sample = self.down_stack()

        print("Assembling down sampling and setting up skip connections")
        skips = down_sample(x)
        x = skips[-1]
        skips = reversed(skips[:-1])

        up_sample = self.up_stack()

        print("Assembling up sampling and skip connections")
        # Upsampling and establishing the skip connections
        for up, skip in zip(up_sample, skips):
            x = up(x)
            concat = tf.keras.layers.Concatenate()
            x = concat([x, skip])

        print("Setting up final output layer")
        last = tf.keras.layers.Conv2DTranspose(
            self.hyper.get('output_channels', 3),
            3, strides=2, padding='same', activation='softmax'
            )  # 64x64 -> 128x128

        x = last(x)

        return tf.keras.Model(inputs=inputs, outputs=x)
