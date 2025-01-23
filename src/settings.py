physics_fps = 120
update_fps = 120

input_slow_motion = 0.2

screen_width = 1216
screen_height = 800

screen_res = (screen_width, screen_height)
screen_mid_point = (screen_width//2, screen_height//2)

tilesize = 32
num_tiles_x = int(screen_width//tilesize)
num_tiles_y = int(screen_height//tilesize)

# physics
gravity = 1000
elasticity_y = 0.6
elasticity_x = 0.8
friction = 0.8

# this causes angle to change
# will fix later
# maximum velocity with which player can lauch themselves
max_impulse = 1500
senstivity = 5

# camera
camera_speed = 25
camera_thresh = 10


##############################
#######       UI       #######
##############################

button_widths = {"large": 100, "medium": 50, "small": 25}

