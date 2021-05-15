from .utils import *
from flask import Flask, render_template, request


app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)


@app.route("/", methods=["GET"])
def home(*vargs):
    captions = ["spongebob cannot", "be a service"]
    filename = createMeme(captions)
    return render_template("display.html", meme_image=filename), 200


@app.route("/createMeme", methods=["GET"])
def meme():
    captions = request.args.get('caption')
    captions = captions.split('/')
    filename = createMeme(captions)
    return render_template("display.html", meme_image=filename), 200


if __name__ == "__main__":
    app.run()
