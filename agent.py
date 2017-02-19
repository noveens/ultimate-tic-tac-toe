import numpy as np

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
		r, c = 0,0

		for level in range(2, 5, 1):
			# perform dfs upto level 'level'

			ret = self.minimax( 
				allowed_moves, 1, level
			)

			ans = max(ans, ret)
			if ret[2] >= ans:
				ans = ret[2]
				r = ret[0]
				c = ret[1]

		return (r, c)

	def minimax(self, allowed_moves, level, allowed_level):
			if level % 2 == 1:
				ans = -self.INF

			else:
				ans = self.INF

			r, c = 0, 0

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
					return our - them

				self.board.update(old_move, move, self.type)

				allowed_moves = board.find_valid_move_cells(old_move)
				ret = self.minimax(allowed_moves, level+1, allowed_level)
				if level % 2 == 0:
					if ret >= ans:
						ans = ret
						r = move[0]
						c = move[1]
					#ans = max(ans, ret)

				else:
					#ans = min(ans, ret)
					if ret <= ans:
						ans = ret
						r = move[0]
						c = move[1]
				
				self.board.update(old_move, move, ' ')

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
				else if self.board.block_status[r][c] != ' ':
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
				else if self.board.block_status[r][c] != ' ':
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
			else if self.board.block_status[r][r] != ' ':
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
						else if self.board.board_status[r][c] != ' ':
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
						else if self.board.board_status[r][c] != ' ':
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

					if self.board.board_status[r+(4*z)][r+(4*z)] == self.type:
						cross+=1;
					else if self.board.board_status[r+(4*z)][r+(4*z)] != ' ':
						ow += 1
				if cross == 2 and ow == 0:
					ans += 4
				if cross == 3 and ow == 0:
					ans += 6

		return ans;