import sys, os, math, random, pygame, OpenGL, ode
from pygame.locals import *
from OpenGL.GL import *

import texture
import gl



def ODEtoOGL(mat,pos):
	return [mat[0],mat[3],mat[6],0,mat[1],mat[4],mat[7],0,mat[2],mat[5],mat[8],0,pos[0],pos[1],1,1]

class BodyBox:
	def __init__(self,world,space,pos,size,mass):
		self.body = ode.Body(world)
		
		self.size = size
		
		m = ode.Mass()
		m.setBoxTotal(mass, size[0],size[1],1)
			
		self.body.setMass(m)
		self.body.setPosition(pos)
			
		self.geom = ode.GeomBox(space,size)
		self.geom.setBody(self.body)
		
		self.join2d = ode.Plane2DJoint(world)
		self.join2d.attach(self.body, ode.environment)
	def draw(self):
		
		x,y,z = self.body.getPosition()
		rgl = ODEtoOGL(self.body.getRotation(),(x,y))
		glPushMatrix()
		glMultMatrixf(rgl)
		rect = ( 0, 0,
				self.size[0]/2, 
				self.size[1]/2 )
		self.texture.Bind()
		gl.DrawQuad(rect)
		glPopMatrix()
	def assignTexture(self,texture):
		self.texture = texture

class BaseCamp:
	def __init__(self,world,space,pos,texture):
		self.mainbody = BodyBox(world,space,pos,(300,150,25),2000)
		self.mainbody.assignTexture(texture)
		
		self.food = 100
		self.fuel = 100
		self.supply = 100
		self.population = 5000
		
	def draw(self):
		self.food -= 0.005
		self.fuel -= 0.005
		self.supply -= 0.005
		
		if self.food < 0:
			self.food = 0
		if self.fuel < 0:
			self.fuel = 0
		if self.supply < 0:
			self.supply = 0
		
		food = 100 - self.food
		fuel = 100 - self.fuel
		supply = 100 - self.supply
		
		self.population -= math.sqrt(food*food+fuel*fuel+supply*supply) / 100
		self.mainbody.draw()
		
	def AddFuel(self):
		self.fuel += 10
		if self.fuel > 100:
			self.fuel = 100
	def AddFood(self):
		self.food += 10
		if self.food > 100:
			self.food = 100
	def AddSupply(self):
		self.supply += 10
		if self.supply > 100:
			self.supply = 100
		
class FuelStation:
	def __init__(self,world,space,pos,texture):
		self.mainbody = BodyBox(world,space,pos,(300,50,25),2000)
		self.mainbody.assignTexture(texture)
		
	def draw(self):
		self.mainbody.draw()
class SupplyCrate:
	def __init__(self,world,space,pos,texture,type):
		self.mainbody = BodyBox(world,space,pos,(25,25,25),3)
		self.mainbody.assignTexture(texture)
		self.type = type
		
	def draw(self):
		self.mainbody.draw()
		

class Enterprise:
	def __init__(self,world,space,pos,texture):
		self.fuellevel = 1
		
		self.rgtexture = texture[0]
		self.lgtexture = texture[1]
		self.bodytexture = texture[2]
		
		leftgear = [pos[0]-33, pos[1]+25, 0]
		rightgear = [pos[0]+33, pos[1]+25, 0]
		self.mainbody = BodyBox(world,space,pos,(50,50,50),15)
		self.leftgearbody = BodyBox(world,space,leftgear,(12,25,25),1)
		self.rightgearbody = BodyBox(world,space,rightgear,(12,25,25),1)
		
		self.leftgearbody.assignTexture(self.lgtexture)
		self.rightgearbody.assignTexture(self.rgtexture)
		self.mainbody.assignTexture(self.bodytexture)
		
		# atach gear to main body
		self.leftjoint = ode.SliderJoint(world)
		self.leftjoint.attach(self.mainbody.body,self.leftgearbody.body)
		self.leftjoint.setAxis((0,1,0))
		self.leftjoint.setParam(ode.paramLoStop,0)
		self.leftjoint.setParam(ode.paramHiStop,50)

		self.rightjoint = ode.SliderJoint(world)
		self.rightjoint.attach(self.mainbody.body,self.rightgearbody.body)
		self.rightjoint.setAxis((0,1,0))
		self.rightjoint.setParam(ode.paramLoStop,0)
		self.rightjoint.setParam(ode.paramHiStop,30)
		
		self.carryingitem = 0
		self.pickupdelay = pygame.time.get_ticks()
		
	def draw(self):
		leftdamp = self.leftjoint.getPositionRate()
		rightdamp = self.rightjoint.getPositionRate()
		if leftdamp > 0:
			self.leftjoint.addForce(-1000)
		if rightdamp > 0:
			self.rightjoint.addForce(-1000)
			
		self.leftjoint.addForce(-500 - rightdamp*5)
		self.rightjoint.addForce(-500 - leftdamp*5)
		
		
		
		if self.carryingitem:
			x,y,z = self.mainbody.body.getPosition()
			attachedbody = self.pickupJoint.getBody(0)
			x1,y1,z1 = attachedbody.getPosition()
			gl.DrawLine((x,y),(x1,y1))

		self.mainbody.draw()
		self.leftgearbody.draw()
		self.rightgearbody.draw()
		
		
	def joinBody(self,world,space,body,type,index):
		if pygame.time.get_ticks() - self.pickupdelay < 500:
			return
		
		self.pickupJoint = ode.BallJoint(world)
		self.pickupJoint.attach(body,self.mainbody.body)
		pos = self.mainbody.body.getPosition()
		realpos = (pos[0],pos[1],0)
		self.pickupJoint.setAnchor(realpos)
		self.carryingitem = 1
		self.pickupdelay = pygame.time.get_ticks()
		self.carrytype = type
		self.carryindex = index
	
	def dropBody(self):
		if pygame.time.get_ticks() - self.pickupdelay < 500:
			return
			
		if self.carryingitem:
			del self.pickupJoint
			self.carryingitem = 0
			self.pickupdelay = pygame.time.get_ticks()
			self.carrytype = -1
		
	def thrustUp(self,throttle):
		self.fuellevel -= 0.0005
		if self.fuellevel < 0.000:
			self.fuellevel = 0
			return
			
		self.mainbody.body.addRelForce((0,-2500*throttle,0))
		
	def rotate(self,ammount):
		self.mainbody.body.addRelTorque((0,0,ammount*15000))
	

def InitPhysics():
	world = ode.World()
	world.setGravity( (0,60,0) )
	world.setQuickStepNumIterations(100)
	world.setERP(0.1)
	
	space = ode.Space()
	
	#floor = ode.GeomPlane(space,(0,-1,0),-600)
	
	contactgroup = ode.JointGroup()
	
	return world,space,contactgroup
	
def near_callback(args, geom1, geom2):
	contacts = ode.collide(geom1,geom2)
	world,contactgroup = args
	for c in contacts:
		c.setBounce(0.2)
		c.setMu(15000)
		j = ode.ContactJoint(world, contactgroup, c)
		j.attach(geom1.getBody(), geom2.getBody())

def RunSimulation(world,space,contactgroup,dt):
	space.collide((world,contactgroup), near_callback)
	world.quickStep(1.0/60)
	contactgroup.empty()
	
