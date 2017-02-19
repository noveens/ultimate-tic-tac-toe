import sys
import random
import signal
import time
import copy

class TimedOutExc(Exception):
	pass

def handler(signum, frame):
	print 'Signal handler called with signal', signum
	raise TimedOutExc()

class BondPlayer():
	def __init__(self):
		self.time_elapsed = 0
		self.type = 'X'
		self.board = Board()
		self.INF = 1000000000

	def move(self, game_board, old_move, type_of_move):
		# game_board.board_status is a 16x16 matrix of all moves
		# game_board.block_status is a 4 x 4 matrix of all blocks status
		# old_move is the move made by the opponent (is a tuple of length 2)
		# type : 'x' or 'o'

		self.type = type_of_move

		board = game_board

		allowed_moves = board.find_valid_move_cells(old_move)
		# when this is first_move some are shitty moves

		ans = -self.INF
		r = allowed_moves[0][0]
		c = allowed_moves[0][1]
		r_b = r
		c_b = c


		for level in range(2, 5, 1):
			# perform dfs upto level 'level'

			ret = self.minimax( 
				allowed_moves, 1, level, old_move
			)

			ans = max(ans, ret)
			if ret[2] >= ans:
				ans = ret[2]
				r = ret[0]
				c = ret[1]

		if r == r_b and c == c_b:
			print ret[2]
		return (r, c)

	def minimax(self, allowed_moves, level, allowed_level, old_move):
			if level % 2 == 1:
				ans = -self.INF

			else:
				ans = self.INF

			r, c = 0,0

			for move in allowed_moves:
				if level >= allowed_level:
					our = self.heuristic()
					if self.type == 'x':
						self.type = 'o'
					else:
						self.type = 'x'
					
					them = self.heuristic()
					if self.type == 'x':
						self.type = 'o'
					else:
						self.type = 'x'
					print 'retrning ', our - them;
					return (r, c, our - them)

				self.board.update(old_move, move, self.type)

				allowed_moves = self.board.find_valid_move_cells(old_move)
				ret = self.minimax(allowed_moves, level+1, allowed_level, move)
				if level % 2 == 0:
					print 'retrning minimising ', ans, ' ret =  ', ret[2]
					if ret[2] <= ans:
						ans = ret[2]
						r = move[0]
						c = move[1]

				else:
					if ret[2] >= ans:
						ans = ret[2]
						r = move[0]
						c = move[1]
				
				self.board.update(old_move, move, '-')

			some_var = (r, c, ans)
			return some_var

	def heuristic(self):

		ans = 0

		for r in range(0,4):
			for c in range(0,4):

				if self.board.block_status[r][c] == self.type:
					ans += 5

					arr = [0,3,5,6,9,10,12,15]

					if ((4*r)+c) in arr:
						ans += 10

					else:
						ans += 3

		for r in range(0,16):
			for c in range(0,16):
				#can optimise by iterating only those required
				r_t = (r%4)
				c_t = (c%4)
				arr = [0,3,5,6,9,10,12,15]

				if (((r_t*4)+c_t) in arr) and self.board.board_status[r][c] == self.type:
					ans += 3

					if (((r/4)*4) + (c/4)) in arr:
						ans += 3

				if (((r/4)*4) + (c/4)) in arr and self.board.board_status[r][c] == self.type:
					ans += 2

		# checking 2 or 3 in row/col rest empty
		for r in range(0,4):
			cross, ow = 0, 0
			
			for c in range(0,4):
				if self.board.block_status[r][c] == self.type:
					cross += 1
				elif self.board.block_status[r][c] != '-':
					ow += 1
			
			if cross == 2 and ow == 0:
				ans += 4

			if cross == 3 and ow == 0:
				ans += 6

		for c in range(0,4):
			cross, ow = 0, 0
			
			for r in range(0,4):
				if self.board.block_status[r][c] == self.type:
					cross += 1
				elif self.board.block_status[r][c] != '-':
					ow += 1
			
			if cross == 2 and ow == 0:
				ans += 4

			if cross == 3 and ow == 0:
				ans += 6

		# checking 2 or 3 in dioganal rest empty
		cross, ow = 0, 0
		for r in range(0,4):

			if self.board.block_status[r][r] == self.type:
				cross+=1;
			elif self.board.block_status[r][r] != '-':
				ow += 1
		if cross == 2 and ow == 0:
			ans += 4
		if cross == 3 and ow == 0:
			ans += 6


		# checking 2 or 3 in row/col of cells rest empty

		for z in range(0,4):
			for r in range(z*4,(z*4)+4):
				cross, ow = 0, 0
				
				for zz in range(0,4):
					for c in range(zz*4,(zz*4)+4):
						if self.board.board_status[r][c] == self.type:
							cross += 1
						elif self.board.board_status[r][c] != '-':
							ow += 1
					
					if cross == 2 and ow == 0:
						ans += 2

					if cross == 3 and ow == 0:
						ans += 3

		for z in range(0,4):
			for c in range(z*4,(z*4)+4):
				cross, ow = 0, 0
				
				for zz in range(0,4):
					for r in range(zz*4,(zz*4)+4):
						if self.board.board_status[r][c] == self.type:
							cross += 1
						elif self.board.board_status[r][c] != '-':
							ow += 1
			
					if cross == 2 and ow == 0:
						ans += 2

					if cross == 3 and ow == 0:
						ans += 3

		# checking 2 or 3 in dioganal rest empty
		cross, ow = 0, 0
		for zz in range(0,4):
			for z in range(0,4):
				for r in range(zz*4,(zz*4)+4):
					if self.board.board_status[r][r+(4*z)-(zz*4)] == self.type:
						cross+=1;
					elif self.board.board_status[r][r+(4*z)-(zz*4)] != '-':
						ow += 1
				if cross == 2 and ow == 0:
					ans += 4
				if cross == 3 and ow == 0:
					ans += 6

		return ans;

class Random_Player():
	def __init__(self):
		pass

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		cells = board.find_valid_move_cells(old_move)
		return cells[random.randrange(len(cells))]

class Manual_Player:
	def __init__(self):
		pass
	def move(self, board, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))

class Board:

	def __init__(self):
		# board_status is the game board
		# block status shows which blocks have been won/drawn and by which player
		self.board_status = [['-' for i in range(16)] for j in range(16)]
		self.block_status = [['-' for i in range(4)] for j in range(4)]

	def print_board(self):
		# for printing the state of the board
		print '==============Board State=============='
		for i in range(16):
			if i%4 == 0:
				print
			for j in range(16):
				if j%4 == 0:
					print "",
				print self.board_status[i][j],
			print 
		print

		print '==============Block State=============='
		for i in range(4):
			for j in range(4):
				print self.block_status[i][j],
			print 
		print '======================================='
		print
		print


	def find_valid_move_cells(self, old_move):
		#returns the valid cells allowed given the last move and the current board state
		allowed_cells = []
		allowed_block = [old_move[0]%4, old_move[1]%4]
		#checks if the move is a free move or not based on the rules

		if old_move != (-1,-1) and self.block_status[allowed_block[0]][allowed_block[1]] == '-':
			for i in range(4*allowed_block[0], 4*allowed_block[0]+4):
				for j in range(4*allowed_block[1], 4*allowed_block[1]+4):
					if self.board_status[i][j] == '-':
						allowed_cells.append((i,j))
		else:
			for i in range(16):
				for j in range(16):
					if self.board_status[i][j] == '-' and self.block_status[i/4][j/4] == '-':
						allowed_cells.append((i,j))
		return allowed_cells	

	def find_terminal_state(self):
		#checks if the game is over(won or drawn) and returns the player who have won the game or the player who has higher blocks in case of a draw
		bs = self.block_status

		cntx = 0
		cnto = 0
		cntd = 0

		for i in range(4):						#counts the blocks won by x, o and drawn blocks
			for j in range(4):
				if bs[i][j] == 'x':
					cntx += 1
				if bs[i][j] == 'o':
					cnto += 1
				if bs[i][j] == 'd':
					cntd += 1

		for i in range(4):
			row = bs[i]							#i'th row 
			col = [x[i] for x in bs]			#i'th column
			#print row,col
			#checking if i'th row or i'th column has been won or not
			if (row[0] =='x' or row[0] == 'o') and (row.count(row[0]) == 4):	
				return (row[0],'WON')
			if (col[0] =='x' or col[0] == 'o') and (col.count(col[0]) == 4):
				return (col[0],'WON')
		#checking if diagnols have been won or not
		if(bs[0][0] == bs[1][1] == bs[2][2] ==bs[3][3]) and (bs[0][0] == 'x' or bs[0][0] == 'o'):
			return (bs[0][0],'WON')
		if(bs[0][3] == bs[1][2] == bs[2][1] ==bs[3][0]) and (bs[0][3] == 'x' or bs[0][3] == 'o'):
			return (bs[0][3],'WON')

		if cntx+cnto+cntd <16:		#if all blocks have not yet been won, continue
			return ('CONTINUE', '-')
		elif cntx+cnto+cntd == 16:							#if game is drawn
			return ('NONE', 'DRAW')

	def check_valid_move(self, old_move, new_move):
		#checks if a move is valid or not given the last move
		if (len(old_move) != 2) or (len(new_move) != 2):
			return False 
		if (type(old_move[0]) is not int) or (type(old_move[1]) is not int) or (type(new_move[0]) is not int) or (type(new_move[1]) is not int):
			return False
		if (old_move != (-1,-1)) and (old_move[0] < 0 or old_move[0] > 16 or old_move[1] < 0 or old_move[1] > 16):
			return False
		cells = self.find_valid_move_cells(old_move)
		return new_move in cells

	def update(self, old_move, new_move, ply):
		#updating the game board and block status as per the move that has been passed in the arguements
		if(self.check_valid_move(old_move, new_move)) == False:
			return 'UNSUCCESSFUL'
		self.board_status[new_move[0]][new_move[1]] = ply

		x = new_move[0]/4
		y = new_move[1]/4
		fl = 0
		bs = self.board_status
		#checking if a block has been won or drawn or not after the current move
		for i in range(4):
			#checking for horizontal pattern(i'th row)
			if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and (bs[4*x+i][4*y] == ply):
				self.block_status[x][y] = ply
				return 'SUCCESSFUL'
			#checking for vertical pattern(i'th column)
			if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and (bs[4*x][4*y+i] == ply):
				self.block_status[x][y] = ply
				return 'SUCCESSFUL'

		#checking for diagnol pattern
		if (bs[4*x][4*y] == bs[4*x+1][4*y+1] == bs[4*x+2][4*y+2] == bs[4*x+3][4*y+3]) and (bs[4*x][4*y] == ply):
			self.block_status[x][y] = ply
			return 'SUCCESSFUL'
		if (bs[4*x+3][4*y] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x][4*y+3]) and (bs[4*x+3][4*y] == ply):
			self.block_status[x][y] = ply
			return 'SUCCESSFUL'

		#checking if a block has any more cells left or has it been drawn
		for i in range(4):
			for j in range(4):
				if bs[4*x+i][4*y+j] =='-':
					return 'SUCCESSFUL'
		self.block_status[x][y] = 'd'
		return 'SUCCESSFUL'

def gameplay(obj1, obj2):				#game simulator

	game_board = Board()
	fl1 = 'x'
	fl2 = 'o'
	old_move = (-1,-1)
	WINNER = ''
	MESSAGE = ''
	TIME = 15
	pts1 = 0
	pts2 = 0

	game_board.print_board()
	signal.signal(signal.SIGALRM, handler)
	while(1):
		#player 1 turn
		temp_board_status = copy.deepcopy(game_board.board_status)
		temp_block_status = copy.deepcopy(game_board.block_status)
		signal.alarm(TIME)

		try:									#try to get player 1's move			
			p1_move = obj1.move(game_board, old_move, fl1)
		except TimedOutExc:					#timeout error
#			print e
			WINNER = 'P2'
			MESSAGE = 'TIME OUT'
			pts2 = 16
			break
		except Exception as e:
			WINNER = 'P2'
			MESSAGE = 'INVALID MOVE'
			pts2 = 16			
			break
		signal.alarm(0)

		#check if board is not modified and move returned is valid
		if (game_board.block_status != temp_block_status) or (game_board.board_status != temp_board_status):
			WINNER = 'P2'
			MESSAGE = 'MODIFIED THE BOARD'
			pts2 = 16
			break
		if game_board.update(old_move, p1_move, fl1) == 'UNSUCCESSFUL':
			WINNER = 'P2'
			MESSAGE = 'INVALID MOVE'
			pts2 = 16
			break

		status = game_board.find_terminal_state()		#find if the game has ended and if yes, find the winner
		print status
		if status[1] == 'WON':							#if the game has ended after a player1 move, player 1 would win
			pts1 = 16
			WINNER = 'P1'
			MESSAGE = 'WON'
			break
		elif status[1] == 'DRAW':						#in case of a draw, each player gets points equal to the number of blocks won
			WINNER = 'NONE'
			MESSAGE = 'DRAW'
			break

		old_move = p1_move
		game_board.print_board()

		#do the same thing for player 2
		temp_board_status = copy.deepcopy(game_board.board_status)
		temp_block_status = copy.deepcopy(game_board.block_status)
		signal.alarm(TIME)

		try:
			p2_move = obj2.move(game_board, old_move, fl2)
		except TimedOutExc:
			WINNER = 'P1'
			MESSAGE = 'TIME OUT'
			pts1 = 16
			break
		except Exception as e:
			WINNER = 'P1'
			MESSAGE = 'INVALID MOVE'
			pts1 = 16			
			break
		signal.alarm(0)
		if (game_board.block_status != temp_block_status) or (game_board.board_status != temp_board_status):
			WINNER = 'P1'
			MESSAGE = 'MODIFIED THE BOARD'
			pts1 = 16
			break
		if game_board.update(old_move, p2_move, fl2) == 'UNSUCCESSFUL':
			WINNER = 'P1'
			MESSAGE = 'INVALID MOVE'
			pts1 = 16
			break

		status = game_board.find_terminal_state()	#find if the game has ended and if yes, find the winner
		print status
		if status[1] == 'WON':						#if the game has ended after a player move, player 2 would win
			pts2 = 16
			WINNER = 'P2'
			MESSAGE = 'WON'
			break
		elif status[1] == 'DRAW':					
			WINNER = 'NONE'
			MESSAGE = 'DRAW'
			break
		game_board.print_board()
		old_move = p2_move

	game_board.print_board()

	print "Winner:", WINNER
	print "Message", MESSAGE

	x = 0
	d = 0
	o = 0
	for i in range(4):
		for j in range(4):
			if game_board.block_status[i][j] == 'x':
				x += 1
			if game_board.block_status[i][j] == 'o':
				o += 1
			if game_board.block_status[i][j] == 'd':
				d += 1
	print 'x:', x, ' o:',o,' d:',d
	if MESSAGE == 'DRAW':
		pts1 = x
		pts2 = o
	return (pts1,pts2)



if __name__ == '__main__':

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		print '                4 => Bond Player vs. Random Player'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Random_Player()
		obj2 = Random_Player()

	elif option == '2':
		obj1 = Random_Player()
		obj2 = Manual_Player()
	elif option == '3':
		obj1 = Manual_Player()
		obj2 = Manual_Player()
	elif option == '4':
		obj1 = Random_Player()
		obj2 = BondPlayer()
	else:
		print 'Invalid option'
		sys.exit(1)

	x = gameplay(obj1, obj2)
	print "Player 1 points:", x[0] 
	print "Player 2 points:", x[1]
