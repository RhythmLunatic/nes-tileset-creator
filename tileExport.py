#!/usr/bin/env python3

from PIL.Image import new
import numpy as np
import cv2
import sys
import math

if len(sys.argv) < 2:
    print("You need to specify the image to convert.")
    sys.exit(-1)

palette = []
uniqueTiles = []


#NES only has 56 colors, so instead of keeping all the RGB values
#it's better just to compress images into an indexed palette
#and then decompress them again when it's time to save
def getPaletteNumber(p):
    for n in range(len(palette)):
        rgbPix = palette[n]
        if rgbPix[0]==p[0] and rgbPix[1]==p[1] and rgbPix[2]==p[2]:
            return n
    return -1

img = cv2.imread(sys.argv[-1], cv2.IMREAD_COLOR)
numColumns = int(img.shape[1]/16)
numRows = int(img.shape[0]/16)
print("There are "+str(numColumns*numRows)+" tiles in total.")
print(numColumns,numRows)

def comparePalettedTile(tile1:list,tile2:list)->bool:
    for i in range(len(tile1)):
        if tile1[i]!=tile2[i]:
            return False
    return True

def getImageTileAsPalette(tile)->list:
    imageAsPalette=[]
    for x in range(16):
        for y in range(16):
            pixel = tile[x,y]
            paletteNum = getPaletteNumber(pixel)
            if paletteNum == -1:
                paletteNum=len(palette)
                palette.append(pixel)
            imageAsPalette.append(paletteNum)
    return imageAsPalette

#Convert a paletted tile back to its original form.
def getImageFromPaletteArray(tile:list):
    #print(tile)
    #np.uint8(1,2,3)
    newImg = np.zeros((16,16,3), dtype='uint8')
    #for x in range(16):
    #    for y in range(16):

    #imgTmp = [None]*16*16
    for i in range(len(tile)):
        x = math.floor(i/16)
        y = i%16
        palettedPixel = tile[i]
        newImg[x,y]=palette[palettedPixel]
    #print(imgTmp)

    #return cv2.resize(imgTmp,(16,16))
    #cv2.resize(imgTmp,dsize=(16,16))
    return newImg


print("read image")
for col in range(numColumns):
    for row in range(numRows):
        #print(col,row)
        x = row*16
        y = col*16
        img2 = img[x:x+16,y:y+16]
        newTile = getImageTileAsPalette(img2)
        if len(uniqueTiles)==0:
            uniqueTiles.append(newTile)

        isUnique=True 
        for tile in uniqueTiles:
            if comparePalettedTile(newTile,tile):
                isUnique=False 
                break
        if isUnique:
            uniqueTiles.append(newTile)
        #img2 = img[0:4,0:4]
        #print(img2)
        #cv2.imshow("",img2)
        #cv2.waitKey(0)
        #sys.exit(0)
print("Found "+str(len(uniqueTiles))+" unique tiles.")

#Now we have to save all the tiles.
for i in range(len(uniqueTiles)):
    newImg = getImageFromPaletteArray(uniqueTiles[i])
    cv2.imwrite("out/tile_"+str(i)+".png",newImg)

#print(getImageTileAsPalette(img2))
        #print(pixel)
#print(img2[0,0])
#cv2.imshow("",getImageFromPaletteArray(getImageTileAsPalette(img2)))
#cv2.waitKey(0)
#print('done')
