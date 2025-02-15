#strategies
step = 4

Pause = False

player_move_down = [0, step]
player_move_right = [step, 0]
player_move_up = [0, -step]
player_move_left = [-step, 0]

#scenes

sc_x = 256
sc_y = 240

sc_scale = 3

sc_size = sc_x * sc_scale, sc_y * sc_scale


black = (0, 0, 0)
white = (255, 255, 255)
grey = (115, 115, 115)
NES_font = "assets/fonts/nes-font.ttf"