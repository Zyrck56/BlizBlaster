from __future__ import division

from math import cos, sin, fabs, pi
from random import randint

import sfml as sf
import time

# define some constants
game_size = sf.Vector2(800, 900)
tank_size = sf.Vector2(100, 25)

# create the window of the application
w, h = game_size
window = sf.RenderWindow(sf.VideoMode(w, h), "Blizzard Blaster")
window.vertical_synchronization = True

# load the sounds used in the game
dray_sound_buffer = sf.SoundBuffer.from_file("data/laser.wav")
dray_sound = sf.Sound(dray_sound_buffer)

rampage_sound_buffer = sf.SoundBuffer.from_file("data/rampage.wav")
rampage_sound = sf.Sound(rampage_sound_buffer)

unstoppable_sound_buffer = sf.SoundBuffer.from_file("data/unstoppable.wav")
unstoppable_sound = sf.Sound(unstoppable_sound_buffer)

whicked_sick_sound_buffer = sf.SoundBuffer.from_file("data/whickedsick.wav")
whicked_sick_sound = sf.Sound(whicked_sick_sound_buffer)

play_sound_buffer = sf.SoundBuffer.from_file("data/prepare4.wav")
play_sound = sf.Sound(play_sound_buffer)

eagle_eye_sound_buffer = sf.SoundBuffer.from_file("data/eagleeye.wav")
eagle_eye_sound = sf.Sound(eagle_eye_sound_buffer)

head_hunter_sound_buffer = sf.SoundBuffer.from_file("data/headhunter.wav")
head_hunter_sound = sf.Sound(head_hunter_sound_buffer)

# create the left paddle
tank = sf.RectangleShape()
tank.size = tank_size - (3, 3)
tank.outline_thickness = 3
tank.outline_color = sf.Color.BLACK
tank.fill_color = sf.Color(0, 100, 0)
tank.origin = tank_size / 2

# create the dray
dray = sf.RectangleShape()
dray.size = (5, game_size.y * 2)
dray.outline_thickness = 3
dray.outline_color = sf.Color.YELLOW
dray.fill_color = sf.Color.RED
dray.origin = dray.size / 2

#create snowflake
snowflake = sf.CircleShape()
snowflake.radius = 15
snowflake.fill_color = sf.Color.WHITE
snowflake.origin = (15, 15)

hit_snowflake = sf.CircleShape()
hit_snowflake.radius = 10
hit_snowflake.outline_thickness = 5
hit_snowflake.outline_color = sf.Color.RED
hit_snowflake.fill_color = sf.Color.YELLOW
hit_snowflake.origin = (15, 15)

# load the font
font = sf.Font.from_file("data/sansation.ttf")

# initialize the pause message
pause_message = sf.Text()
pause_message.font = font
pause_message.character_size = 40
pause_message.position = (170, 150)
pause_message.color = sf.Color.WHITE
pause_message.string = "Welcome to Blizzard Blaster!\nPress space to start the game"

game_over_message = sf.Text()
game_over_message.font = font
game_over_message.character_size = 40
game_over_message.position = (170, 150)
game_over_message.color = sf.Color.WHITE

score_display = sf.Text()
score_display.font = font
score_display.character_size = 14
score_display.position = (game_size.x - 100, 20)
score_display.color = sf.Color.WHITE
# define the paddles properties
dray_clock = sf.Clock()
ai_time = sf.seconds(0.1)
tank_speed = 800.

high_score = 0

skill_clock = sf.Clock()

clock = sf.Clock()
dray_time_delta = 0
is_playing = False
game_over = False

while window.is_open:

	# handle events
	for event in window.events:
		# window closed or escape key pressed: exit
		if type(event) is sf.CloseEvent:
			window.close()

		if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.ESCAPE:
			window.close()

		# space key pressed: play
		if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.SPACE:
			if not is_playing:
				# (re)start the game
				is_playing = True
				draw_dray = False
				draw_snowflake = True
				game_over = False
				snowflake_speed = 100.
				score = 0
				streak = 0
				misscount = 0
				longest_streak = 0
				score_display.string = "Score: 0"
				clock.restart()
				dray_clock.restart()

				# reset the position of the paddles and dray
				tank.position = (game_size.x / 2, game_size.y - 10)
				snowflake.position = (randint(tank_size.x / 2, game_size.x - (tank_size.x / 2)), 0) 

				play_sound.play()
	if is_playing:
		delta_time = clock.restart().seconds
		
		if draw_snowflake == False:
			snowflake.position = (randint(tank_size.x / 2, game_size.x - (tank_size.x / 2)), 0) 
			draw_snowflake = True
			snowflake_speed += 10
		
		# move the tank
		if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT) and tank.position.x - tank_size.x / 2 > 5:
			tank.move((-tank_speed * delta_time, 0))

		if sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT) and tank.position.x + tank_size.x / 2 < game_size.x - 5:
			tank.position += (tank_speed * delta_time, 0)

		if sf.Keyboard.is_key_pressed(sf.Keyboard.ESCAPE):
			is_playing = False			

		if sf.Keyboard.is_key_pressed(sf.Keyboard.Z):
			if dray_clock.elapsed_time.milliseconds < 30:
				dray.position = tank.position
				draw_dray = True
				missed = True
				for x in range(int(dray.position.x - 25), int(dray.position.x + 25)):
					if x == snowflake.position.x:
						skill_delta = skill_clock.restart().milliseconds
						if skill_delta < 250 and misscount == 0:
							eagle_eye_sound.play()
						elif skill_delta < 400 and misscount == 0:
							head_hunter_sound.play()
						dray_sound.play()
						draw_snowflake = False
						hit_snowflake.position = snowflake.position
						score += 10

						if score > high_score:
							high_score = score

						streak += 1

						if streak > longest_streak:
							longest_streak = streak

						misscount = 0
						missed = False
						score_display.string = "Score: %d" % score
						if streak == 7:
							whicked_sick_sound.play()
						if streak == 12:
							rampage_sound.play()
						if streak == 15:
							unstoppable_sound.play()
 
				if missed:
					misscount += 1
					streak = 0

			else:
				draw_dray = False

		else:
			draw_dray = False	
			dray_clock.restart()

		snowflake.position += (0, snowflake_speed * delta_time)

	if snowflake.position.y > game_size.y:
		is_playing = False
		game_over = True
		game_over_message.string = " Game Over\n Score: %d\n High Score: %d\n Longest Streak: %d\n\n Space to start a new game\n Escape to quit" % (score, high_score, longest_streak)	    

	window.clear(sf.Color(0, 0, 0))

	if is_playing:
		# draw stuff
		if draw_dray:
			window.draw(dray)
		window.draw(tank)
		window.draw(score_display)

		if draw_snowflake:
			window.draw(snowflake)
		else:
			window.draw(hit_snowflake)

	if game_over:
		window.draw(game_over_message)
	elif not is_playing:
		# draw the pause message
		window.draw(pause_message)

	# display things on screen
	window.display()
		
	
