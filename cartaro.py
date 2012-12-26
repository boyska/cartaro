import os, os.path
import re
from itertools import izip, count
from copy import copy
import textwrap

from PIL import Image, ImageDraw, ImageFont

class RichText(dict):
    default_margin_down = 0
    default_margin_up = 3
    default_interspacing = 1
    default_bgcolor = None
    def __init__(self, text):
        self['text'] = text
        self['margin_down'] = self.__class__.default_margin_down
        self['margin_up'] = self.__class__.default_margin_up
        self['interspacing'] = self.__class__.default_interspacing
        self['bgcolor'] = self.__class__.default_bgcolor

    def __getattr__(self, key):
        return self[key]

class BaseCard(object):
    max_width=30 #30mm
    max_heigth=40 #40mm
    bgcolor='white'
    borderwidth=2
    bordercolor=None
    interspacing=1
    fontsize=24
    def __init__(self):
        pass
    def __mul__(self, integer):
        return [self for i in xrange(integer)]
#TODO: make it a property
    def get_texts(self):
        '''return a list of rich texts introspecting text\d+ attributes'''
        richtexts = {}
        d = {k: getattr(self, k) for k in dir(self)}

        text_re=re.compile(r'^text([0-9]+)$')
        for attr in d.keys():
            m = text_re.match(attr)
            if m:
                richtexts[int(m.group(1))] = RichText(getattr(self, m.group(0)))
        text_attr_re=re.compile(r'^text([0-9]+)\_([a-z_]+)$')
        for attr in d.keys():
            m = text_attr_re.match(attr)
            if m:
                richtexts[int(m.group(1))][m.group(2)] = getattr(self, m.group(0))
        
        listtexts=[None]*(max(richtexts.keys()) + 1)
        for index, value in richtexts.items():
            listtexts[index] = value
        return listtexts

def create_images(l, directory='.'):
    if not os.path.exists(directory):
        os.mkdir(directory)
    elif not os.path.isdir(directory):
        raise IOError('not a valid path: %s' % directory)
    for card, i in zip(sorted(l), count(1)):
        img = create_image(card)
        img.save(os.path.join(directory, 'card-%03d.jpeg' % i), 'JPEG', dpi=(72,72))

def _wrap_line(text, width, draw, font):
    '''Return a list of lines, each one fits in width'''
    words = text.split()
    lines = []
    while words:
        line = []
        while words:
            line.append(words[0])
            w,h = draw.textsize(' '.join(line), font=font)
            if w <= width:
                del words[0]
            else:
                line.pop()
                break
        lines.append(' '.join(line))
    return lines


def memo_last(f):
    cache= {}
    def memf(*x):
        if x not in cache:
            cache.clear()
            cache[x] = f(*x)
            return cache[x]
        return cache[x]
    return memf

@memo_last
def create_image(card):
    def mm_to_pixel(mm):
        dpi = 72
        dpcm = dpi/2.54
        return int(mm*dpcm)

    img = Image.new('RGBA',
            (mm_to_pixel(card.max_width), mm_to_pixel(card.max_heigth)),
            card.bgcolor)

    box = img.getbbox()
    draw = ImageDraw.Draw(img)
    bwidth=0
    if card.bordercolor is not None:
        bwidth = mm_to_pixel(card.borderwidth)
        draw.rectangle(box, fill=card.bordercolor)
        draw.rectangle((bwidth,bwidth,box[2]-bwidth,box[3]-bwidth),
                fill='white')
    width = box[2]-2*bwidth

    size = card.fontsize
    last = bwidth
    for rich in card.get_texts():
        if rich is None:
            continue
        rich.update(card.__class__.__dict__)
        rich.update(card.__dict__)
        font = ImageFont.truetype('serif.ttf',
                rich.size if 'size' in rich else size)
        last += mm_to_pixel(rich.margin_up)
        for subline in _wrap_line(rich.text, width, draw, font):
            w,h = draw.textsize(subline, font=font)
            draw.text(((box[2]-w)/2, last),
                    subline, fill='black', font=font)
            last = last+h+mm_to_pixel(rich.interspacing)
        last -= mm_to_pixel(rich.interspacing)
        last += mm_to_pixel(rich.margin_down)


    return img


