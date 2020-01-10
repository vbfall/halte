import numpy as np

from data.data_pipeline import DataPipeline
from models.weapon_classifier import WeaponClassifierModel
# import foundations

data_path = '../data/images'

hyper_dict={'num_epochs': 2,
    'batch_size': 64,
    'learning_rate': 0.001,
    'conv_layers': 0,
    'conv_activation': 'relu',
    'conv_filters': [32, 64],
    'dense_layers': 2,
    'dense_activation': 'relu',
    'dense_size': [96, 48],
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
weapon_classifier.train(train_dataset, STEPS_PER_EPOCH=STEPS_PER_EPOCH, epochs=hyper_dict['num_epochs'])

print('#### EVALUATE MODEL ####')
weapon_classifier.evaluate(test_dataset)
