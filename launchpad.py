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
import sys, pygame, pygame.midi
pygame.init()
size = width, height = 1000, 700
SQUARE_EDGE_LENGTH = 80
PADDING = 20
ENTIRE_CELL = PADDING + SQUARE_EDGE_LENGTH
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
VELOCITY = 64
pygame.midi.init()
def noteOff(pygameInstrument, notesBeenPressed, note, velocity):
	if notesBeenPressed:
		pygameInstrument.note_off(note, velocity)
def main(args):
	for port2 in range(0,pygame.midi.get_count()):
		portInfo = str(pygame.midi.get_device_info(port2)[1])[2:]
		portInfo = portInfo[:len(portInfo) - 1]
		print(str(port2) + ": " +  str(portInfo))
	port = int(input("Enter a number 0 to " + str(port2) + " to select which midi device you want to use: "))
	if not(0 < port < port2):
		port = pygame.midi.get_default_output_id()
	midi_out = pygame.midi.Output(port, 0)
	#0 = grand piano
	midi_out.set_instrument(0)
	redrawNecessary = True
	colorIndex = 0
	notesHaveBeenPressed = False
	previouslyPressed = (width / (PADDING + SQUARE_EDGE_LENGTH), height / (PADDING + SQUARE_EDGE_LENGTH))
	surface = pygame.display.set_mode(size)
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				del midi_out
				pygame.midi.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONUP:
				redrawNecessary = True
		#draw a square
		if pygame.mouse.get_pressed()[0] == True:
				location = (int(pygame.mouse.get_pos()[0] / ENTIRE_CELL), int(pygame.mouse.get_pos()[1] / ENTIRE_CELL))
				if location != previouslyPressed:
					noteOff(midi_out, notesHaveBeenPressed, 30 + 5*previouslyPressed[0] + previouslyPressed[1], VELOCITY)
					previouslyPressed = location
					pygame.draw.rect(surface, COLOR_PALLETE[colorIndex], pygame.Rect(ENTIRE_CELL*location[0], ENTIRE_CELL*location[1], SQUARE_EDGE_LENGTH, SQUARE_EDGE_LENGTH), 0)
					midi_out.note_on(30 + 5*location[0] + location[1], 64)
					notesHaveBeenPressed = True
				colorIndex  = colorIndex + 1
				colorIndex = colorIndex - len(COLOR_PALLETE) * int(colorIndex / len(COLOR_PALLETE))
				pygame.display.update()
				redrawNecessary = False
				
		if redrawNecessary == True:
			noteOff(midi_out, notesHaveBeenPressed, 30 + 5*previouslyPressed[0] + previouslyPressed[1], VELOCITY)
			notesHaveBeenPressed = False
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
