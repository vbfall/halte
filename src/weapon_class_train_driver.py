import numpy as np
import yaml

from data.data_pipeline import ClassificationDataPipeline
from models.weapon_classifier import WeaponClassifierModel

with open('./src/config/weapon_classifier.config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

hyper_dict = config.get('hyperparameters')

print('#### SET UP DATA PIPELINE ####')
data_pipeline = ClassificationDataPipeline(config.get('data_path'))
data_pipeline.split_data()

train_dataset = data_pipeline.load_dataset()
train_dataset = data_pipeline.prepare_for_training(train_dataset,
                                                    batch_size=hyper_dict['batch_size'])

test_dataset = data_pipeline.load_dataset(test=True)
test_dataset = data_pipeline.prepare_for_training(test_dataset,
                                                    batch_size=hyper_dict['batch_size'])

STEPS_PER_EPOCH = int(np.ceil(data_pipeline.image_count/hyper_dict['batch_size']))

print('#### INITIALIZE AND TRAIN MODEL ####')
weapon_classifier = WeaponClassifierModel(input_shape=(data_pipeline.IMG_WIDTH, data_pipeline.IMG_HEIGHT,3),
                                            hyperparameters=hyper_dict,
                                            num_classes=len(data_pipeline.class_names))
weapon_classifier.train(train_dataset, STEPS_PER_EPOCH=STEPS_PER_EPOCH)

print('#### EVALUATE MODEL ####')
weapon_classifier.evaluate(test_dataset)
