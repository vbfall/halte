from flask import Flask, redirect, render_template, request
import sqlite3
import numpy
from helpers import list_to_inverse_prob

# Configure application
app = Flask(__name__)

# Following two blocks are for debugging:
# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = sqlite3.connect('halte.db')

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response
# End of debugging blocks

@app.route('/')
def index():
    """Shows welcome message"""
    return render_template('index.html')

@app.route('/imagesHelp', methods=['GET', 'POST'])
def imagesHelp():
    """Randomly selects an image from database and receives label as input from user"""
    if request.method == 'GET':
        # get full list of images
        """TODO: current method only gets images that have at least one label"""
        # Counts how many labels each image has
        db_cursor = db.cursor()
        db_cursor.execute('SELECT image_id, COUNT(DISTINCT \"index\") FROM image_labels GROUP BY image_id')
        results = db_cursor.fetchall()
        # turns results into lists (Python's zip is its own inverse)
        # '*' operator passes separated elements of each tuple
        images, counts = zip(*results)
        # turns list of counts into probabilities inversely proportional to current label volume
        probs = list_to_inverse_prob(counts)
        # Selects one image from list respecting probabilities in probs
        selected_image = numpy.random.choice(images,1,probs)[0]

        #Present image and wait for label
        """TODO: make new template and call it passing file name"""
        return render_template('pasdetouche.html')
    else:
        """Receive label from user and enter it into image_labels table"""
        """TODO:"""
        # At the end, select new random image
        return redirect('/imagesHelp')

@app.route('/clipsHelp')
def clipsHelp():
    return render_template('pasdetouche.html')

@app.route('/imagesApply')
def imagesApply():
    return render_template('pasdetouche.html')

@app.route('/clipsApply')
def clipsApply():
    return render_template('pasdetouche.html')

@app.route('/thanks')
def thanks():
    return render_template('pasdetouche.html')



if __name__ == '__main__':
   app.run()
