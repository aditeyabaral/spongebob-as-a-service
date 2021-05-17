from .utils import createMeme
from flask import Flask, render_template, request


app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/", methods=["GET"])
def home(*vargs):
    captions = {
        "top": "spongebob cannot",
        "bottom": "be a service"
    }
    filename = createMeme(captions)
    return render_template("display.html", meme_image=filename), 200


@app.route("/<path:vargs>", methods=["GET"])
def meme(vargs):
    captions = vargs.split('/')
    if len(captions) == 2:
        captions = {
            "top": captions[0],
            "bottom": captions[1]
        }
    else:
        captions = {
            "top": "",
            "bottom": captions[0]
        }

    filename = createMeme(captions)
    return render_template("display.html", meme_image=filename), 200


@app.route("/q", methods=["GET"])
def memeParameters():

    top = request.args.get('top', default="")
    bottom = request.args.get('bottom', default="")
    captions = {
        'top': top,
        'bottom': bottom
    }
    filename = createMeme(captions)
    return render_template("display.html", meme_image=filename), 200


if __name__ == "__main__":
    app.run()
