from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Following two blocks are for debugging:
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
# End of debugging blocks

@app.route("/")
def index():
    """Shows welcome message"""
    return render_template("index.html")

@app.route("/imagesHelp", methods=["GET", "POST"])
def imagesHelp():
    """Randomly selects an image from database and receives label as input from user"""
    if request.method == "GET":
        #Random selection of an image, biased by current label volume


        #Present image and wait for label
        return render_template("pasdetouche.html")
    else:
        return redirect("/imagesHelp")
    return render_template("pasdetouche.html")

@app.route("/clipsHelp")
def clipsHelp():
    return render_template("pasdetouche.html")

@app.route("/imagesApply")
def imagesApply():
    return render_template("pasdetouche.html")

@app.route("/clipsApply")
def clipsApply():
    return render_template("pasdetouche.html")

@app.route("/thanks")
def thanks():
    return render_template("pasdetouche.html")



if __name__ == '__main__':
   app.run()
