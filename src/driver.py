import numpy as np

from data.data_pipeline import DataPipeline
from models.weapon_classifier import WeaponClassifierModel
# import foundations

data_path = '../data/images'
BATCH_SIZE=32

print('#### SET UP DATA PIPELINE ####')
data_pipeline = DataPipeline(data_path)
data_pipeline.split_data()

train_dataset = data_pipeline.load_dataset()
train_dataset = data_pipeline.prepare_for_training(train_dataset, batch_size=BATCH_SIZE)

test_dataset = data_pipeline.load_dataset(train=False)
test_dataset = data_pipeline.prepare_for_training(test_dataset, batch_size=BATCH_SIZE)

STEPS_PER_EPOCH = int(np.ceil(data_pipeline.image_count/BATCH_SIZE))

print('#### INITIALIZE AND TRAIN MODEL ####')
weapon_classifier = WeaponClassifierModel(input_shape=(data_pipeline.IMG_WIDTH, data_pipeline.IMG_HEIGHT,3))
weapon_classifier.train(train_dataset, STEPS_PER_EPOCH=STEPS_PER_EPOCH, epochs=3)

print('#### EVALUATE MODEL ####')
weapon_classifier.evaluate(test_dataset)
