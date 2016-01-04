#!/usr/bin/python2

from PIL import Image
import os
import re
import urllib

profile = "68776a23-af20-4589-a2b9-6ee6622a8ffc"
upperBThresh = 200
LowerBThresh = 75

def computeAvgCol(img):
   width, height = img.size
   pixels = img.getcolors(width * height)
   avgPix = pixels[0]
   pixCount = len(pixels)

   for i in range(0, pixCount):
      avgPix = pixels[i]
      (r, g, b) = avgPix[1][:3]
      ## old upper limit 235; old lower limit 35
      ### limits now set globally
      if ((r + g + b) / 3 < upperBThresh) and ((r + g + b) / 3 > LowerBThresh):
         break

   for i, color in pixels:
      (r_t, g_t, b_t) = color[:3]
      avg_t = (r_t + g_t + b_t) / 3
      if ((i > avgPix[0]) and ((avg_t > LowerBThresh) and (avg_t < upperBThresh))):
         avgPix = (i, color[:3])
   (r, g, b) = avgPix[1]

   if ((r + g + b) / 3 > 200):
      rInv = 255 - r
      gInv = 255 - g
      bInv = 255 - b
      ria = ((rInv + gInv + bInv) / 3) + 27
      os.system("dconf write /org/gnome/terminal/legacy/profiles:/:" + profile + """/foreground-color "'rgb(""" + str(ria) + "," + str(ria) + "," + str(ria) + """)'" """)
   else:
      os.system("dconf write /org/gnome/terminal/legacy/profiles:/:" + profile + """/foreground-color "'rgb(255,255,255)'" """)
   return (r, g, b)

location = os.popen('gsettings get org.gnome.desktop.background picture-uri')
locMod = location.read()
locMod = locMod[8:-2]
locMod = urllib.unquote(locMod)
img = Image.open(locMod)
img = img.resize((250,250))  # Small optimization
averageColor = computeAvgCol(img)
averageColor = """ "'rgb """ + str(averageColor) + """ '" """
averageColor = re.sub(' ', '', averageColor)
output = "dconf write /org/gnome/terminal/legacy/profiles:/:" + profile + "/background-color " + averageColor
os.system(output)
