import flask
from utils import *
from flask import Flask, request, render_template


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home(*vargs):
    captions = ["SpongeBob cannot", "be a Service"]
    filename = generateMeme(captions)
    return render_template("display.html", meme_image=filename), 200


@app.route("/<path:vargs>", methods=["GET"])
def meme(vargs):
    captions = vargs.split('/')
    # captions = list(map(convertCaptionsCamelCase, captions))
    filename = generateMeme(captions)
    print(f"filename = {filename}")
    return render_template("display.html", meme_image=filename), 200


if __name__ == "__main__":
    app.run()
