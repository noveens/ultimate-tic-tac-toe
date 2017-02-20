import sys
import random
import signal
import time
import copy
import datetime
from Aman import *
from P2 import *

class TimedOutExc(Exception):
	pass

def handler(signum, frame):
	print 'Signal handler called with signal', signum
	raise TimedOutExc()

class Intelligent_Player():
	def __init__(self):
		self.INFINITY = 100
		self.maxSearchDepth = 2
		self.marker = 'x'
		self.myMove = False
		return

	def heuristics(self, oldMove, newMove, board):
		currFlag = 'x'

		ownFlag = self.marker
		if(self.myMove):
			currFlag = ownFlag
		else:
			currFlag = self.getMarker(ownFlag)

		#checking if own turn or opponents turn
		varMM = 0
		if(self.myMove == False):
			varMM = -1 #opponents turn
		else:
			varMM = 1 #own turn

		tempBoard = copy.deepcopy(board)

		#bs = tempBoard.board_status
		status = tempBoard.find_terminal_state()
		#if game has already ended
		if status[1] == 'WON':
			return varMM*10000
		elif status[1] == 'DRAW': #have to maximize score with draw
			x=0
			o=0
			for i in range(4):
				for j in range(4):
					if tempBoard.block_status[i][j] == 'x':
						x += 1
					if tempBoard.block_status[i][j] == 'o':
						o += 1
			if(ownFlag == 'x'):
				return (x-o)
			else:
				return (o-x)

		#if the game is not yet over heuristics acc to current scenario
		heurVal = 0

		bs = tempBoard.block_status

		##############################################################
		#checking for continuous blocks or cutting other blocks
		##############################################################

		#checking rows
		for i in range(4):
			fl = 0
			count = 0
			for j in range(4):
				if bs[i][j] == self.getMarker(ownFlag):
					fl = 1
				if bs[i][j] == ownFlag:
					count+=1
			if(fl == 0 and count>0):
				for j in range(4):
					heurVal += (2 if bs[i][j]==ownFlag else 0)
			if(fl == 1 and count>0):
				for j in range(4):
					heurVal += (3 if bs[i][j]==self.getMarker(ownFlag) else 0)

		#checking columns
		for j in range(4):
			fl = 0
			count = 0
			for i in range(4):
				if bs[i][j] == self.getMarker(ownFlag):
					fl = 1
				if bs[i][j] == ownFlag:
					count+=1
			if(fl == 0 and count>0):
				for i in range(4):
					heurVal += (2 if bs[i][j]==ownFlag else 0)
			if(fl == 1 and count>0):
				for i in range(4):
					heurVal += (3 if bs[i][j]==self.getMarker(ownFlag) else 0)


		#checking forward diagonal
 		fl = 0
		count = 0
		for i in range(4):
			if bs[i][i] == self.getMarker(ownFlag):
				fl = 1
			if bs[i][i] == ownFlag:
				count+=1
		if(fl == 0 and count>0):
			for i in range(4):
				heurVal += (2 if bs[i][i]==ownFlag else 0)
		if(fl == 1 and count>0):
			for i in range(4):
				heurVal += (3 if bs[i][i]==self.getMarker(ownFlag) else 0)

		#checking back diagonal
		fl = 0
		count = 0
		for i in range(4):
			if bs[3-i][i] == self.getMarker(ownFlag):
				fl = 1
			if bs[3-i][i] == ownFlag:
				count+=1
		if(fl == 0 and count>0):
			for i in range(4):
				heurVal += (2 if bs[3-i][i]==ownFlag else 0)
		if(fl == 1 and count>0):
			for i in range(4):
				heurVal += (3 if bs[3-i][i]==self.getMarker(ownFlag) else 0)

		#############################################################
		#checking for continuous cells in each block or cutting
		##############################################################
		BS = tempBoard.board_status
		for k in range(4):
			for l in range(4):

				#checking rows
				for i in range(4):
					fl = 0
					count = 0
					for j in range(4):
						if BS[4*k + i][4*l + j] == self.getMarker(ownFlag):
							fl = 1
						if BS[4*k + i][4*l + j] == ownFlag:
							count+=1
					if(fl == 0 and count>0):
						# print "continuous row"
						for j in range(4):
							heurVal += (2 if BS[4*k+i][4*l+j]==ownFlag else 0)
					if(fl == 1 and count>0):
						# print "row kaata"
						for j in range(4):
							heurVal += (3 if BS[4*k+i][4*l+j]==self.getMarker(ownFlag) else 0)

				#checking columns
				for j in range(4):
					fl = 0
					count = 0
					for i in range(4):
						if BS[4*k + i][4*l + j] == self.getMarker(ownFlag):
							fl = 1
						if BS[4*k + i][4*l + j] == ownFlag:
							count+=1
					if(fl == 0 and count>0):
						# print "continuous columns"
						for i in range(4):
							heurVal += (2 if BS[4*k+i][4*l+j]==ownFlag else 0)
					if(fl == 1 and count>0):
						# print "column kaata"
						for i in range(4):
							heurVal += (3 if BS[4*k+i][4*l+j]==self.getMarker(ownFlag) else 0)

				#checking forward diagonal
		 		fl = 0
				count = 0
				for i in range(4):
					if BS[4*k+i][4*l+i] == self.getMarker(ownFlag):
						fl = 1
					if BS[4*k + i][4*l + i] == ownFlag:
						count+=1
				if(fl == 0 and count>0):
					# print "continous diagonal"
					for i in range(4):
						heurVal += (2 if BS[4*k+i][4*l+i]==ownFlag else 0)
				if(fl == 1 and count>0):
					# print "diagonal kaata"
					for i in range(4):
						heurVal += (3 if BS[4*k+i][4*l+i]==self.getMarker(ownFlag) else 0)

				#checking back diagonal
				fl = 0
				count=0
				for i in range(4):
					if BS[4*k+3-i][4*l+i] == self.getMarker(ownFlag):
						fl = 1
					if BS[4*k+3-i][4*l+i] == ownFlag:
						count+=1
				if(fl == 0 and count>0):
					# print "continous backward diagonal"
					for i in range(4):
						heurVal += (2 if BS[4*k+3-i][4*l+i]==ownFlag else 0)
				if(fl == 1 and count>0):
					# print "back diagonal kaata"
					for i in range(4):
						heurVal += (3 if BS[4*k+3-i][4*l+i]==self.getMarker(ownFlag) else 0)

		####################################################################################
		#getting centre/corner squares in blocks AND getting squares in centre/corner blocks
		####################################################################################
		for k in range(4):
			for l in range(4):

				#winning/losing centre block
				if( (k==1 or k==2) and (k==1 or k==2)):
					if(bs[k][l] == ownFlag):
						heurVal += 10
					elif(bs[k][l] == self.getMarker(ownFlag)):
						heurVal -= 10

				#winning/losing corner blocks
				if((k==0 or k==3) and (l==0 or l==3)):
					if(bs[k][l] == ownFlag):
						heurVal += 10 #3
					elif(bs[k][l] ==self.getMarker(ownFlag)):
						heurVal -= 10 #3

				#winning/losing blocks
				if bs[k][l] == ownFlag:
					heurVal += 10
				elif bs[k][l] == self.getMarker(ownFlag):
					heurVal -= 10

				for i in range(4):
					for j in range(4):

						#getting centre squares in blocks
						if ((i==1 or i==2) and (j==1 or j==2)):
							if BS[4*k+i][4*l+j] == ownFlag:
								# print "centre square mila"
								heurVal += 3
							elif BS[4*k+i][4*l+j] == self.getMarker(ownFlag):
								# print "centre square kata"
								heurVal -= 3

						#getting corner squares in blocks
						if ((i==0 or i==3) and (j==0 or j==3)):
							if BS[4*k+i][4*l+j] == ownFlag:
								# print "corner square mila"
								heurVal += 3
							elif BS[4*k+i][4*l+j] == self.getMarker(ownFlag):
								# print "corner square kata"
								heurVal -= 3

						#getting square in centre block
						if ((k==1 or k==2) and (l==1 or l==2)):
							if BS[4*k+i][4*l+j] == ownFlag:
								# print "centre block me mila"
								heurVal += 2
							elif BS[4*k+i][4*l+j] == self.getMarker(ownFlag):
								# print "centre block me kata"
								heurVal -= 2

						#getting square in corner block
						if ((k==0 or k==3) and (l==0 or l==3)):
							if BS[4*k+i][4*l+j] == ownFlag:
								# print "corner block me mila"
								heurVal += 2
							elif BS[4*k+i][4*l+j] == self.getMarker(ownFlag):
								# print "corner block me kata"
								heurVal -= 2

		del tempBoard

		return heurVal

	def getMarker(self, flag):
		if flag == 'x':
			return 'o'
		else:
			return 'x'

	def evaluate(self, old_move, node, board):
		#return random.randint(-100,101)
		return self.heuristics(old_move, node, board)

	def move(self, board, old_move, flag):
		self.marker = flag
		self.myMove = True

		#Find the list of valid cells allowed
		cells = board.find_valid_move_cells(old_move)
		initMoves = len(cells)

		# Make a copy of board for future use
		boardCopy = copy.deepcopy(board)
		move = copy.deepcopy(old_move)

		answer_value = -self.INFINITY
		# answer_index = []

		for i in range(0, initMoves):
			temp_value, temp_index = self.IDS(cells[i], boardCopy, move)
			if (temp_value > answer_value):
				answer_value = copy.deepcopy(temp_value)
				answer_index = copy.deepcopy(temp_index)
				# answer_index = []
				# answer_index.append(temp_index)
			# elif (temp_value == answer_value):
				# answer_index.append(temp_index)

		# moveCell = random.randint(0, len(answer_index)-1)
		# print answer_value
		del boardCopy
		return answer_index

	def MTDf(self, root, f, d, board, old_move):
		g = f
		upperBound = self.INFINITY
		lowerBound = -self.INFINITY

		while (lowerBound < upperBound):
			beta = max(g, lowerBound + 1)
			boardCopy = copy.deepcopy(board)
			boardCopy.update(old_move, root, self.marker)
			self.myMove = True

			g = self.alphaBeta(root, beta-1, beta, d, boardCopy, old_move)
			if (g < beta):
				upperBound = g
			else:
				lowerBound = g
		del boardCopy
		return g

	def store(self):
		pass

	def retrieve(self):
		pass

	def allChildren(self, board, blockIdentifier):
		cells = board.find_valid_move_cells(blockIdentifier)
		return cells

	def alphaBeta(self, node, alpha, beta, d, board, old_move):
		# Transposition table lookup
		# lowerbound = 2*self.INFINITY
		# lowerbound, upperbound = self.retrieve(node)
		#
		# if lowerbound != 2*self.INFINITY:
		# 	# Value exists in Transposition table i.e Node value has been determined earlier
		# 	if lowerbound >= beta:
		# 		return lowerbound
		#
		# 	if upperbound <= alpha:
		# 		return upperbound)
		# 	alpha = max(alpha, n.lowerbound);
		# 	beta = min(beta, node.upperbound)

		boardCopy = copy.deepcopy(board)
		if self.myMove:
			boardCopy.update(old_move, node, self.marker)
		else:
			boardCopy.update(old_move, node, self.getMarker(self.marker))

		# print "Wah ji wah"
		# boardCopy.print_board()
		# print
		children = self.allChildren(boardCopy, node)
		nSiblings = len(children)

		# Node is a leaf node
		if ((d == 0) or (nSiblings == 0)):
			g = self.evaluate(old_move, node, boardCopy)
			# print g
			# boardCopy.print_board()
			# print "hello"
			# g = random.randint(-100, 101)

		elif self.myMove:
			# Mark current node as taken by us for future reference
			g = -self.INFINITY

			# Save original alpha value
			a = alpha
			i = 0

			while ((g < beta) and (i < nSiblings)):
				self.myMove = False
				c = children[i]
				g = max(g, self.alphaBeta(c, a, beta, d-1, boardCopy, node))
				a = max(a, g)
				i = i + 1

		# Node is a min node
		else:
			# Mark current node as taken by opponent for future reference
			g = self.INFINITY

			# Save original beta value
			b = beta
			i = 0

			while ((g > alpha) and (i < nSiblings)):
				self.myMove = True
				c = children[i]
				g = min(g, self.alphaBeta(c, alpha, b, d-1, boardCopy, node))
				b = min(b, g)
				i = i + 1

		del boardCopy
		return g;


	def IDS(self, root, board, old_move):
		firstGuess = 0
		#for d in range(1, self.maxSearchDepth):
		boardCopy = copy.deepcopy(board)
		firstGuess = self.MTDf(root, firstGuess, self.maxSearchDepth, boardCopy, old_move)
		#if timeUp:
		#    break
		del boardCopy
		return firstGuess, root

class tictac():
	def __init__(self):
		pass

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		cells = ticTacToe().find_valid_move_cells(board,old_move,flag)
		return cells

class BondPlayer():
	def __init__(self):
		self.time_elapsed = 0
		self.type = 'x'
		self.board = Board()
		self.INF = 1000000000
		self.count = 0
		self.timeLimit = datetime.timedelta(seconds = 14)
		self.begin = 0


	def move(self, game_board, old_move, type_of_move):
		# game_board.board_status is a 16x16 matrix of all moves
		# game_board.block_status is a 4 x 4 matrix of all blocks status
		# old_move is the move made by the opponent (is a tuple of length 2)
		# type : 'x' or 'o'

		self.type = type_of_move

		self.board = copy.deepcopy(game_board)

		allowed_moves = self.board.find_valid_move_cells(old_move)
		# when this is first_move some are shitty moves

		ans = -self.INF
		r = allowed_moves[0][0]
		c = allowed_moves[0][1]
		r_b = r
		c_b = c

		self.begin = datetime.datetime.utcnow()
		while datetime.datetime.utcnow() - self.begin < self.timeLimit:

			for level in range(2, 100, 1):
				# perform dfs upto level 'level'

				if datetime.datetime.utcnow() - self.begin >= self.timeLimit:
					break

				self.count = 0

				ret = self.minimax( 
					allowed_moves, 1, 
					level, old_move,
					-self.INF, self.INF
				)

				if datetime.datetime.utcnow() - self.begin >= self.timeLimit:
					print 'took ', self.count, ' moves at level ', level, '(partial)'

				else:
					#print 'remaining time = ', datetime.datetime.utcnow() - self.begin
					print 'took ', self.count, ' moves at level ', level
				#print 'took ', self.count, ' moves at level ', level

				#print 'gett ', ret[2]
				#ans = max(ans, ret)
				if ret[2] >= ans:
					ans = ret[2]
					r = ret[0]
					c = ret[1]

		# if r == r_b and c == c_b:
		# 	print ret[2]
		# else:
		# 	print '0'
		#print 'final = ', ans
		return (r, c)

	def switch_type(self):
		if self.type == 'x':
			self.type = 'o'
		else:
			self.type = 'x'

	# def alphabeta(self, node, depth, alpha, beta, maximizingPlayer)
 #      	if depth = 0 or node is a terminal node
 #          	return the heuristic value of node
      	
 #      	if maximizingPlayer
 #          	v = -self.INF
 #          	for each child of node
	# 			v = max(v, alphabeta(child, depth - 1, alpha, beta, FALSE))
	# 			alpha = max(alpha, v)
	# 			if beta <= alpha
	# 				break (* beta cut-off *)
	# 		return v
      	
 #      	else
 #          	v = self.INF
 #          	for each child of node
 #              	v = min(v, alphabeta(child, depth - 1, alpha, beta, TRUE))
 #              	beta = min(beta, v)
 #              	if beta <= alpha
 #                  	break (* alpha cut-off *)
 #          	return v

	def minimax(self, allowed_moves, level, allowed_level, old_move, alpha, beta):
		self.count += 1
		#print 'took ', self.count, ' moves at level ', level

		if level % 2 == 1:
			ans = -self.INF

		else:
			ans = self.INF

		r, c = 0, 0

		for move in allowed_moves:
			if datetime.datetime.utcnow() - self.begin < self.timeLimit:

				if alpha < beta:

					if level >= allowed_level:

						our = self.heuristic()
						self.switch_type()
						
						them = self.heuristic()
						self.switch_type()
						
						#print 'returning our: ', our, ' them: ', them
						return (r, c, our - them)

					self.board.update(old_move, move, self.type)

					self.switch_type()

					allowed_moves2 = self.board.find_valid_move_cells(move)

					#print 'len = ', len(allowed_moves2)
					#if len(allowed_moves2) == 0:
					# print 'debug', move 
					# self.board.print_board();
					# print 'debug end'

					ret = self.minimax(allowed_moves2, level+1, allowed_level, move, alpha, beta)
					
					if level % 2 == 0:
						#print 'returning minimising ', ans, ' ret =  ', ret[2]
						if ret[2] <= ans:

							ans = ret[2]
							r = move[0]
							c = move[1]

						beta = min(beta, ret[2])

					else:
						#print 'returning maximising ', ans, ' ret =  ', ret[2]
						if ret[2] >= ans:

							ans = ret[2]
							r = move[0]
							c = move[1]

						alpha = max(alpha, ret[2])
					
					ree = self.update(move, '-')
					#print 'getting', ree
					#self.board.board_status[move[0]][move[1] = '-'

					self.switch_type()

			else:
				break

		if len(allowed_moves) == 0:

			ans *= -1
			self.count-=1

		if ans == self.INF or ans == -self.INF:
			ans *= -1
			#print 'yolo'

		return (r, c, ans)

	def update(self, new_move, ply):
		#updating the game board and block status as per the move that has been passed in the arguements

		self.board.board_status[new_move[0]][new_move[1]] = ply

		x = new_move[0]/4
		y = new_move[1]/4
		fl = 0
		bs = self.board.board_status
		#checking if a block has been won or drawn or not after the current move
		for i in range(4):
			#checking for horizontal pattern(i'th row)
			if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and (bs[4*x+i][4*y] == ply):
				self.board.block_status[x][y] = ply
				return 'SUCCESSFUL'
			#checking for vertical pattern(i'th column)
			if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and (bs[4*x][4*y+i] == ply):
				self.board.block_status[x][y] = ply
				return 'SUCCESSFUL'

		#checking for diagnol pattern
		if (bs[4*x][4*y] == bs[4*x+1][4*y+1] == bs[4*x+2][4*y+2] == bs[4*x+3][4*y+3]) and (bs[4*x][4*y] == ply):
			self.board.block_status[x][y] = ply
			return 'SUCCESSFUL'
		if (bs[4*x+3][4*y] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x][4*y+3]) and (bs[4*x+3][4*y] == ply):
			self.board.block_status[x][y] = ply
			return 'SUCCESSFUL'

		#checking if a block has any more cells left or has it been drawn
		for i in range(4):
			for j in range(4):
				if bs[4*x+i][4*y+j] =='-':
					return 'SUCCESSFUL'
		self.board.block_status[x][y] = 'd'
		return 'SUCCESSFUL'

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
		obj1 = BondPlayer()
		obj2 = player2()
		obj3 = Random_Player()
		obj4 = Intelligent_Player()
	else:
		print 'Invalid option'
		sys.exit(1)

	x = gameplay(obj1, obj2)
	print "Player 1 points:", x[0] 
	print "Player 2 points:", x[1]
