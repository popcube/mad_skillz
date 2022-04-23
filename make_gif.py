from PIL import Image
import os
import datetime

def today():
    return datetime.datetime.now().strftime("%Y%m%d")

f_list = os.listdir("./figs")
images = []

for fn in f_list:
    if fn.endswith(".png"):
        images.append(Image.open("./figs/" + fn))

images[0].save(today() + ".gif",
    save_all=True,
    append_images=images[1:],
    duration=500)