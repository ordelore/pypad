#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  launchpad.py
#  
#  Copyright 2017 ordelore <>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import sys, pygame, pyaudio, math
pygame.init()
PyAudio = pyaudio.PyAudio     #initialize pyaudio

size = width, height = 1500, 800
SQUARE_EDGE_LENGTH = 80
PADDING = 20
ENTIRE_CELL = PADDING + SQUARE_EDGE_LENGTH
surface = pygame.display.set_mode(size)
TUNED_FREQUENCY = 440
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
YELLOW_GREEN = (127, 255, 0)
GREEN = (0, 255, 0)
SLATE_BLUE = (0, 128, 128)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
COLOR_PALLETE = (RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 1, 1024)

def playSound(FREQUENCY, LENGTH):
	#See https://en.wikipedia.org/wiki/Bit_rate#Audio
	BITRATE = 320000     #number of frames per second/frameset.      

	if FREQUENCY > BITRATE:
		BITRATE = int(FREQUENCY)+100
	if BITRATE > 100000:
		BITRATE = 100000
	NUMBEROFFRAMES = int(BITRATE * LENGTH)
	print(NUMBEROFFRAMES)
	print(BITRATE)
	RESTFRAMES = NUMBEROFFRAMES % BITRATE
	WAVEDATA = ''    

	#generating wawes
	for x in range(NUMBEROFFRAMES):
		WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))    
	
	for x in range(RESTFRAMES): 
		WAVEDATA = WAVEDATA+chr(128)
	
	p = PyAudio()
	stream = p.open(format = p.get_format_from_width(1), channels = 1, rate = BITRATE, output = True)
	stream.write(WAVEDATA)
	stream.stop_stream()
	stream.close()
	p.terminate()

def main(args):
	redrawNecessary = True
	colorIndex = 0
	previouslyPressed = (width / (PADDING + SQUARE_EDGE_LENGTH), height / (PADDING + SQUARE_EDGE_LENGTH))
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.mixer.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONUP:
				redrawNecessary = True
		#draw a square
		if pygame.mouse.get_pressed()[0] == True:
				location = (int(pygame.mouse.get_pos()[0] / ENTIRE_CELL), int(pygame.mouse.get_pos()[1] / ENTIRE_CELL))
				if location != previouslyPressed:
					previouslyPressed = location
					pygame.draw.rect(surface, COLOR_PALLETE[colorIndex], pygame.Rect(ENTIRE_CELL*location[0], ENTIRE_CELL*location[1], SQUARE_EDGE_LENGTH, SQUARE_EDGE_LENGTH), 0)
					playSound(TUNED_FREQUENCY * math.pow(1.05946309436,location[1]+11*location[0]), 0.001)
				else:
					playSound(TUNED_FREQUENCY * math.pow(1.05946309436,previouslyPressed[1]+11*previouslyPressed[0]), 0.00001)
				colorIndex  = colorIndex + 1
				colorIndex = colorIndex - len(COLOR_PALLETE) * int(colorIndex / len(COLOR_PALLETE))
				pygame.display.update()
				redrawNecessary = False
				
		if redrawNecessary == True:
			#Draw the squares
			for a in range(0,width,PADDING + SQUARE_EDGE_LENGTH):
				for b in range(0,height,PADDING + SQUARE_EDGE_LENGTH):
					pygame.draw.rect(surface, WHITE, pygame.Rect(a, b, SQUARE_EDGE_LENGTH, SQUARE_EDGE_LENGTH), 0)
			pygame.display.update()
			redrawNecessary = False
	return 0
	
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
    sample_rate = 44100