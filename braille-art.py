#!/usr/bin/python3

from PIL import Image
import random
import argparse

parser = argparse.ArgumentParser(description='Takes an image and turns it in to braille characters')

parser.add_argument('--invert', action='store_true')
parser.add_argument('filename', help='the file that will be converted')

args = parser.parse_args()


average = lambda x: sum(x)/len(x) if len(x) > 0 else 0
start = 0x2800
char_width = 10
char_height = char_width * 2
dither = 10
sensitivity = 0.8
char_width_divided = round(char_width / 2)
char_height_divided = round(char_height / 4)
output_buffer = ""


base = Image.open(args.filename)
match = lambda a, b: a < b if args.invert else a > b
def image_average(x1, y1, x2, y2):
    return average([average(base.getpixel((x, y))[:3]) for x in range(x1, x2) for y in range(y1, y2)])
def convert_index(x):
    return {3: 6, 4: 3, 5: 4, 6: 5}.get(x, x)
for y in range(0, base.height - char_height - 1, char_height): #line
    for x in range(0, base.width - char_width - 1, char_width): #column
        byte = 0x0
        index = 0
        for xn in range(2):
            for yn in range(4):
                avg = image_average(x + (char_height_divided * xn), y + (char_width_divided * yn), x + (char_height_divided * (xn + 1)), y + (char_width_divided * (yn + 1)))
                if match(avg + random.randint(-dither, dither), sensitivity * 0xFF):
                    byte += 2**convert_index(index)
                index += 1
        #print(chr(start + byte), end = "")
        output_buffer = output_buffer + chr(start+byte)
    #print()
    output_buffer = output_buffer + "\n"
    
print(output_buffer)
