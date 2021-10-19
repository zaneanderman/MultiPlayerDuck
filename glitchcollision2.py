#!/usr/bin/python3
import pyglet
from pyglet import shapes
screen = pyglet.window.Window(640, 500, "Head Jump Game")
birdimage = pyglet.image.load("bird.png")
keys = pyglet.window.key.KeyStateHandler()
screen.push_handlers(keys)
bird = pyglet.sprite.Sprite(birdimage, 200, screen.height/2)
bird.update(scale=0.1)
velocity = -1
gravity = 0.5
platformbatch = pyglet.graphics.Batch()
platforms = []
platforms.append(shapes.Rectangle(120, 250, 400, 50, batch=platformbatch, color=(255,255,255)))
platforms.append(shapes.Rectangle(120, 250, 50, 400, batch=platformbatch, color=(255,255,255)))

def iscolliding(rect1, rect2):
	if (rect1.x + rect1.width >= rect2.x and    # rect1. right edge past rect2. left
		rect1.x <= rect2.x + rect2.width and    # rect1. left edge past rect2. right
		rect1.y + rect1.height >= rect2.y and    # rect1. top edge past rect2. bottom
		rect1.y <= rect2.y + rect2.height):      # rect1. bottom edge past rect2. top
		print("collided")
		return True

def update(dt):
	global velocity,gravity
	bird.y += velocity
	onground = False
	for platform in platforms:
		if iscolliding(bird, platform):
			if velocity < 0:
				bird.y = platform.y + platform.height
				onground = True
			else:
				bird.y = platform.y - bird.height

	if keys[pyglet.window.key.UP] and onground:
		velocity = 10

	if keys[pyglet.window.key.LEFT] and not keys[pyglet.window.key.RIGHT]:
		bird.x -= 3
		for platform in platforms:
			if iscolliding(bird, platform):
				bird.x = platform.x + platform.width
	
	if keys[pyglet.window.key.RIGHT] and not keys[pyglet.window.key.LEFT]:
		bird.x += 3
		for platform in platforms:
			if iscolliding(bird, platform):
				bird.x = platform.x - bird.width
	
	velocity -= gravity
	velocity = max(-10, velocity)



@screen.event
def on_draw():
	screen.clear()
	bird.draw()
	platformbatch.draw()

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
