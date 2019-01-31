import tensorflow as tf
import image_preprocessing
from tqdm import tqdm
import sqlite3

IMAGE_SIZE = [192, 192]
IMAGES_PATH = './../static/image_data/'

def main():
    # Get image paths
    image_list = image_preprocessing.get_images_list(images_path=IMAGES_PATH)

    # Create data set - initially of paths
    path_dataset = tf.data.Dataset.from_tensor_slices(image_list)

    # Apply preprocessing function on path dataset via map
    image_dataset = path_dataset.map(image_preprocessing.load_image(target_size=IMAGE_SIZE), num_parallel_calls=AUTOTUNE)

    # Fetch labels



    return 0

if __name__ == '__main__':
    main()
