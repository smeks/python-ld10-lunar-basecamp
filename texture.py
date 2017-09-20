import sys, os, math, random, pygame, OpenGL, ode
from pygame.locals import *
from OpenGL.GL import *

class Texture:
	def __init__(self,filename):
		surface = pygame.image.load(filename)
		image = pygame.image.tostring(surface, 'RGBA', 0)
		width = surface.get_width()
		height = surface.get_height()
		
		#self.textureId = 0
		self.textureId = glGenTextures(1)
	
		glBindTexture(GL_TEXTURE_2D, self.textureId)
		glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)

	def Bind(self):
		#glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.textureId)
		
	def UnBind(self):
		#glDisable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, 0)
		
