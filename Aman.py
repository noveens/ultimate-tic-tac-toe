import random
class ticTacToe:
	def __init__(self):
		pass

	def find_empty_cells(self,board):
		
		validCells = []
		for i in range(16):
			for j in range(16):
				if board[i][j] == '-': validCells.append([i,j])
		return validCells


	def generate_random_cells(self,board):
		
		allowedMoves = []
		for i in range(16):
			for j in range(16):
				if board.board_status[i][j] == '-' and board.block_status[i/4][j/4] == '-':
					allowedMoves.append([i,j])
				
		return allowedMoves
        
	def find_valid_cells(self,board,old_move):
		
		x, y, emptyCells = (old_move[0]%4)*4, (old_move[1]%4)*4,[]
		for i in range(4):
			for j in range(4):
				if board[x+i][y+j] == '-':emptyCells.append([x+i,y+j])
		return emptyCells

	def block_occupied(self,board,old_move,player):
		
		x, y, flag = (old_move[0]%4)*4, (old_move[1]%4)*4, 0
		
		# print 'please', x, y
		for i in range(4):
			if board[x+i][y] == board[x+i][y+1] == board[x+i][y+2] == board[x+i][y+3]:
				if board[x+i][y] != '-': 
					return 1
			if board[x][y+i] == board[x+1][y+i] == board[x+2][y+i] == board[x+3][y+i]:
				if board[x][y+i] != '-': 
					return 1


		if board[x][y] == board[x+1][y+1] == board[x+2][y+2] == board[x+3][y+3]:
			if board[x][y] != '-': 
				return 1

		if board[x+3][y] == board[x+2][y+1] == board[x+1][y+2] == board[x][y+3]:
			if board[x+3][y] != '-': 
				return 1


		for i in range(4):
			for j in range(4):
				if board[x+i][y+j] == '-': flag = 1

		if flag == 0: return 1

		return 0

	def check_status(self,board,old_move,player,block):

		x,y=(old_move[0]%4)*4,(old_move[1]%4)*4
		for i in range(4):
			if board[x+i][y] == board[x+i][y+1] == board[x+i][y+2] == board[x+i][y+3]:
				if board[x+i][y] == player: 
					return 10
				if board[x+i][y] != player and board[x+i][y] != '-': 
					return -10
		
			if board[x][y+i] == board[x+1][y+i] == board[x+2][y+i] == board[x+3][y+i]:
				if board[x][y+i] == player: 
					return 10
				if board[x][y+i] != player and board[x][y+i] != '-': 
					return -10

		if board[x][y] == board[x+1][y+1] == board[x+2][y+2] == board[x+3][y+3]:
			if board[x][y] == player: 
				return 10
			if board[x][y] != player and board[x][y] != '-': 
				return -10
		
		if board[x+3][y] == board[x+2][y+1] == board[x+1][y+2] == board[x][y+3]:
			if board[x][y+3] == player: 
				return 10
			if board[x][y+3] != player and board[x][y+3] != '-': 
				return -10
		

		for i in range(4):
			if board[x+i][y].count('x') + board[x+i][y+1].count('x') + board[x+i][y+2].count('x') + board[x+i][y+3].count('x') == 3:
				if player == 'x': return 5
				else: return -5 
			if board[x][y+i].count('x') + board[x+1][y+i].count('x') + board[x+2][y+i].count('x') + board[x+3][y+i].count('x') == 3:
				if player == 'x': return 5
				else: return -5 

		if board[x][y].count('x') + board[x+1][y+1].count('x') + board[x+2][y+2].count('x') + board[x+3][y+3].count('x') == 3:
			if player == 'x': return 5
			else: return -5 				
			
		if board[x][y+3].count('x') + board[x+1][y+2].count('x') + board[x+2][y+1].count('x') + board[x+3][y].count('x') == 3:
			if player == 'x': return 5
			else: return -5 				

		# print "YESU"
		x1,y1=(x%4)*4,(y%4)*4

		if block[x1][y1] == '-':
			for i in range(4):
				if board[x1+i][y1].count('x') + board[x1+i][y1+1].count('x') + board[x1+i][y1+2].count('x') + board[x1+i][y1+3].count('x') == 3:
					if player != 'x': return -50
				if board[x1][y1+i].count('x') + board[x1+1][y1+i].count('x') + board[x1+2][y1+i].count('x') + board[x1+3][y1+i].count('x') == 3:
					if player != 'x': return -50

			if board[x1][y1].count('x') + board[x1+1][y1+1].count('x') + board[x1+2][y1+2].count('x') + board[x1+3][y1+3].count('x') == 3:
				if player != 'x' : return -50 				
				
			if board[x1][y1+3].count('x') + board[x1+1][y1+2].count('x') + board[x1+2][y1+1].count('x') + board[x1+3][y1].count('x') == 3:
				if player != 'x': return -50 				



		return 0


	def callMinMax(self,board,old_move,isMax,current_depth,player,alpha,beta,block):
		
		if isMax: best = 100
		else: best = -100

		x, y, flag=(old_move[0]%4)*4,(old_move[1]%4)*4,0
		temp_status = self.check_status(board,old_move,player,block)
		# print 'Hi',temp_status
		if temp_status != 0: 
			return temp_status

		for i in range(4):
			for j in range(4):
				if board[x+i][y+j] == '-':
					flag=1

		if flag == 0: return 0

		if current_depth == 2: 
			return temp_status
	
		for i in range(4):
			for j in range(4):
				if board[x+i][y+j] == '-':
					flag = 1
					c1 = [x+i,y+j]
					if isMax == 1:
						board[x+i][y+j] = player
						best = max(self.callMinMax(board,c1,not isMax, current_depth + 1, player, alpha, beta,block), best)						
						alpha = max(best, alpha)
					else:
						if player == 'x': board[x+i][y+j] = 'o'
						else: board[x+i][y+j] = 'x'
						best = min(self.callMinMax(board,c1,not isMax, current_depth + 1, player, alpha, beta,block), best)
						beta = max(beta, best)
					if beta <= alpha: break
					board[x+i][y+j] = '-'
		return best


	def find_valid_move_cells(self,board,old_move,player):
				

		# First move when old_move is initialised to [-1,-1]

		if old_move[0] == old_move[1] == -1:
			moves = self.generate_random_cells(board)

		# Condition if the whole board is filled or the block in which the player is to move is occupied
		elif self.block_occupied(board.board_status,old_move,player) == 0:
			moves = self.find_valid_cells(board.board_status,old_move)

		# Condition when the cell is full or captured
		else:
			moves = self.generate_random_cells(board)

		# print 'hello = ', self.block_occupied(board.board_status,old_move,player)
		
		# print 'MOves = ', moves

		heuristic = -103
		MIN = -101
		MAX = 101
		isMax = 0
		for i in range(len(moves)):
			x,y = moves[i][0],moves[i][1]
			board.board_status[x][y] = player
			cell = [x,y]
			temp = self.callMinMax(board.board_status,cell,isMax,0,player,MIN,MAX,board.block_status)
			if temp > heuristic:
				heuristic = temp
				f,g = x,y
			board.board_status[x][y] = '-'

		print 'Returning = ', f, g
		
		return f,g