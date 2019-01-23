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
    """Show welcome message"""
    return render_template("index.html")

@app.route("/imagesHelp")
def imagesHelp():
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




if __name__ == '__main__':
   app.run()
