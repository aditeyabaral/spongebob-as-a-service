import flask
from .utils import *
from flask import Flask, request, render_template


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home(*vargs):
    result = 'home page'
    return result, 200


@app.route("/<path:vargs>", methods=["GET"])
def meme(vargs):
    print(vargs)
    captions = vargs.split('/')
    # captions = list(map(convertCaptionsCamelCase, captions))
    print(f"Captions = {captions}")
    filename = generateMeme(captions)
    print(f"meme filename = {filename}")
    return render_template("display.html", image=filename), 200


if __name__ == "__main__":
    app.run()
