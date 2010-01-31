#! /usr/bin/python
##Amarokcam.py##
#Released under GNU General Public License v2.0 or higher
import pygame
import Image
from pygame.locals import *
import sys
import os
import opencv
#this is important for capturing/displaying images
from opencv import highgui 

camera = highgui.cvCreateCameraCapture(0)
def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    #im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im)
def define_areas(im):
  (x,y)=im.size
  for i in xrange(y):
    im.putpixel(((x/2),i),(0,0,0))
  for j in xrange(x):
    im.putpixel((j,(y/2)),(0,0,0))
  return im
fps = 40.0
pygame.init()
window = pygame.display.set_mode((640,480))
pygame.display.set_caption("Amarok Remote Laser Control")
screen = pygame.display.get_surface()
cumulvara=0
cumulvarb=0
cumulvarc=0
cumulvard=0
threshold=2
while True:
  events = pygame.event.get()
  for event in events:
    if event.type == QUIT or event.type == KEYDOWN:
      sys.exit(0)
  im = get_image()
  (x,y)=im.size
  print cumulvara,cumulvarb,cumulvarc,cumulvard
  for i in xrange(0,x,20):
    for j in xrange(0,y,20):
      (r,b,g)=im.getpixel((i,j))
      if ((r==255)and(b==255)and(g==255)):
	if (i < x/2) and (j < y/2):
	  cumulvara=cumulvara+1
	  cumulvarb=0
	  cumulvarc=0
	  cumulvard=0
	elif (i > x/2) and (j < y/2):
	  cumulvarb=cumulvarb+1
	  cumulvara=0
	  cumulvarc=0
	  cumulvard=0
	elif (i < x/2) and (j > y/2):
	  cumulvarc=cumulvarc+1
	  cumulvarb=0
	  cumulvara=0
	  cumulvard=0
	elif (i > x/2) and (j > y/2):
	  cumulvard=cumulvard+1
	  cumulvarb=0
	  cumulvarc=0
	  cumulvara=0
	if cumulvara==threshold:
	  os.system("dcop amarok player playPause")
	  cumulvara=0
	if cumulvarb==threshold:
	  os.system("dcop amarok player stop")
	  cumulvarb=0
	if cumulvarc==threshold:
	  os.system("dcop amarok player prev")
	  cumulvarc=0
	if cumulvard==threshold:
	  os.system("dcop amarok player next")
	  cumulvard=0
  im=define_areas(im)
  pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
  screen.blit(pg_img, (0,0))
  pygame.display.flip()
  pygame.time.delay(int(1000 * 1.0/fps))
