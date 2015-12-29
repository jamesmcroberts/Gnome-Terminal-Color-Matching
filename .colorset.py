#!/usr/bin/python2

from PIL import Image
import os
import re
import urllib

profile = "68776a23-af20-4589-a2b9-6ee6622a8ffc"

def compute_average_image_color(img):
   width, height = img.size
   pixels = img.getcolors(width * height)
   avg_pix = pixels[0]
   [r, g, b] = avg_pix[1][:3]
   if (r + g + b) / 3 >= 235:
      avg_pix = pixels[1]
   ## print(avg_pix) # for debugging purposes
   for i, color in pixels:
      (r_t, g_t, b_t) = color[:3]
      avg_t = (r_t + g_t + b_t) / 3
      if ((i > avg_pix[0]) and ((avg_t > 30) and (avg_t < 235))):
         avg_pix = (i, color[:3])
         ## print(color) # for debugging purposes
   (count, (r, g, b)) = avg_pix
   if ((r + g + b) / 3 > 200):
      r_inv = 255 - r
      g_inv = 255 - g
      b_inv = 255 - b
      ria = ((r_inv + g_inv + b_inv) / 3) + 27
      os.system("dconf write /org/gnome/terminal/legacy/profiles:/:" + profile + """/foreground-color "'rgb(""" + str(ria) + "," + str(ria) + "," + str(ria) + """)'" """)
   else:
      os.system("dconf write /org/gnome/terminal/legacy/profiles:/:" + profile + """/foreground-color "'rgb(255,255,255)'" """)
   return (r, g, b)
location = os.popen('gsettings get org.gnome.desktop.background picture-uri')
loc_mod = location.read()
loc_mod = loc_mod[8:-2]
loc_mod = urllib.unquote(loc_mod)
img = Image.open(loc_mod)
img = img.resize((250,250))  # Small optimization
average_color = compute_average_image_color(img)
average_color = """ "'rgb """ + str(average_color) + """ '" """
average_color = re.sub(' ', '', average_color)
output = "dconf write /org/gnome/terminal/legacy/profiles:/:" + profile + "/background-color " + average_color
os.system(output)
