import numpy as np
import pygame
import sys

pygame.init()

'''True: not empty
   False: empty cell'''

"""game_surface = pygame.display.set_mode((1440, 800))
time_image = pygame.image.load(r'/Users/maria/Downloads/timeline.jpg')
button_image = pygame.image.load(r'/Users/maria/Downloads/Group 1.jpg')
clock_image = pygame.image.load(r'/Users/maria/Downloads/Group 2.jpg')
button_income_image = pygame.image.load(r'/Users/maria/Downloads/Button_Income.png').convert_alpha()
button_image_black = pygame.image.load(r'/Users/maria/Downloads/button_with_black.jpg')
button_petya = pygame.image.load(r'/Users/maria/Downloads/Rectangle 6.png').convert_alpha()
button_vasya = pygame.image.load(r'/Users/maria/Downloads/Rectangle 13.png').convert_alpha()"""
game_surface = pygame.display.set_mode((1440, 800))
time_image = pygame.image.load(r'/Users/vanuyshka/Documents/timeline.jpg')
button_image = pygame.image.load(r'/Users/vanuyshka/Downloads/Group 1.jpg')
button_income_image = pygame.image.load(r'/Users/vanuyshka/Downloads/Button_Income.png').convert_alpha()
clock_image = pygame.image.load(r'/Users/vanuyshka/Downloads/Group 2.jpg')
button_image_black = pygame.image.load(r'/Users/vanuyshka/Downloads/button_with_black.jpg')
button_petya = pygame.image.load(r'/Users/vanuyshka/Downloads/Rectangle 6.png').convert_alpha()
button_vasya = pygame.image.load(r'/Users/vanuyshka/Downloads/Rectangle 13.png').convert_alpha()
CELL_SIZE = 30
CELL_TIMELINE = 50
BLACK = (15, 15, 15)
YELLOW = (255, 255, 153)
YELLOW_CHOSEN = (255, 220, 118)
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
x_timeline, y_timeline = 510, 290


class Tile:
	def __init__(self, default_config, button_income, placing_time, placing_price):
		self.default_config = default_config
		self.current_config = default_config
		self.price = placing_price
		self.button_income = button_income
		self.time = placing_time

	def get_all_configurations(self):  # сколько их вообще должно быть?
		''' - conf0 = default conf
			- conf1 = rot 90
			- conf2 = rot 180
			- conf3 = rot 270
			- conf4 = mirrored default
			- conf5 = mirrored 90
			- conf6 = mirrored 180
			- conf7 = mirrored 270
		'''
		rotated90 = (np.rot90(self.default_config))
		rotated180 = (np.rot90(rotated90))
		rotated270 = (np.rot90(rotated180))
		mirrored = (np.flip(self.default_config, axis=1))
		mirrored90 = (np.rot90(mirrored))
		mirrored180 = (np.rot90(mirrored90))
		mirrored270 = (np.rot90(mirrored180))
		res = [self.default_config, rotated90, rotated180, rotated270, mirrored, mirrored90, mirrored180, mirrored270]
		return res

	@property
	def height(self):
		return self.current_config.shape[0]

	@property
	def width(self):
		if self.height == 0:
			return 0
		return self.current_config.shape[1]

	def print_possible_tile(self, x_player):
		x_coordinate = x_player + 10
		y_coordinate = 230
		income_counter = 0
		for row in self.default_config:
			for cell in row:
				if cell == True:
					pygame.draw.rect(game_surface, (255, 255, 153), (x_coordinate, y_coordinate, 29, 29))
					if income_counter < self.button_income:
						game_surface.blit(button_income_image, (x_coordinate + 7, y_coordinate + 7))
						income_counter += 1
				x_coordinate += 30
			x_coordinate = x_player + 10
			y_coordinate += 30
		pygame.display.update()

	def print_tile(self, x_coordinate, y_coordinate, colour=(255, 255, 153)):
		income_counter = 0
		for row in self.current_config:
			for cell in row:
				if cell == True:
					pygame.draw.rect(game_surface, colour, (x_coordinate, y_coordinate, 29, 29))
					if income_counter < self.button_income:
						game_surface.blit(button_income_image, (x_coordinate + 7, y_coordinate + 7))
						income_counter += 1
				x_coordinate += 30
			x_coordinate -= 30 * self.width
			y_coordinate += 30
		pygame.display.update()


FIELD_HEIGHT = 9
FIELD_WIDTH = 9


class QuiltBoard:
	def __init__(self):
		board = np.zeros((FIELD_HEIGHT, FIELD_WIDTH), dtype=bool)
		self.board = board
		self.bonus = False

	def has_filled_7x7_square(self):
		# здесь подумать как удобней его задать bonus_tile
		bonus_tile = [[True for _ in range(7)] for i in range(7)]
		return np.all(self.board & bonus_tile is False)

	def check_for_bonus(self):
		# проверяет, есть ли на этой борде бонус
		# мб просто смотреть, можно ли поставить тайл 7*7
		# class Player will have player.bonus = False
		pass

	def is_tile_placing_possible(self, player, x_coordinate, y_coordinate, tile):
		x_from = x_coordinate
		y_from = y_coordinate
		if player.buttons < tile.price:
			return False
		if y_from + tile.height > FIELD_HEIGHT or x_from + tile.width > FIELD_WIDTH:
			return False
		return np.all(tile.current_config & self.board[y_from:y_from+tile.height, x_from:x_from+tile.width] == False)

	def place_tile(self, player,  x_coordinate, y_coordinate, tile):
		x_from = x_coordinate
		y_from = y_coordinate
		for i in range(y_from, y_from + tile.height):
			for j in range(x_from, x_from + tile.width):
				if not (self.board[i, j]):
					self.board[i, j] = tile.current_config[i - y_from, j - x_from]
		player.tile_buttons += tile.button_income
		player.buttons -= tile.price
		player.move_timeline(tile.time)

	def print_board(self, player):
		if player == 1:
			x_begin, y_begin = 60, 440
		if player == 2:
			x_begin, y_begin = 1110, 440
		pygame.draw.rect(game_surface, BLACK, (x_begin, y_begin, 9 * CELL_SIZE, 9 * CELL_SIZE))
		for i in range(10):  # 1 board
			pygame.draw.line(game_surface, (255, 255, 255), (x_begin + 30 * i, y_begin),
							 (x_begin + 30 * i, y_begin + 270))
			pygame.draw.line(game_surface, (255, 255, 255), (x_begin, y_begin + 30 * i),
							 (x_begin + 30 * 9, y_begin + 30 * i))
		for row_index in range(len(self.board)):
			for cell_index in range(len(self.board[row_index])):
				if self.board[row_index][cell_index] == True:
					pygame.draw.rect(game_surface, YELLOW, (x_begin + CELL_SIZE * cell_index, y_begin + CELL_SIZE * row_index, 30, 30))

	@property
	def empty_cells_left(self):  # можно не считать так сложно каждый раз, но с 9*9 it isn't important
		empty_cells_counter = 0
		for row in self.board:
			for cell in row:
				if not cell:
					empty_cells_counter += 1
		return empty_cells_counter


class TimeLine:
	def __init__(self, button_income_coords, special_patch_coords, prohibited_coords):
		self.button_income_coordinates = button_income_coords
		self.special_patch_coordinates = special_patch_coords
		self.end_position = 61
		self.prohibited_coordinates = prohibited_coords

	def print_timeline(self, petya, vasya):
		game_surface.blit(time_image, (x_timeline, y_timeline))
		x_button_petya = x_timeline+petya.time_position[2]*CELL_TIMELINE
		y_button_petya = y_timeline+petya.time_position[1]*CELL_TIMELINE
		x_button_vasya = x_timeline+vasya.time_position[2]*CELL_TIMELINE
		y_button_vasya = y_timeline+vasya.time_position[1]*CELL_TIMELINE
		game_surface.blit(button_petya, (x_button_petya, y_button_petya))
		game_surface.blit(button_vasya, (x_button_vasya, y_button_vasya))


class Player:
	def __init__(self, player_board):
		self.player_board = player_board
		self.time_position = [3, 0, 2]  # first_num: position [1;64], second_num: row, third_num: cell
		self.buttons = 5  # buttons that we can waste
		self.special_patch = 0
		self.tile_buttons = 0  # save all tiles buttons

	def move_timeline(self, position_num):
		for i in timeline.prohibited_coordinates:
			if self.time_position[0] < i < self.time_position[0] + position_num:
				position_num += 1
				self.special_patch += 1
		self.time_position[0] += position_num
		i = self.time_position[1]
		j = self.time_position[2]
		for k in range(position_num):
			n = 8
			if j in timeline.button_income_coordinates:
				self.buttons += self.tile_buttons
			if i <= j + 1 and i + j < n - 1:
				j += 1
			elif i < j and i + j >= n - 1:
				i += 1
			elif i >= j and i + j > n - 1:
				j -= 1
			elif i > j + 1 and i + j <= n - 1:
				i -= 1
		self.time_position[1] = i
		self.time_position[2] = j

	def print_buttons(self, x):
		f1 = pygame.font.SysFont('arial', 20)
		game_surface.blit(f1.render(str(self.buttons), False, WHITE), (x, 30))


def create_game_board():
	game_surface.fill((15, 15, 15))
	f1 = pygame.font.SysFont('arial', 20)
	game_surface.blit(f1.render("Нажмите 1, чтобы пройти вперед по треку времени", False, WHITE), (x_timeline - 20, 100))
	game_surface.blit(f1.render("Нажмите 2, чтобы взять и расположить лоскут", False, WHITE), (x_timeline - 20, 120))
	game_surface.blit(f1.render("Нажмите ENTER, чтобы начать игру", False, WHITE), (x_timeline - 20, 140))
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					running = False
		game_surface.blit(time_image, (x_timeline, y_timeline))  # inserts tile piccc
		game_surface.blit(button_petya, (x_timeline + CELL_TIMELINE, y_timeline))
		game_surface.blit(button_vasya, (x_timeline, y_timeline))
		game_surface.blit(button_image_black, (240, 30))
		game_surface.blit(button_image_black, (1170, 30))
		f1 = pygame.font.SysFont('arial', 20)
		game_surface.blit(f1.render(str(5), False, WHITE), (280, 30))
		game_surface.blit(f1.render(str(5), False, WHITE), (1210, 30))
		pygame.draw.rect(game_surface, (96, 96, 96), (60, 220, 390, 190))  # 1 tiles
		pygame.draw.rect(game_surface, (96, 96, 96), (990, 220, 390, 190))  # 2 tiles
		pygame.draw.rect(game_surface, (96, 96, 96), (60, 30, 150, 150))
		pygame.draw.rect(game_surface, (96, 96, 96), (990, 30, 150, 150))
		x_begin = 60
		y_begin = 440
		for i in range(10):  # 1 board
			pygame.draw.line(game_surface, (255, 255, 255), (x_begin + 30 * i, y_begin),
							 (x_begin + 30 * i, y_begin + 270))
			pygame.draw.line(game_surface, (255, 255, 255), (x_begin, y_begin + 30 * i),
							 (x_begin + 30 * 9, y_begin + 30 * i))
		x_begin = x_begin + 30 * 9 + 780
		for i in range(10):  # 2 board
			pygame.draw.line(game_surface, (255, 255, 255), (x_begin + 30 * i, y_begin),
							 (x_begin + 30 * i, y_begin + 270))
			pygame.draw.line(game_surface, (255, 255, 255), (x_begin, y_begin + 30 * i),
							 (x_begin + 30 * 9, y_begin + 30 * i))
		pygame.display.flip()


def choose_tiles(all_tiles, thimble_coordinates):
	if thimble_coordinates + 3 <= len(all_tiles):
		return all_tiles[thimble_coordinates:thimble_coordinates+3]
	return all_tiles[thimble_coordinates:] + all_tiles[:(3-len(all_tiles)+thimble_coordinates)]


def count_score(player, player_board):
	return player.buttons - 2 * player_board.empty_cells_left


create_game_board()
timeline = TimeLine([7, 13, 19, 26, 53, 60], [23, 30, 57, 50], [22, 29, 36, 49])
vasya_board = QuiltBoard()
petya_board = QuiltBoard()
vasya = Player(vasya_board)
petya = Player(petya_board)
thimble_coordinates = 0
all_tiles = [Tile(np.array([
    [False, True, False],
    [True, True, True],
    [False, True, False]], int), button_income=2, placing_time=4, placing_price=1),
Tile(np.array([
    [True, True, False],
    [True, True, True]], int), button_income=1, placing_time=3, placing_price=2),
Tile(np.array([
    [False, True, True, False],
    [True, True, True, True],
    [False, True, True, False],
    [False, True, True, False]], int), button_income=2, placing_time=3, placing_price=4),
Tile(np.array([
    [True, True, True],
    [False, True, False]], int), button_income=1, placing_time=2, placing_price=2),
Tile(np.array([
    [True, True, False],
    [False, True, True],], int), button_income=1, placing_time=2, placing_price=3),
Tile(np.array([
    [False, True, True],
    [True, True, True],
    [True, False, False]], int), button_income=3, placing_time=6, placing_price=8),
Tile(np.array([
    [True, True]], int), button_income=1, placing_time=2, placing_price=2),
Tile(np.array([
    [True, True],
    [False, True]], int), button_income=1, placing_time=1, placing_price=3),
Tile(np.array([
    [True, True, True, True],
    [True,True, False, False]], int), button_income=3, placing_time=5, placing_price=10),
Tile(np.array([
    [True, True, True],
    [False, True, False],
    [True, True, True]], int), button_income=2, placing_time=3, placing_price=2),
Tile(np.array([
    [True, True, True],
    [True, False, True],
    [True, False, True]], int), button_income=1, placing_time=1, placing_price=4),
Tile(np.array([
    [False, True, True],
    [False, True, False],
    [True, True, False]], int), button_income=1, placing_time=2, placing_price=1),
Tile(np.array([
    [True, True],
    [False, True]], int), button_income=0, placing_time=1, placing_price=3),
Tile(np.array([
    [False, True, True],
    [True, True, False]], int), button_income=3, placing_time=6, placing_price=7),
Tile(np.array([
    [False, True, False],
    [True, True, True],
    [False, True, False]], int), button_income=1, placing_time=1, placing_price=7),
Tile(np.array([
    [True, True, False, False],
    [False, True, True, True]], int), button_income=1, placing_time=3, placing_price=2),
Tile(np.array([
    [False, True, True, False],
    [True, True, True, True],
    [False, True, True, False]], int), button_income=1, placing_time=3, placing_price=5),
Tile(np.array([
    [False, False, True],
    [False, True, True],
    [True, True, False]], int), button_income=3, placing_time=4, placing_price=10),
Tile(np.array([
    [True, True, True]], int), button_income=1, placing_time=3, placing_price=3),
Tile(np.array([
    [True, True, True],
    [True, False, True]], int), button_income=0, placing_time=2, placing_price=1),
Tile(np.array([
    [True, True, True],
    [False, False, True]], int), button_income=1, placing_time=2, placing_price=4),
Tile(np.array([
    [False, True, True, True],
    [True, True, True, False]], int), button_income=0, placing_time=2, placing_price=4),
Tile(np.array([
    [True, True, True],
    [False, True, True]], int), button_income=0, placing_time=2, placing_price=2),
Tile(np.array([
    [True, True, True, True],
    [False, False, True, False]], int), button_income=1, placing_time=4, placing_price=3),
Tile(np.array([
    [True, True, True, True]], int), button_income=0, placing_time=1, placing_price=2),
Tile(np.array([
    [True, True],
    [True, True]], int), button_income=2, placing_time=5, placing_price=6),
Tile(np.array([
    [False, True, False],
    [True, True, True],
    [True, False, True]], int), button_income=2, placing_time=6, placing_price=3),
Tile(np.array([
    [True, True, True, True],
    [True, False, False, False]], int), button_income=2, placing_time=3, placing_price=10),
Tile(np.array([
    [True, True, True, True],
    [True, False, False, True]], int), button_income=1, placing_time=5, placing_price=1),
Tile(np.array([
    [True, True, True, True],
    [False, True, True, False]], int), button_income=2, placing_time=3, placing_price=10),
Tile(np.array([
    [True, True],
    [True, False]], int), button_income=0, placing_time=3, placing_price=1),
Tile(np.array([
    [False, True, False, False],
    [True, True, True, True],
    [False, False, True, False]], int), button_income=1, placing_time=3, placing_price=5)]
small_tile = Tile(np.array([[True]], int), button_income=0, placing_time=0, placing_price=0)


def players_move(player, another_player, num_player, players_board, all_tiles, thimble_coordinates):
	if num_player == 1:
		x, y = 60, 100
		x_from = 61
	else:
		x, y = 990, 100
		x_from = 1111
	possible_tiles = choose_tiles(all_tiles, thimble_coordinates)
	prices = []
	for tile in possible_tiles:
		f1 = pygame.font.SysFont('arial', 20)
		game_surface.blit(button_image, (x, 340))
		game_surface.blit(f1.render(str(tile.price), False, WHITE), (x + 40, 345))
		game_surface.blit(clock_image, (x, 380))
		game_surface.blit(f1.render(str(tile.time), False, WHITE), (x + 40, 385))
		tile.print_possible_tile(x)
		prices.append(tile.price)
		x += 130
	x -= 130 * 3
	if player.buttons < min(prices) and another_player.time_position[0] <= player.time_position[0]:
		return 0
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					if another_player.time_position[0] > player.time_position[0]:
						players_move_a(player, another_player)
						running = False
				if event.key == pygame.K_2:
					if player.buttons < min(prices):
						running = False
					else:
						players_move_b(player, num_player, players_board, all_tiles, thimble_coordinates)
						running = False
	pygame.draw.rect(game_surface, BLACK, (x + 220, 30, 20, 20))
	player.print_buttons(x + 160 + 60)
	pygame.draw.rect(game_surface, (96, 96, 96), (x, 220, 390, 190))
	pygame.draw.rect(game_surface, (96, 96, 96), (x, 30, 150, 150))
	timeline.print_timeline(petya, vasya)
	if player.special_patch != 0:
		player.special_patch -= 1
		tile = small_tile
		running = True
		counter_x = 0
		counter_y = 0
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					counter_y_before = counter_y
					counter_x_before = counter_x
					players_board.print_board(num_player)
					if event.key == pygame.K_DOWN:
						counter_y += 1
					if event.key == pygame.K_RIGHT:
						counter_x += 1
					if event.key == pygame.K_UP:
						counter_y -= 1
					if event.key == pygame.K_LEFT:
						counter_x -= 1
					if event.key == pygame.K_RETURN and players_board.is_tile_placing_possible(player, counter_x,
																							   counter_y, tile):
						running = False
					if counter_y + tile.height > FIELD_HEIGHT or counter_x + tile.width > FIELD_WIDTH or counter_x < 0 or counter_y < 0:
						counter_x = counter_x_before
						counter_y = counter_y_before
					elif not (np.all(tile.current_config & players_board.board[counter_y:counter_y + tile.height,
														   counter_x:counter_x + tile.width] == False)):
						tile.print_tile(x_from + counter_x * 30, 441 + counter_y * 30, (200, 150, 200, 0.1))
					elif players_board.is_tile_placing_possible(player, counter_x, counter_y, tile):
						tile.print_tile(x_from + counter_x * 30, 441 + counter_y * 30, GRAY)
		players_board.place_tile(player, counter_x, counter_y, tile)
		tile.print_tile(x_from + counter_x * 30, 441 + counter_y * 30, YELLOW)


def players_move_a(current_player, another_player):
	delta = another_player.time_position[0] - current_player.time_position[0] + 1
	current_player.move_timeline(delta)
	current_player.buttons += delta


def players_move_b(player, num_player, players_board, all_tiles, thimble_coordinates):
	if num_player == 1:
		x, y = 60, 100
		x_from = 61
	else:
		x, y = 990, 100
		x_from = 1111
	possible_tiles = choose_tiles(all_tiles, thimble_coordinates)
	for tile in possible_tiles:
		f1 = pygame.font.SysFont('arial', 20)
		game_surface.blit(button_image, (x, 340))
		game_surface.blit(f1.render(str(tile.price), False, WHITE), (x + 40, 345))
		game_surface.blit(clock_image, (x, 380))
		game_surface.blit(f1.render(str(tile.time), False, WHITE), (x + 40, 385))
		tile.print_possible_tile(x)
		x += 130
	x -= 130 * 3
	# printed possible tiles
	# here choose tile
	chosen_tile = 0
	running = True
	while running:
		y_coordinate = 230
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN and possible_tiles[chosen_tile - 1].price <= player.buttons:
					running = False
				if event.key == pygame.K_RIGHT:
					for i, tile in enumerate(possible_tiles):
						if i == chosen_tile:
							tile.print_tile(x+10, y_coordinate, YELLOW_CHOSEN)
						else:
							tile.print_tile(x+10, y_coordinate, YELLOW)
						x += 130
					x -= 130 * 3
					chosen_tile = (chosen_tile + 1) % 3
					pygame.display.update()
	if chosen_tile == 0:
		tile_index = thimble_coordinates + 2
	else:
		tile_index = thimble_coordinates + chosen_tile - 1
	tile = possible_tiles[chosen_tile - 1]
	all_tiles.pop(tile_index)
	thimble_coordinates += 1
	all_configurations = tile.get_all_configurations()
	pygame.draw.rect(game_surface, (96, 96, 96), (x, 30, 150, 150))
	tile.print_tile(x, 30)
	# print all configurations
	running = True
	i = 1
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					running = False
				if event.key == pygame.K_RIGHT:
					pygame.draw.rect(game_surface, (96, 96, 96), (x, 30, 150, 150))
					tile.current_config = all_configurations[i]
					tile.print_tile(x, 30)
					i = (i+1) % 8
	tile.current_config = all_configurations[i-1]
	running = True
	counter_x = 0
	counter_y = 0
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				counter_y_before = counter_y
				counter_x_before = counter_x
				players_board.print_board(num_player)
				if event.key == pygame.K_DOWN:
					counter_y += 1
				if event.key == pygame.K_RIGHT:
					counter_x += 1
				if event.key == pygame.K_UP:
					counter_y -= 1
				if event.key == pygame.K_LEFT:
					counter_x -= 1
				if event.key == pygame.K_RETURN and players_board.is_tile_placing_possible(player, counter_x, counter_y, tile):
					running = False
				if counter_y + tile.height > FIELD_HEIGHT or counter_x + tile.width > FIELD_WIDTH or counter_x < 0 or counter_y < 0:
					counter_x = counter_x_before
					counter_y = counter_y_before
				elif not(np.all(tile.current_config & players_board.board[counter_y:counter_y+tile.height, counter_x:counter_x+tile.width] == False)):
					tile.print_tile(x_from + counter_x * 30, 441 + counter_y * 30, (200, 150, 200, 0.1))
				elif players_board.is_tile_placing_possible(player, counter_x, counter_y, tile):
					tile.print_tile(x_from + counter_x * 30, 441 + counter_y * 30, GRAY)
	players_board.place_tile(player, counter_x, counter_y, tile)
	pygame.draw.rect(game_surface, BLACK, (x+220, 30, 20, 20))
	player.print_buttons(x + 160 + 60)
	tile.print_tile(x_from + counter_x * 30, 441 + counter_y * 30, YELLOW)
	pygame.draw.rect(game_surface, (96, 96, 96), (x, 220, 390, 190))
	pygame.draw.rect(game_surface, (96, 96, 96), (x, 30, 150, 150))


while vasya.time_position[0] < timeline.end_position and petya.time_position[0] < timeline.end_position:
	'''if abs(petya.time_position[0] - vasya.time_position[0]) <= 1:
		if players_move(vasya, petya, 2, vasya_board, all_tiles, thimble_coordinates) == players_move(vasya, petya, 2, vasya_board, all_tiles, thimble_coordinates) == 0:
			break;'''
	if petya.time_position[0] > vasya.time_position[0]:
		res = players_move(vasya, petya, 2, vasya_board, all_tiles, thimble_coordinates)
		if res == 0:
			players_move(petya, vasya, 1, petya_board, all_tiles, thimble_coordinates)
	else:
		res = players_move(petya, vasya, 1, petya_board, all_tiles, thimble_coordinates)
		if res == 0:
			players_move(vasya, petya, 2, vasya_board, all_tiles, thimble_coordinates)
	timeline.print_timeline(petya, vasya)
	# поверка есть ли бонус

score_petya = count_score(petya, petya_board)
score_vasya = count_score(vasya, vasya_board)
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		else:
			pygame.draw.rect(game_surface, BLACK, (0, 0, 1440, 800))
			ft_font = pygame.freetype.SysFont('Sans', 96)
			text_str = ''
			if score_vasya > score_petya:
				text_str = "Player 2 won"
			elif score_vasya < score_petya:
				text_str = "Player 1 won"
			else:
				text_str = "Draw"
			text_rect = ft_font.get_rect(text_str)
			text_rect.center = game_surface.get_rect().center
			ft_font.render_to(game_surface, text_rect.topleft, text_str, (255, 200, 255))
			pygame.display.flip()

pygame.quit()