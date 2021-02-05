import flask
import utils
from flask import Flask, request, render_template


app = Flask(__name__)


def errorMeme():
    return "", 200


@app.route("/", methods=["GET"])
def home():
    result = 'home page'
    return result, 200


@app.route("/<path:vargs>", methods=["GET"])
def meme(vargs):
    captions = vargs.split('/')
    num_captions = len(captions)
    if 1 <= num_captions <= 2:
        utils.generateMeme(captions)
    else:
        errorMeme()

    result = "-".join(captions)
    return result, 200


if __name__ == "__main__":
    app.run()
