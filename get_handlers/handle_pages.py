from flask import render_template

def handleIndex():
    """
    Handles when user acces root url.
    """
    return render_template("index.html") 
