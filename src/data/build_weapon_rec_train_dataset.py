import tensorflow as tf
import image_preprocessing
from tqdm import tqdm
import sqlite3
import json

IMAGE_SIZE = [192, 192]
IMAGES_PATH = './../static/image_data/'
DB_PATH = './../halte.db'


def fetch_labels():
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    labels = cur.execute('SELECT image_id, label FROM image_labels WHERE label_category=\"weapon\" AND user_id=1').fetchall()
    labels = zip(*labels)
    db.close()
    return labels[1]


def main():
    # Get image paths
    image_list = image_preprocessing.get_images_list(images_path=IMAGES_PATH)

    # Create data set - initially of paths
    path_dataset = tf.data.Dataset.from_tensor_slices(image_list)

    # Apply preprocessing function on path dataset via map
    image_dataset = path_dataset.map(image_preprocessing.load_image)#,target_size=IMAGE_SIZE)

    # Fetch string labels
    labels = fetch_labels()
    with open('weapons.json') as weapons_json:
        weapons_dict = json.load(weapons_json)
    print(weapons_dict)

    # index labels


    # create labels Dataset

    # zip datasets together


    return 0

if __name__ == '__main__':
    main()
