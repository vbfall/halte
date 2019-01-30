import numpy
import sqlite3
import os


def query_db(db_name, command_string):
    """Receives a db name, opens it with sqlite, executes a query on it as per command_string and returns results in format of lists - caller must know how many lists will be returned"""
    db = sqlite3.connect(db_name)
    cur = db.cursor()
    cur.execute(command_string)
    results = cur.fetchall()
    results = zip(*results)
    db.close()
    return results


def insert_into_db(db_name, table_name, row):
    """Receives a db and table name and a row dict, and inserts row into table"""
    # Sample row:
    # row = {'name':'\"THREEPWOOD, G\"', 'nationality':'\"LUC\"', 'fencing_since':'1992', 'fav_weapon':'\"rapier\"', 'birth_year':'1972'}
    # note escaped quotes for string fields and integer fields as simple strings
    db = sqlite3.connect(db_name)
    cur = db.cursor()
    # construct query
    fields = ','.join(list(row.keys()))
    values = ','.join(list(row.values()))
    query = 'INSERT INTO ' + table_name + ' (' + fields + ') VALUES (' + values + ')'
    # Send query to db
    cur.execute(query)
    db.commit()
    db.close()
    return 0


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
