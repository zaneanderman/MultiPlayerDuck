#!/usr/bin/python3
import pyglet
from pyglet import shapes
import random
screen = pyglet.window.Window(640, 500, "Head Jump Game")
leftbird = pyglet.image.load("duckleft.png")
rightbird = pyglet.image.load("duckright.png")

keys = pyglet.window.key.KeyStateHandler()
screen.push_handlers(keys)

class Player(pyglet.sprite.Sprite):
	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(*args, **kwargs)
		self.vy = 0
		self.vx = 0
		self.attackcooldown = 0
		self.onground = False
		self.controls = None
		self.direction = None
		self.timeshit = 0

#class FadingRect(shapes.Rectangle):
#	super(FadingRect, self).__init__

player1 = Player(rightbird, 200, screen.height/2)
player1.controls = {"left":pyglet.window.key.LEFT, "up":pyglet.window.key.UP, "right":pyglet.window.key.RIGHT, "shove":pyglet.window.key.PAGEDOWN}
player1.direction = "right"
player2 = Player(leftbird, 300, screen.height/2)
player2.controls = {"left":pyglet.window.key.A, "up":pyglet.window.key.W, "right":pyglet.window.key.D, "shove":pyglet.window.key.E}
player2.direction = "left"

gravity = 0.5
friction = 0.05
percentperhit = 3
platformbatch = pyglet.graphics.Batch()
platforms = []
drawcache = []
platforms.append(shapes.Rectangle(120, 250, 400, 50, batch=platformbatch, color=(215,1215,255)))
platforms.append(shapes.Rectangle(120, 250, 50, 100, batch=platformbatch, color=(115,255,255)))
platforms.append(shapes.Rectangle(120, 150, 400, 50, batch=platformbatch, color=(255,255,1234567)))
platforms.append(shapes.Rectangle(90, 200, 20, 20, batch=platformbatch, color=(115,255,251234)))
platforms.append(shapes.Rectangle(40, 230, 20, 20, batch=platformbatch, color=(1255,155,155)))
platforms.append(shapes.Rectangle(60, 250, 20, 20, batch=platformbatch, color=(2255,255,856365)))
platforms.append(shapes.Rectangle(-155, 150, 40, 60, batch=platformbatch, color=(3215,255,255)))
platforms.append(shapes.Rectangle(-156, 151, 40, 140, batch=platformbatch, color=(4215,255,255)))
platforms.append(shapes.Rectangle(-159, 152, 40, 290, batch=platformbatch, color=(4215,255,255)))
platforms.append(shapes.Rectangle(100, 50, 470, 50, batch=platformbatch, color=(215,1215,255)))
platforms.append(shapes.Rectangle(555, 130, 20, 20, batch=platformbatch, color=(115,255,251234)))
platforms.append(shapes.Rectangle(555, 370, 20, 20, batch=platformbatch, color=(115,255,251234)))
platforms.append(shapes.Rectangle(400, 430, 75, 1, batch=platformbatch, color=(0,35,0)))
platforms.append(shapes.Rectangle(10, 130, 10, 1, batch=platformbatch, color=(0,34,0)))
platforms.append(shapes.Rectangle(0, 2, 1, 150, batch=platformbatch, color=(0,34,0)))

def iscolliding(rect1, rect2):
	if (rect1.x + rect1.width > rect2.x and
		rect1.x < rect2.x + rect2.width and
		rect1.y + rect1.height > rect2.y and
		rect1.y < rect2.y + rect2.height):  
		return True

def update(dt):
	global gravity
	for player in player1, player2:
		otherplayer = [player1,player2]
		otherplayer.remove(player)
		otherplayer = otherplayer[0]
		player.y += player.vy
		player.onground = False
		isfalling = (player.vy < 0)
		redo = True #this is so you will be pushed out of platforms continually until you aren't in any
		while redo:
			redo = False
			for platform in platforms:
				if iscolliding(player, platform):
					if isfalling:
						player.y = platform.y + platform.height
						player.onground = True
						player.vy = 0
					else:
						player.y = platform.y - player.height
						player.vy = 0

		player.x += player.vx
		ismovingleft = (player.vx < 0)
		redo = True #this is so you will be pushed out of platforms continually until you aren't in any
		while redo:
			redo = False
			for platform in platforms:
				if iscolliding(player, platform):
					redo = True
					if ismovingleft:
						player.x = platform.x + platform.width
						player.vx = 0
					else:
						player.x = platform.x - player.width
						player.vx = 0

		if keys[player.controls["up"]] and player.onground:
			player.vy = 10

		if keys[player.controls["left"]] and not keys[player.controls["right"]]:
			player.direction = "left"
			player.image = leftbird
			if player.vx > -4:
				player.vx -= 0.2

		
		if keys[player.controls["right"]] and not keys[player.controls["left"]]:
			player.direction = "right"
			player.image = rightbird
			if player.vx < 4:
				player.vx += 0.2
		
		if keys[player.controls["shove"]] and player.attackcooldown <= 0:
			player.attackcooldown = 30
			if player.direction == "right":
				attackrect = shapes.Rectangle(player.x+player.width+8, player.y-10, 30, 40, color=(255,0,0))
			else:
				attackrect = shapes.Rectangle(player.x-38, player.y-10, 30, 40, color=(255,0,0))
			drawcache.append(attackrect)
			if iscolliding(otherplayer, attackrect):
				otherplayer.vy = 5*(1+(otherplayer.timeshit*percentperhit/100))
				otherplayer.vx = {"left":-5, "right":5}[player.direction]*(1+otherplayer.timeshit*percentperhit/100)
				otherplayer.timeshit += 1

		player.attackcooldown -= 1
		if player.onground:
			if player.vx < 0:
				player.vx = min(player.vx+friction, 0)
			elif player.vx > 0:
				player.vx = max(player.vx-friction, 0)
		player.vy -= gravity
		player.vy = max(-10, player.vy)
	if player1.y < 0:
		print("player one totally died")
		exit()
	if player2.y < 0:
		print("player two totally died")
		exit()



@screen.event
def on_draw():
	global drawcache
	screen.clear()
	for item in drawcache:
		item.draw()
	drawcache = []
	player1.draw()
	player2.draw()
	platformbatch.draw()

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
