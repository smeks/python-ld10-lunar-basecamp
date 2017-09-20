import sys, os, math, random

import pygame, OpenGL, ode
import texture
import gl
import text
import physics
import math
import random

from pygame.locals import *
from OpenGL.GL import *

screenwidth = 800
screenheight = 600

global mousedown


def input(events):
	

		
	for event in events:
			if event.type == QUIT:
				sys.exit(0)
			if event.type == KEYDOWN:
				if( event.key == 27 ):
					sys.exit(0)
					
			if event.type == VIDEORESIZE:
				global screenwidth,screenheight
				screenwidth = event.w
				screenheight = event.h
				gl.ResizeView( screenwidth, screenheight )
				
			if event.type == MOUSEMOTION:
				blah = 1
				
			global mousedown
			mousedown = 0
			if event.type == MOUSEBUTTONDOWN:
				mousedown = 1
				
def InitGraphics():
	global screenwidth
	global screenheight
	pygame.init()
	window = pygame.display.set_mode((screenwidth,screenheight), pygame.OPENGL | pygame.DOUBLEBUF, 32 )
	pygame.display.set_caption('Basecamp Chain Reaction v1.0')
	gl.ResizeView(screenwidth,screenheight)
	

	
def main():
	InitGraphics()
	
	fps = 0
	fpsdisplay=0
	starttime = pygame.time.get_ticks()
	fpsstring = 'none'
	clock = pygame.time.Clock()
	
	
	background = texture.Texture('data/background.png')
	
	camptexture = texture.Texture('data/basecamp.png')
	
	fuelstationtexture = texture.Texture('data/fuelstation.png')
	
	font = text.BMFont("data/font.fnt")
	foodtexture = texture.Texture('data/foodcrate.png')
	supplytexture = texture.Texture('data/supplycrate.png')
	fueltexture = texture.Texture('data/fuelcrate.png')
	
	rightgeartexture = texture.Texture('data/right_gear.png')
	leftgeartexture = texture.Texture('data/left_gear.png')
	shiptexture = texture.Texture('data/ship.png')
	
	
	

	
	world,space,contactgroup = physics.InitPhysics()
	
	basecampHunger = 0
	basecampEnergy = 100
	basecampSupply = 100
	basecampPopulation = 4000
	
	ship = physics.Enterprise(world,space,(200,200,0),(rightgeartexture,leftgeartexture,shiptexture))
	fuelstation = physics.FuelStation(world,space,(1200,50,0),fuelstationtexture)
	basecamp = physics.BaseCamp(world,space,(2200,50,0),camptexture)
	
	
	supplycrates = []
	
	# add 10 of each crate to the world
	for index in range(0,10):
		xrand = random.randrange(0,200)
		yrand = random.randrange(0,25)
		yrand+=400
		xrand += index * 10
		yrand += index * 10
		fuelcrate = physics.SupplyCrate(world,space,(500+xrand,yrand,0),fueltexture,0)
		
		xrand = random.randrange(0,200)
		yrand = random.randrange(0,25)
		yrand+=400
		xrand += 25
		yrand -= index * 10
		foodcrate = physics.SupplyCrate(world,space,(500+xrand,yrand,0),foodtexture,1)
		
		xrand = random.randrange(0,200)
		yrand = random.randrange(0,25)
		yrand+=400
		xrand += 25
		yrand -= index * 20
		supplycrate = physics.SupplyCrate(world,space,(500+xrand,yrand,0),supplytexture,2)
		
		supplycrates.append(fuelcrate)
		supplycrates.append(foodcrate)
		supplycrates.append(supplycrate)
	
	verts = [[0.0,600.0,0.0],[200.0,500.0,0.0],[400.0,600.0,0.0],[800.0,500.0,0.0],[1000.0,600.0,0.0],[1500.0,550.0,0.0],[2000.0,600.0,0.0],[2500.0,400.0,0.0],[3000.0,600.0,0.0]]
	faces = [[0,1,2],[2,3,4],[4,5,6],[6,7,8]]
	tris = ode.TriMeshData()
	tris.build( verts,faces )
	worldmesh = ode.GeomTriMesh(tris,space)
		
	
	gamestate = 0
	
	basecampstarttime = 0
	basecampendtime = 0
	while 1:
		input(pygame.event.get())
		keystate = pygame.key.get_pressed()
		if keystate[K_UP]:
			ship.thrustUp(1.0)
		if keystate[K_LEFT]:
			ship.rotate(-1.0)
		if keystate[K_RIGHT]:
			ship.rotate(1.0)
		if keystate[K_SPACE]:
			# find the nearest crate to pickup
			if ship.carryingitem == 0:
				index = 0
				for curcrate in supplycrates:
					x,y,z = curcrate.mainbody.body.getPosition()
					x1,y1,z1 = ship.mainbody.body.getPosition()
					dx = x - x1
					dy = y - y1
					distance = math.sqrt(dx*dx+dy*dy)
					if distance < 100:
						ship.joinBody(world,space,curcrate.mainbody.body,curcrate.type,index)
					index+=1
			else:
				ship.dropBody()
				
		if gamestate == 2:
			background.Bind()
			gl.DrawQuad((0,0,4024,4024))
			font.draw((300,300),"OMG EVERYONE DIED\nGame Over\nYour score %d" % basecampendtime)
			
		
		if gamestate == 0:
			background.Bind()
			gl.DrawQuad((0,0,4024,4024))
			
			font.draw((20,20),"INSTRUCTIONS:\n\nLEFTARROW:      rotate ship left\nRIGHTARROW:     rotate ship right\nUPARROW:           thrust up\nSPACE:                grapple supply crate\n\nThe point to the game is to keep the base camp\npopulation alive as long as possible.  \nEach resource has a chain reaction on other resources\nwhich can in turn exponential kill off the population.\n\nGrap resource crates and fly them near the basecamp\nRefuel by landing on the fuel platform.")
			
			glColor4f(1.0,0.5,0.5,0.40)
			gl.DrawColorQuad((110,520,550,32))
			glColor4f(1.0,1.0,1.0,1.0)
			font.draw((200,520),"CLICK ANYWHERE TO START GAME")
			global mousedown
			if mousedown:
				basecampstarttime = pygame.time.get_ticks()
				gamestate = 1
		if gamestate == 1:
			if basecamp.population < 1:
				gamestate = 2
				basecampendtime = pygame.time.get_ticks() - basecampstarttime
				
			
				
			# basecamp takes resource off of your ship if within proximity
			x,y,z = ship.mainbody.body.getPosition()
			x1,y1,z1 = basecamp.mainbody.body.getPosition()
			dx = x1 - x
			dy = y1 - y
			distance = math.sqrt(dx*dx+dy*dy)
			if distance < 300 and ship.carryingitem == 1 and ship.carryindex > 0:
				if ship.carrytype == 0:
					basecamp.AddFuel()
				if ship.carrytype == 1:
					basecamp.AddFood()
				if ship.carrytype == 2:
					basecamp.AddSupply()
				

				ship.dropBody()
				del supplycrates[ship.carryindex]
				ship.carryingitem = 0
				ship.carryindex = -1
				
				
				
			
			# add fuel to ship only if really close to fuel station & landing gear not moving
			x,y,z = ship.mainbody.body.getPosition()
			x1,y1,z1 = fuelstation.mainbody.body.getPosition()
			dx = x1 - x
			dy = y1 - y
			distance = math.sqrt(dx*dx+dy*dy)
			leftgear = abs(ship.leftjoint.getPositionRate())
			rightgear = abs(ship.rightjoint.getPositionRate())
			gearforce = leftgear+rightgear
			
			if distance < 140 and gearforce < 0.5:
				ship.fuellevel+= 0.01
				if ship.fuellevel > 1.0:
					ship.fuellevel = 1.0
			

			
			physics.RunSimulation(world,space,contactgroup,1.0/60.0)
			
			# translate to the ship
			x,y,z = ship.mainbody.body.getPosition()
			glTranslatef(-x-200,-y+300,0)
			
			background.Bind()
			gl.DrawQuad((0,0,4024,4024))
			
			#draw world
			for index in range(0,len(verts)-1):
				glPushMatrix()
				x1 = verts[index][0]
				y1 = verts[index][1]
				
				x2 = verts[index+1][0]
				y2 = verts[index+1][1]
				
				gl.DrawLine((x1,y1),(x2,y2))
				
				glPopMatrix()

			
			ship.draw()
			
			
			# draw basecamp
			basecamp.draw()
			fuelstation.draw()
			
			#draw supply crates
			for crate in supplycrates:
				crate.draw()
			
			
			
			# draw hud
			glPushMatrix()
			x,y,z = ship.mainbody.body.getPosition()
			glColor4f(1.0,0.5,0.5,0.75)
			gl.DrawColorQuad((x-375,y-250,300*ship.fuellevel,32))
			glPopMatrix()
			
			fuel = basecamp.fuel
			food = basecamp.food
			supply = basecamp.supply
			pop = basecamp.population
			
			glPushMatrix()
			glColor4f(0.5,1.0,0.5,0.75)
			gl.DrawColorQuad((x-375,y+150,fuel,16))
			glPopMatrix()
			glPushMatrix()
			gl.DrawColorQuad((x-375,y+190,food,16))
			glPopMatrix()
			glPushMatrix()
			gl.DrawColorQuad((x-375,y+230,supply,16))
			glPopMatrix()
			glPushMatrix()
			gl.DrawColorQuad((x-375,y+270,pop/50,16))
			glPopMatrix()
			
			glColor4f(1.0,1.0,1.0,1.0)
			
			
			font.draw((32,435),"fuel %d" % fuel)
			font.draw((32,435+38),"food %d" % food)
			font.draw((32,435+38*2),"supply %d" % supply)
			font.draw((32,435+38*3),"population %d" % pop)
			
			fuelleveltext = 'fuel level: %.0f' % (ship.fuellevel*100)
			font.draw((32,32),fuelleveltext)

			
			if ship.fuellevel < 0.3:
				fuelleveltext = 'LOW FUEL'
				font.draw((400,300),fuelleveltext)
				

		
		font.draw((screenwidth-200,0),fpsstring)
		pygame.display.flip()
		fps+=1
		
		clock.tick(60)
		if( pygame.time.get_ticks() - starttime > 1000 ):
			fpsdisplay=fps
			fpsstring = 'fps: %d' % fpsdisplay
			fps=0
			starttime = pygame.time.get_ticks()
		
main()
	