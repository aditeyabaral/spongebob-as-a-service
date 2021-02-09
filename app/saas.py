import flask
from .utils import *
from flask import Flask, request, render_template


app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)


@app.route("/", methods=["GET"])
def home(*vargs):
    captions = ["sPoNgEbOb CaNnOt", "Be A sErViCe"]
    filename = generateMeme(captions)
    return render_template("display.html", meme_image=filename), 200


@app.route("/<path:vargs>", methods=["GET"])
def meme(vargs):
    captions = vargs.split('/')
    print(captions)
    captions = convertCaptionsCamelCase(captions)
    print(captions)
    filename = generateMeme(captions)
    return render_template("display.html", meme_image=filename), 200


if __name__ == "__main__":
    app.run()
