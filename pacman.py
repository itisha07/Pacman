from random import *
from sys import exit

class Grid:
	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.n_coins = 20
		self.coins_pos = []
		self.n_walls = 20
		self.walls_pos = []
		self.n_ghosts = 1
		self.ghosts = []
	
	def make_grid(self):
		self.grid = [['.' for i in range(self.width)] for j in range(self.height)]
		ctr = 0
		while ctr < self.n_coins:
			x = randint(0,self.height-1)
			y = randint(0,self.width-1)
			if self.grid[x][y] == '.':
				ctr += 1
				self.coins_pos = self.coins_pos + [(x,y)]
				self.grid[x][y] = 'C'
		ctr = 0
		while ctr < self.n_walls:
			x = randint(0,self.height-1)
			y = randint(0,self.width-1)
			if self.grid[x][y] == '.':
				ctr += 1
				self.walls_pos = self.walls_pos + [(x,y)]
				self.grid[x][y] = 'X'
		ctr = 0
		while ctr < self.n_ghosts:
			flag = 0
			while flag == 0:
				x = randint(0,self.height-1)
				y = randint(0,self.width-1)
				if self.grid[x][y] == '.':
					flag = 1
					self.grid[x][y] = 'G'
					ghost_pos = (x,y)
					self.ghosts = self.ghosts + [Ghost(ghost_pos)]
			ctr += 1
		flag = 0
		while flag == 0:
			x = randint(0,self.height-1)
			y = randint(0,self.width-1)
			if self.grid[x][y] == '.':
				flag = 1
				self.grid[x][y] = 'P'
				self.pacman_pos = (x,y)
		self.pacman = Pacman(self.pacman_pos)
	
	def print_board(self):
		for i in range(self.height):
			for j in range(self.width):
				print self.grid[i][j],
			print ""

class Game(Grid):
	def __init__(self,width,height):
		Grid.__init__(self,width,height)
		self.coins_left = 20
		self.is_win = False
		self.is_lose = False
		self.score = 0
		self.level = 1
		self.act_score = 0
	
	def get_score(self):
		if self.coins_left == 0:
			self.is_win = True
		return self.act_score
	
	def get_move(self):
		self.print_board()
		print "Score: ",self.get_score()
		if self.is_win:
			print "Level Completed\n"
			self.n_coins += 5
			self.coins_left = self.n_coins
			self.is_win = False
			self.is_lose = False
			self.score = 0
			self.level += 1
			self.n_ghosts += 1
			self.ghosts = []
			print "Level",self.level,"\n"
			self.make_grid()
			self.game()
		elif self.is_lose:
			print "You Lose!!"
			exit()
		else:
			self.move = raw_input("Enter move: ")
			if self.move == 'q':
				exit()
		
	def game(self):
		while not self.is_win and not self.is_lose:
			self.get_move()
			self.make_move()
		if self.is_lose:
			self.get_move()
			
	def make_move(self):
		ctr = 0
		while ctr < self.n_ghosts:
			self.ghosts[ctr].move(self)
			ctr += 1
		self.pacman.move(self)
	
class Person:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	
class Pacman(Person):
	def __init__(self,pos):
		Person.__init__(self,pos[0],pos[1])
		
	def move(self,game_pos):
		if game_pos.move == 'a':
			nextx = self.x
			nexty = self.y-1
			if not self.check_wall(nextx,nexty,game_pos):
				if self.check_ghost(nextx,nexty,game_pos):
					game_pos.is_lose = True
					game_pos.grid[self.x][self.y] = '.'
				elif self.collect_coin(nextx,nexty,game_pos):
					game_pos.coins_left -= 1
					game_pos.score += 1
					game_pos.act_score += 1
					if game_pos.grid[self.x][self.y] != 'G':
						game_pos.grid[self.x][self.y] = '.'
					game_pos.grid[nextx][nexty] = 'P'
					game_pos.coins_pos.remove((nextx,nexty))
					self.x = nextx
					self.y = nexty
				else:
					if game_pos.grid[self.x][self.y] != 'G':
						game_pos.grid[self.x][self.y] = '.'
					game_pos.grid[nextx][nexty] = 'P'
					self.x = nextx
					self.y = nexty
			else:
				if self.check_ghost(self.x,self.y,game_pos):
					game_pos.is_lose = True
		elif game_pos.move == 'w':
			nextx = self.x-1
			nexty = self.y
			if not self.check_wall(nextx,nexty,game_pos):
				if self.check_ghost(nextx,nexty,game_pos):
					game_pos.is_lose = True
					game_pos.grid[self.x][self.y] = '.'
				elif self.collect_coin(nextx,nexty,game_pos):
					game_pos.coins_left -= 1
					game_pos.score += 1
					game_pos.act_score += 1
					if game_pos.grid[self.x][self.y] != 'G':
						game_pos.grid[self.x][self.y] = '.'
					game_pos.grid[nextx][nexty] = 'P'
					game_pos.coins_pos.remove((nextx,nexty))
					self.x = nextx
					self.y = nexty
				else:
					if game_pos.grid[self.x][self.y] != 'G':
						game_pos.grid[self.x][self.y] = '.'
					game_pos.grid[nextx][nexty] = 'P'
					self.x = nextx
					self.y = nexty
			else:
				if self.check_ghost(self.x,self.y,game_pos):
					game_pos.is_lose = True
		elif game_pos.move == 's':
			nextx = self.x+1
			nexty = self.y
			if not self.check_wall(nextx,nexty,game_pos):
				if self.check_ghost(nextx,nexty,game_pos):
					game_pos.is_lose = True
					game_pos.grid[self.x][self.y] = '.'
				elif self.collect_coin(nextx,nexty,game_pos):
					game_pos.coins_left -= 1
					game_pos.score += 1
					game_pos.act_score += 1
					if game_pos.grid[self.x][self.y] != 'G':
						game_pos.grid[self.x][self.y] = '.'
					game_pos.grid[nextx][nexty] = 'P'
					game_pos.coins_pos.remove((nextx,nexty))
					self.x = nextx
					self.y = nexty
				else:
					if game_pos.grid[self.x][self.y] != 'G':
						game_pos.grid[self.x][self.y] = '.'
					game_pos.grid[nextx][nexty] = 'P'
					self.x = nextx
					self.y = nexty
			else:
				if self.check_ghost(self.x,self.y,game_pos):
					game_pos.is_lose = True
		elif game_pos.move == 'd':
			nextx = self.x
			nexty = self.y+1
			if not self.check_wall(nextx,nexty,game_pos):
				if self.check_ghost(nextx,nexty,game_pos):
					game_pos.is_lose = True
					game_pos.grid[self.x][self.y] = '.'
				elif self.collect_coin(nextx,nexty,game_pos):
					game_pos.coins_left -= 1
					game_pos.score += 1
					game_pos.act_score += 1
					if game_pos.grid[self.x][self.y] != 'G':
						game_pos.grid[self.x][self.y] = '.'
					game_pos.grid[nextx][nexty] = 'P'
					game_pos.coins_pos.remove((nextx,nexty))
					self.x = nextx
					self.y = nexty
				else:
					if game_pos.grid[self.x][self.y] != 'G':
						game_pos.grid[self.x][self.y] = '.'
					game_pos.grid[nextx][nexty] = 'P'
					self.x = nextx
					self.y = nexty
			else:
				if self.check_ghost(self.x,self.y,game_pos):
					game_pos.is_lose = True
		#print "Pacman: ",self.x,self.y
					
	def check_wall(self,nextx,nexty,game_pos):
		if nextx < 0 or nexty < 0 or nextx >= game_pos.height or nexty >= game_pos.width:
			return True
		elif game_pos.grid[nextx][nexty] == 'X':
			return True
		else:
			return False
			
	def check_ghost(self,nextx,nexty,game_pos):
		return game_pos.grid[nextx][nexty] == 'G'
			
	def collect_coin(self,nextx,nexty,game_pos):
		return game_pos.grid[nextx][nexty] == 'C'

class Ghost(Person):
	def __init__(self,pos):
		Person.__init__(self,pos[0],pos[1])
		
	def move(self,game_pos):
		while True:
			r = randint(0,3)
			if r == 0:
				nextx = self.x
				nexty = self.y - 1
			elif r == 1:
				nextx = self.x
				nexty = self.y + 1
			elif r == 2:
				nextx = self.x - 1
				nexty = self.y
			elif r == 3:
				nextx = self.x + 1
				nexty = self.y
			if not self.check_wall(nextx,nexty,game_pos):
				if (self.x,self.y) in game_pos.coins_pos:
					game_pos.grid[self.x][self.y] = 'C'
				else:
					game_pos.grid[self.x][self.y] = '.'
				game_pos.grid[nextx][nexty] = 'G'
				self.x = nextx
				self.y = nexty
				#print "Ghost: ",self.x,self.y
				break
		
	def check_wall(self,nextx,nexty,game_pos):
		if nextx < 0 or nexty < 0 or nextx >= game_pos.height or nexty >= game_pos.width:
			return True
		elif game_pos.grid[nextx][nexty] == 'X':
			return True
		else:
			return False
							
if __name__ == '__main__':
	Game = Game(35,15)
	print "Level 1\n"
	Game.make_grid()
	Game.game()
	while Game.is_win is True:
		Game = Game(35,15)
		Game.make_grid()
		Game.game()
