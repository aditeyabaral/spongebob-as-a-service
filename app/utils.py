import random
import string
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def createMeme(captions):
    captions = convertCaptionsCamelCase(captions)
    try:
        filename = generateImage(captions)
    except ValueError as e:
        print(f"Bad request: {str(e)}")
        filename = handleErrorMeme()
    return filename


def handleErrorMeme():
    caption_choices = [
        ["i know how to", "make memes"],
        ["i can make memes bro"],
        ["i am a professional", "meme maker"],
        ["my meme game", "is strong"],
        ["i know how to", "use saas"]
    ]
    captions = random.choice(caption_choices)
    filename = createMeme(captions)
    return filename


def convertCaptionsCamelCase(captions):
    n_words = [len(caption.split()) for caption in captions]
    text = " ".join(captions).lower()
    new_text = str()
    flag = False
    for ch in text:
        if ch in string.ascii_lowercase:
            if flag:
                new_text += ch.upper()
                flag = False
            else:
                new_text += ch
                flag = True
        else:
            new_text += ch

    new_text = new_text.split()
    new_captions = list()
    pos = 0
    for _, ctr in enumerate(n_words):
        new_captions.append(" ".join(new_text[pos: pos + ctr]))
        pos += ctr
    return new_captions


def generateImage(captions):
    num_captions = len(captions)
    meme_format = dict()

    if num_captions == 1:
        meme_format["bottom"] = captions[0]
    elif num_captions == 2:
        meme_format["top"] = captions[0]
        meme_format["bottom"] = captions[1]
    else:
        raise ValueError("Incorrect number of captions")

    img = Image.open("app/static/template.jpg")
    for position, caption in list(meme_format.items()):
        addText(img, position, caption)

    filename = "-".join(captions)+".jpg"
    filename = filename.replace(' ', '-')
    img.save("app/static/"+filename)
    img.close()
    return filename


def addText(img, pos, msg):
    fontSize = 56
    lines = []

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("app/impact.ttf", fontSize)
    w, h = draw.textsize(msg, font)

    imgwithpadding = img.width * 0.99

    # 1. how many lines for the msg to fit ?
    line_C = 1
    if(w > imgwithpadding):
        line_C = int(round((w / imgwithpadding) + 1))

    if line_C > 2:
        while 1:
            fontSize -= 2
            fnopen = open("app/impact.ttf", "rb")
            font = ImageFont.truetype(fnopen, fontSize)
            w, h = draw.textsize(msg, font)
            line_C = int(round((w / imgwithpadding) + 1))
            #print("try again with fontSize={} => {}".format(fontSize, line_C))
            if line_C < 3 or fontSize < 10:
                break

    #print("img.width: {}, text width: {}".format(img.width, w))
    #print("Text length: {}".format(len(msg)))
    #print("Lines: {}".format(line_C))

    # 2. divide text in X lines
    lastCut = 0
    isLast = False
    for i in range(0, line_C):
        if lastCut == 0:
            cut = (len(msg) / line_C) * i
        else:
            cut = lastCut

        if i < line_C-1:
            nextCut = (len(msg) / line_C) * (i+1)
        else:
            nextCut = len(msg)
            isLast = True

        cut = int(cut)
        nextCut = int(nextCut)
        #print("cut: {} -> {}".format(cut, nextCut))

        # make sure we don't cut words in half
        if nextCut == len(msg) or msg[nextCut] == " ":
            print("may cut")
        else:
            print("may not cut")
            while msg[nextCut] != " ":
                nextCut += 1
            print("new cut: {}".format(nextCut))

        line = msg[cut:nextCut].strip()

        # is line still fitting ?
        w, h = draw.textsize(line, font)
        if not isLast and w > imgwithpadding:
            print("overshot")
            nextCut -= 1
            while msg[nextCut] != " ":
                nextCut -= 1
            print("new cut: {}".format(nextCut))

        lastCut = nextCut
        lines.append(msg[cut:nextCut].strip())

    # 3. print each line centered
    lastY = -h
    if pos == "bottom":
        lastY = img.height - h * (line_C+1) - 10

    for i in range(0, line_C):
        w, h = draw.textsize(lines[i], font)
        textX = img.width/2 - w/2
        # if pos == "top":
        #    textY = h * i
        # else:
        #    textY = img.height - h * i
        textY = lastY + h
        draw.text((textX-2, textY-2), lines[i], (0, 0, 0), font=font)
        draw.text((textX+2, textY-2), lines[i], (0, 0, 0), font=font)
        draw.text((textX+2, textY+2), lines[i], (0, 0, 0), font=font)
        draw.text((textX-2, textY+2), lines[i], (0, 0, 0), font=font)
        draw.text((textX, textY), lines[i], (255, 255, 255), font=font)
        lastY = textY
