import logging
import sys


# main
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s %(filename)s:%(funcName)s %(levelname)s] %(message)s'))
logger.addHandler(handler)

FPS = 60


# scenes
sc_x = 256
sc_y = 240

sc_scale = 3
sc_x_obj = sc_x * sc_scale
sc_y_obj = sc_y * sc_scale

font_size = 12

sc_size = sc_x_obj, sc_y_obj

hud = 16
hud_width = hud * sc_scale

offs_obj = 20

black = (0, 0, 0)
white = (255, 255, 255)
grey = (115, 115, 115)
NES_font = "assets/fonts/nes-font.ttf"


# strategies
Pause = False


#sprites
speed = 0.4
speed_bullet = 1.4
tank_scale = 0.8125
