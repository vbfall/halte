
import os
os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'

import copy
import foundations
import numpy as np
import yaml

class SearchSpace:

    def __init__(self, min, max, type):
        self.min = min
        self.max = max
        self.type = type

    def sample(self):
        if self.type == int:
            return np.random.randint(self.min, self.max)
        elif self.type == float:
            return round(np.random.uniform(self.min, self.max), 7)


def sample_hyperparameters(hyperparameter_ranges):
    hyperparameters = copy.deepcopy(hyperparameter_ranges)
    for hparam in hyperparameter_ranges:
        if isinstance(hyperparameter_ranges[hparam], SearchSpace):
            search_space = hyperparameter_ranges[hparam]
            hyperparameters[hparam] = search_space.sample()
    return hyperparameters


with open('./src/config/weapon_classifier.config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


hyperparameter_ranges={
    'num_epochs': 10,
    'batch_size': SearchSpace(16, 256, int),
    'learning_rate': SearchSpace(1e-5, 1e-2, float),
    'conv_layers': SearchSpace(0, 3, int),
    'conv_activation': 'relu',
    'conv_filters': [4, 8, 16],
    'conv_sizes': [(9, 9), (5, 5), (3, 3)],
    'pooling': SearchSpace(0, 1, int),
    'dense_layers': SearchSpace(0, 3, int),
    'dense_activation': 'relu',
    'dense_size': [64, 32, 16],
    'opt': SearchSpace(0, 1, int),
    'decay': SearchSpace(1e-7, 1e-5, float),
    }


for _ in range(config.get('model_search',{}).get('num_jobs')):
    hyperparameters = sample_hyperparameters(hyperparameter_ranges)
    foundations.submit(scheduler_config='scheduler',
                    command='src/weapon_class_train_driver.py',
                    params=hyperparameters)
