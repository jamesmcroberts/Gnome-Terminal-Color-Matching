#!/usr/bin/python2

from PIL import Image
import os
import re
import urllib

# user variables
## the profile for the gnome terminal that you are using
profile = "68776a23-af20-4589-a2b9-6ee6622a8ffc"
## brightness thresholds for the color set by the program
upperBThresh = 200
LowerBThresh = 75

def computeAvgCol(img):
   # gets image dimensions and applies them accordingly
   width, height = img.size
   pixels = img.getcolors(width * height)
   #initialize the avgPix variable
   avgPix = pixels[0]
   pixCount = len(pixels)

   # defines the first pixel according to threshold
   for i in range(0, pixCount):
      avgPix = pixels[i]
      (r, g, b) = avgPix[1][:3]
      # if the color is within the brightness threshold
      #set as the first pixel
      if ((r + g + b) / 3 < upperBThresh) and ((r + g + b) / 3 > LowerBThresh):
         break

   # find the rest of the pixels and if the count is higher
   # and the brightness is okay set it as the new avgPix
   for i, color in pixels:
      (r_t, g_t, b_t) = color[:3]
      avg_t = (r_t + g_t + b_t) / 3
      if ((i > avgPix[0]) and ((avg_t > LowerBThresh) and (avg_t < upperBThresh))):
         avgPix = (i, color[:3])
   # set r g b values
   (r, g, b) = avgPix[1]

   # if the brightness is over a certain point, then take the
   # brightness and invert it
   if ((r + g + b) / 3 > 200):
      rInv = 255 - r
      gInv = 255 - g
      bInv = 255 - b
      ria = ((rInv + gInv + bInv) / 3) + 27
      # set the color (foreground)
      os.system("dconf write /org/gnome/terminal/legacy/profiles:/:" + profile + """/foreground-color "'rgb(""" + str(ria) + "," + str(ria) + "," + str(ria) + """)'" """)
   else:
      # ^^^
      os.system("dconf write /org/gnome/terminal/legacy/profiles:/:" + profile + """/foreground-color "'rgb(255,255,255)'" """)
   return (r, g, b)

#find picture and format its URI
location = os.popen('gsettings get org.gnome.desktop.background picture-uri')
locMod = location.read()
locMod = locMod[8:-2]
locMod = urllib.unquote(locMod)
# open image and optimize
img = Image.open(locMod)
img = img.resize((250,250))
# call average color then write to gnome profile (background)
averageColor = computeAvgCol(img)
averageColor = """ "'rgb """ + str(averageColor) + """ '" """
averageColor = re.sub(' ', '', averageColor)
output = "dconf write /org/gnome/terminal/legacy/profiles:/:" + profile + "/background-color " + averageColor
os.system(output)
