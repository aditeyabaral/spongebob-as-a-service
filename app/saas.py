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


@app.route("/q", methods=["GET"])
def meme():
    top = request.args.get('top')
    bottom = request.args.get('bottom')
    captions = []
    captions.append(top)
    captions.append(bottom)
    filename = createMeme(captions)
    return render_template("display.html", meme_image=filename), 200


if __name__ == "__main__":
    app.run()
