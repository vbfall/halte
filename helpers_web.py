import numpy
import sqlite3
import os

def query_db(db_name, command_string):
    """Receives a sqlite db object, executes a query on it as per command_string and returns results in format of lists - caller must know how many lists will be returned"""
    db = sqlite3.connect(db_name)
    cur = db.cursor()
    cur.execute(command_string)
    results = cur.fetchall()
    db.close()
    return zip(*results)


def list_to_inverse_prob(l):
    """Receives a list of positive values and returns a normalized numpy array with probabilities inverse to the lists values"""
    a = numpy.array(l)
    a = 1 / a
    total = a.sum()
    a = a / total
    return a


def get_image_path(index):
    """Receives a file number without extension and returns the full path to it"""
    path_to_images = '/static/image_data/'
    file_list = os.listdir('.'+path_to_images)
    path = path_to_images + file_list[index]
    return path


def get_form_optional_value(request, field_name):
    try: result = request.form[field_name]
    except: result = ''
    return result

def get_user_info(request):
    user_info = dict()
    user_info['user_name'] = get_form_optional_value(request, 'user_name')
    user_info['nationality'] = get_form_optional_value(request,'nationality')
    user_info['favored_weapon'] = get_form_optional_value(request,'favored_weapon')
    user_info['fencing_since'] = get_form_optional_value(request,'fencing_since')
    user_info['yob'] = get_form_optional_value(request,'yob')
    return user_info
