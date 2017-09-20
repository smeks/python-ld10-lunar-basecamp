import sys, os, math, random, pygame, OpenGL, ode
from pygame.locals import *
from OpenGL.GL import *

import gl
import texture

# number of fields for each block
INFO_FIELDS = 12
COMMON_FIELDS = 7
PAGE_FIELDS = 2
CHAR_FIELDS = 1

class BMLetter:
	def __init__(self):
		self.u = 0.0
		self.v = 0.0
		self.ue = 0.0
		self.ve = 0.0
		
		self.w = 0.0
		self.h = 0.0
	
		self.lH = 0.0
		
		self.xoff = 0.0
		self.yoff = 0.0
		self.xadv = 0.0
		


class BMFont:
	def draw(self,pos,string):
		glLoadIdentity()
		glTranslatef(pos[0],pos[1],0.0)
		
		self.texture.Bind()
		
		x = 0.0
		y = 0.0
		
		for index in range(0,len(string)):
		
			char = ord(string[index])-32
			
			u = self.letters[char].u
			v = self.letters[char].v
			ue = self.letters[char].ue
			ve = self.letters[char].ve
			
			w = self.letters[char].w
			h = self.letters[char].h
			
			lh = self.letters[char].lH
			
			xoff = self.letters[char].xoff
			yoff = self.letters[char].yoff
			xadv = self.letters[char].xadv
			
			if char == ord(' ')-32:
				x += xadv
				continue
				
			if char == ord('\n')-32:
				y += lh
				x = 0.0
				continue

			
			glBegin(GL_QUADS)
			#glColor4f(1,1,1,1)
			
			glTexCoord2f( u,v )
			glVertex2f( x + xoff, y + yoff)
			
			glTexCoord2f( ue,v )
			glVertex2f( x + xoff + w, y + yoff)
			
			glTexCoord2f( ue,ve )
			glVertex2f( x + xoff + w, y + yoff + h)
			
			glTexCoord2f( u,ve )
			glVertex2f( x + xoff, y + yoff + h)
			
			glEnd()
			
			x += xadv
			
			
	def __init__(self,filename):
		hfile = open(filename,'r')
		infoline = hfile.readline()
		commonline = hfile.readline()
		pageline = hfile.readline()
		charline = hfile.readline()
		
		
		
		self.infofields = []
		self.commonfields = []
		self.pagefields = []
		self.charfields = []
		self.letterfields = []
		self.letters = []
		
		
		
		# -----------------------info block------------------------
		infoline = infoline.split()
		del infoline[0]
		
		for index_key in infoline:
			index = index_key.find('=') + 1			# index to first character/number of the value
			length = len(index_key) - index			# length of the value
			rawkey = index_key[index:index+length]  # copy the value string for cleaning up

			# if there are commas seperating values its a number, split them and convert to number
			if rawkey.find(',') != -1:
				rawkey = rawkey.replace(',', ' ')
				rawkey = rawkey.split()
				for subvalue in rawkey:		# convert each string into number
					subvalue = int(subvalue)
					
				
			# its a string or a single number
			else:
				if rawkey.find('"') != -1:
					rawkey = rawkey.strip('"')
				else:
					rawkey = int(rawkey)

			# we cleaned up the raw key value by now, we need to store it
			self.infofields.append(rawkey)
		
		
		# -----------------------common block------------------------
		commonline = commonline.split()
		del commonline[0]
		
		for index_key in commonline:
			index = index_key.find('=') + 1			# index to first character/number of the value
			length = len(index_key) - index			# length of the value
			rawkey = index_key[index:index+length]  # copy the value string for cleaning up

			# if there are commas seperating values its a number, split them and convert to number
			if rawkey.find(',') != -1:
				rawkey = rawkey.replace(',', ' ')
				rawkey = rawkey.split()
				for subvalue in rawkey:		# convert each string into number
					subvalue = int(subvalue)
					
				
			# its a string or a single number
			else:
				if rawkey.find('"') != -1:
					rawkey = rawkey.strip('"')
				else:
					rawkey = int(rawkey)

			# we cleaned up the raw key value by now, we need to store it
			self.commonfields.append(rawkey)
			
		self.textureWidth = self.commonfields[2]
		self.textureHeight = self.commonfields[3]
			
		#print self.commonfields
		
		# -----------------------page block------------------------
		pageline = pageline.split()
		del pageline[0]
		
		for index_key in pageline:
			index = index_key.find('=') + 1			# index to first character/number of the value
			length = len(index_key) - index			# length of the value
			rawkey = index_key[index:index+length]  # copy the value string for cleaning up

			# if there are commas seperating values its a number, split them and convert to number
			if rawkey.find(',') != -1:
				rawkey = rawkey.replace(',', ' ')
				rawkey = rawkey.split()
				for subvalue in rawkey:		# convert each string into number
					subvalue = int(subvalue)
					
				
			# its a string or a single number
			else:
				if rawkey.find('"') != -1:
					rawkey = rawkey.strip('"')
				else:
					rawkey = int(rawkey)

			# we cleaned up the raw key value by now, we need to store it
			self.pagefields.append(rawkey)
		
		self.textureName = self.pagefields[1]
		
		
		# -----------------------chars block------------------------
		charline = charline.split()
		del charline[0]
		
		for index_key in charline:
			index = index_key.find('=') + 1			# index to first character/number of the value
			length = len(index_key) - index			# length of the value
			rawkey = index_key[index:index+length]  # copy the value string for cleaning up

			# if there are commas seperating values its a number, split them and convert to number
			if rawkey.find(',') != -1:
				rawkey = rawkey.replace(',', ' ')
				rawkey = rawkey.split()
				for subvalue in rawkey:		# convert each string into number
					subvalue = int(subvalue)
					
				
			# its a string or a single number
			else:
				if rawkey.find('"') != -1:
					rawkey = rawkey.strip('"')
				else:
					rawkey = int(rawkey)

			# we cleaned up the raw key value by now, we need to store it
			self.charfields.append(rawkey)
			

		# -----------------------character data/specs------------------------
		
		
		# for each letter
		charcount = self.charfields[0]
		for mainindex in range(0,charcount):
			letterline = hfile.readline()
			letterline = letterline.split()
			del letterline[0]
			
			#print letterline
			
			
			
			# strip everything but the value
			for index_key in letterline:
				index = index_key.find('=') + 1			# index to first character/number of the value
				length = len(index_key) - index			# length of the value
				rawkey = index_key[index:index+length]  # copy the value string for cleaning up
				
				# its already just a number, so convert it and save
				rawkey = int(rawkey)
				
				self.letterfields.append(rawkey)

			
			# now we build the letter spec fields
			templetter = BMLetter()
			
			templetter.u = float(self.letterfields[1]) / float(self.textureWidth)
			templetter.v = float(self.letterfields[2]) / float(self.textureHeight)
			templetter.ue = float(self.letterfields[3]) / float(self.textureWidth) + templetter.u
			templetter.ve = float(self.letterfields[4]) / float(self.textureHeight) + templetter.v
			
			
			templetter.w = self.letterfields[3]
			templetter.h = self.letterfields[4]
			
			templetter.xoff = self.letterfields[5]
			templetter.yoff = self.letterfields[6]
			templetter.xadv = self.letterfields[7]
			
			templetter.lH = self.commonfields[0]
			
			self.letters.append(templetter)
			
			self.letterfields = []
			
		hfile.close()
		

		
		texturepath = 'data/'
		texturepath += self.textureName
		self.texture = texture.Texture( texturepath )
		
	