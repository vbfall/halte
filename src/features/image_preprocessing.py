import tensorflow as tf
import os


def get_images_list(images_path = './data/images/'):
    """Return list of paths to files within provided path"""
    image_list = sorted([images_path + image for image in os.listdir(images_path)])
    return image_list


def decode_according_to_extension(img_raw,extension='.jpg'):
    if (extension=='.jpg') or (extension=='.jpeg'):
        return tf.image.decode_jpeg(img_raw, channels=3)
    elif (extension=='.png'):
        return tf.image.decode_png(img_raw)
    elif (extension=='.gif'):
        return tf.image.decode_gif(img_raw)
    else:
        return None


def load_image(image_path, target_size=[256,256]):
    """Loads, decodes and resizes an image with tensorflow"""
    img_raw = tf.read_file(image_path)
    extension=image_path[-4:].lower()
    img_tensor = decode_according_to_extension(img_raw,extension)
    img_resized = tf.image.resize_images(img_tensor, target_size)
    img_final = img_resized / 255.0
    return img_final
