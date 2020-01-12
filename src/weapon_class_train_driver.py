import numpy as np

from data.data_pipeline import DataPipeline
from models.weapon_classifier import WeaponClassifierModel

import foundations
# foundations.set_tensorboard_logdir('../logs')

data_path = 'c:\\users\\vbfal\\projects\\halte-data\\test' # works on Windows
data_path = '/data/test' # works in F9s - see job.config.yaml

hyper_dict={'num_epochs': 5,
    'batch_size': 128,
    'learning_rate': 0.0001,
    'conv_layers': 2,
    'conv_activation': 'relu',
    'conv_filters': [8, 16],
    'conv_sizes': [(9, 9), (5, 5)],
    'pooling': True,
    'dense_layers': 1,
    'dense_activation': 'relu',
    'dense_size': [32, 16],
    'opt': 0,
    'decay': 1e-6
    }
# hyper_dict = foundations.load_parameters()


print('#### SET UP DATA PIPELINE ####')
data_pipeline = DataPipeline(data_path)
data_pipeline.split_data()

train_dataset = data_pipeline.load_dataset()
train_dataset = data_pipeline.prepare_for_training(train_dataset, batch_size=hyper_dict['batch_size'])

test_dataset = data_pipeline.load_dataset(train=False)
test_dataset = data_pipeline.prepare_for_training(test_dataset, batch_size=hyper_dict['batch_size'])

STEPS_PER_EPOCH = int(np.ceil(data_pipeline.image_count/hyper_dict['batch_size']))

print('#### INITIALIZE AND TRAIN MODEL ####')
weapon_classifier = WeaponClassifierModel(input_shape=(data_pipeline.IMG_WIDTH, data_pipeline.IMG_HEIGHT,3), hyperparameters=hyper_dict, num_classes=len(data_pipeline.class_names))
weapon_classifier.train(train_dataset, STEPS_PER_EPOCH=STEPS_PER_EPOCH)

print('#### EVALUATE MODEL ####')
weapon_classifier.evaluate(test_dataset)
