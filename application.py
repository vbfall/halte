from flask import Flask, redirect, render_template, request
import sqlite3
import numpy
from helpers_web import list_to_inverse_prob, query_db, get_image_path, get_user_info

# Configure application
app = Flask(__name__)

# Following two blocks are for debugging:
# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

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
        # Counts how many labels each image has (function returns results in lists)
        images, counts = query_db('halte.db','SELECT image_id, COUNT(DISTINCT \"index\") FROM image_labels GROUP BY image_id')
        # turns list of counts into probabilities inversely proportional to current label volume
        probs = list_to_inverse_prob(counts)
        # Selects one image from list respecting probabilities in probs
        selected_image = numpy.random.choice(images,1,p=probs)[0]
        image_path = get_image_path(selected_image)

        #Present image and wait for label
        """TODO: make new template and call it passing file name"""
        return render_template('imageHelp.html',image_path=image_path,image_id=selected_image)
    else:
        # If route called from 'skip' button redirect to GET method
        if request.form['label']=='skip':
            return redirect('/imagesHelp')

        # Get user info
        user_info = get_user_info(request)

        # Save user to db
        # Fetch user_id

        # Get label and image id
        label = request.form['label']
        image_id = request.form['image_id']

        # Save label to db
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
    return render_template('thanks.html')



if __name__ == '__main__':
   app.run()
