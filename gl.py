import sys
from OpenGL.GL import *
import math

class gf2DVert:
	def __init__(self, x=None, y=None, u=None, v=None ):
		self.x=x
		self.y=y
		self.y=u
		self.v=v

class gfRect:
	def __init__(self, left=None, top=None, right=None, bottom=None ):
		self.left=left
		self.top=top
		self.right=right
		self.bottom=bottom

	


def ResizeView(width,height):
	glViewport( 0, 0, width, height )
	
	glMatrixMode( GL_PROJECTION )
	glLoadIdentity()
	glOrtho( 0, width, height, 0, -10, 10 )
	
	glMatrixMode( GL_MODELVIEW )
	glLoadIdentity()
	
	glClearColor( 0.2, 0.2, 0.2, 1.0 )
	glEnable( GL_BLEND )
	glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
	glEnable( GL_TEXTURE_2D )
	
	glDisable( GL_CULL_FACE )
	
	
def DrawLine(v1,v2):
	glDisable(GL_TEXTURE_2D)
	
	glColor3f(1,1,1)
	glBegin(GL_LINES)
	glVertex2f(v1[0],v1[1])
	glVertex2f(v2[0],v2[1])
	glEnd()
	
	glEnable(GL_TEXTURE_2D)
	
def DrawTriStrip(verts):
	glDisable(GL_TEXTURE_2D)
	glColor3f(1,1,1)
	glBegin(GL_TRIANGLE_STRIP)
	
	for vert in verts:
		glVertex2f(vert[0],vert[1])
	
	glEnd()


def DrawTri(verts):
	glBegin(GL_TRIANGLES)
	for vert in verts:
		glVertex2f(vert.x,vert.y)
	glEnd()

	
def DrawColorQuad(rect):
	x,y = rect[0],rect[1]
	width = rect[2]
	height = rect[3]
	
	glTranslatef(x,y,0)
	glDisable(GL_TEXTURE_2D)
	glBegin(GL_QUADS)
	glVertex2f(0,-height)
	glVertex2f(width,-height)
	glVertex2f(width,height)
	glVertex2f(0,height)
	glEnd()
	glEnable(GL_TEXTURE_2D)
	
def DrawQuad(rect):
	x,y = rect[0],rect[1]
	width = rect[2]
	height = rect[3]
	
	#glTranslatef(x,y,0.0)
	
	glBegin(GL_QUADS)
	
	glTexCoord2f(0.0,0.0)
	glVertex2f(-width,-height)
	
	glTexCoord2f(1.0,0.0)
	glVertex2f(width,-height)
	
	glTexCoord2f(1.0,1.0)
	glVertex2f(width,height)
	
	glTexCoord2f(0.0,1.0)
	glVertex2f(-width,height)
	
	glEnd()
	

def DrawGuiQuad(rect):
	glBegin(GL_QUADS)
	
	glTexCoord2f(0.0,0.0)
	glVertex2f(rect.left,rect.top)
	
	glTexCoord2f(1.0,0.0)
	glVertex2f(rect.right,rect.top)
	
	glTexCoord2f(1.0,1.0)
	glVertex2f(rect.right,rect.bottom)
	
	glTexCoord2f(0.0,1.0)
	glVertex2f(rect.left,rect.bottom)
	
	glEnd()

def DrawCircle(pos,rad,seg):
	
	if( seg < 3 ):
		seg = 3
	
	diameter = rad*2
	circum = diameter*math.pi
	radians = math.pi*2
	anglestep = radians / seg
	angle = 0.0
	
	glTranslatef(pos[0],pos[1],0.0)
	glBegin(GL_TRIANGLE_FAN)
	
	glColor3f(1.0,1.0,1.0)
	glTexCoord2f(0.5,0.5)
	glVertex2f(0.0,0.0)
	
	for x in range(0,seg):
		fx = math.cos(angle) * rad
		fy = math.sin(angle) * rad
		angle = angle+anglestep
		
		u =  (fx+rad) / diameter
		v =  (fy+rad) / diameter
		
		glColor3f(1.0,1.0,1.0)
		glTexCoord2f(u,v)
		glVertex2f(fx,fy)
		
	fx = math.cos(0) * rad
	fy = math.sin(0) * rad
	
	u =  (fx+rad) / diameter
	v =  (fy+rad) / diameter
	
	glColor3f(1.0,1.0,1.0)
	glTexCoord2f(u,v)
	glVertex2f(fx,fy)
	glEnd()
		
		
	

