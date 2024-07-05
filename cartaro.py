from functools import total_ordering
import os, os.path
import tempfile
import re
from itertools import count
from copy import copy
import textwrap

from PIL import Image, ImageDraw, ImageFont

def memo_last(f):
    cache = {}

    def memf(*x):
        if x not in cache:
            cache.clear()
            cache[x] = f(*x)
            return cache[x]
        return cache[x]

    return memf


@total_ordering
class RichText(dict):
    default_margin_down = 0
    default_margin_up = 3
    default_interspacing = 1
    default_bgcolor = None

    def __init__(self, text):
        self["text"] = text
        self["margin_down"] = self.__class__.default_margin_down
        self["margin_up"] = self.__class__.default_margin_up
        self["interspacing"] = self.__class__.default_interspacing
        self["bgcolor"] = self.__class__.default_bgcolor

    def __getattr__(self, key):
        return self[key]

    def __lt__(self, other):
        return self["text"] < other["text"]


@total_ordering
class BaseCard(object):
    max_width = 30  # 30mm
    max_heigth = 40  # 40mm
    bgcolor = "white"
    borderwidth = 2
    bordercolor = None
    interspacing = 1
    fontsize = 24
    # TODO: support "center all texts"

    def __init__(self):
        pass

    def __mul__(self, integer):
        return [self for i in range(integer)]

    def __lt__(self, other):
        return self.texts < other.texts

    @property
    def texts(self):
        """return a list of rich texts introspecting text\d+ attributes"""
        richtexts = {}
        d = {k: getattr(self, k) for k in dir(self) if k != "texts"}

        text_re = re.compile(r"^text([0-9]+)$")
        for attr in d.keys():
            m = text_re.match(attr)
            if m:
                richtexts[int(m.group(1))] = RichText(getattr(self, m.group(0)))
        text_attr_re = re.compile(r"^text([0-9]+)\_([a-z_]+)$")
        for attr in d.keys():
            m = text_attr_re.match(attr)
            if m:
                richtexts[int(m.group(1))][m.group(2)] = getattr(self, m.group(0))

        listtexts = [None] * (max(richtexts.keys()) + 1)
        for index, value in richtexts.items():
            listtexts[index] = value
        return listtexts

    def post_rendering(self, img, bwidth=0, last=0):
        return img

    def get_font_rich(self, num, rich):
        font = ImageFont.truetype("serif.ttf", rich.size if "size" in rich else self.fontsize)
        return font

    @memo_last
    def create_image(self):
        def mm_to_pixel(mm):
            dpi = 72
            dpcm = dpi / 2.54
            return int(mm * dpcm)

        img = Image.new(
            "RGBA",
            (mm_to_pixel(self.max_width), mm_to_pixel(self.max_heigth)),
            self.bgcolor,
        )

        box = img.getbbox()
        draw = ImageDraw.Draw(img)
        bwidth = 0
        if self.bordercolor is not None:
            bwidth = mm_to_pixel(self.borderwidth)
            draw.rectangle(box, fill=self.bordercolor)
            draw.rectangle((bwidth, bwidth, box[2] - bwidth, box[3] - bwidth), fill="white")
        width = box[2] - 2 * bwidth

        last = bwidth
        for i, rich in enumerate(self.texts, 0):
            if rich is None:
                continue
            rich.update(self.__class__.__dict__)
            rich.update(self.__dict__)
            font = self.get_font_rich(i, rich)
            last += mm_to_pixel(rich.margin_up)
            for subline in _wrap_line(rich.text, width, draw, font):
                w, h = draw.textsize(subline, font=font)
                draw.text(((box[2] - w) / 2, last), subline, fill="black", font=font)
                last = last + h + mm_to_pixel(rich.interspacing)
            last -= mm_to_pixel(rich.interspacing)
            last += mm_to_pixel(rich.margin_down)

        img = self.post_rendering(img, bwidth=bwidth, last=last)

        return img


def create_pdf(l, fname="out.pdf"):
    from fpdf import FPDF

    pdf = FPDF(unit="mm", format="A4", orientation="P")
    pdf.add_page()
    last_x = 0  # mm
    last_y = 0
    for i, card in enumerate(sorted(l), 1):
        img = card.create_image()
        with tempfile.NamedTemporaryFile(suffix=".png") as temp_f:
            img.save(temp_f.name, "PNG", dpi=(72, 72))
            if last_x + card.max_width >= pdf.w:
                last_x = 0
                last_y += card.max_heigth
            if last_y + card.max_heigth >= pdf.h:
                pdf.add_page()
                last_x = 0
                last_y = 0
            pdf.image(temp_f.name, x=last_x, y=last_y, w=card.max_width)
        last_x += card.max_width
    pdf.output("out.pdf")


def create_images(l, directory=".", prefix="card-"):
    if not os.path.exists(directory):
        os.mkdir(directory)
    elif not os.path.isdir(directory):
        raise IOError("not a valid path: %s" % directory)

    for i, card in enumerate(sorted(l), 1):
        img = card.create_image()
        card_prefix = getattr(card, "file_prefix", prefix)
        fname = os.path.join(directory, "%s%03d.png" % (card_prefix, i))
        img.save(fname, "PNG", dpi=(72, 72))


def _wrap_line(text, width, draw, font):
    """Return a list of lines, each one fits in width"""
    words = text.split()
    lines = []
    while words:
        line = []
        while words:
            line.append(words[0])
            w, h = draw.textsize(" ".join(line), font=font)
            if w <= width:
                del words[0]
            else:
                line.pop()
                break
        lines.append(" ".join(line))
    return lines



