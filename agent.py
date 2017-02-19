class player():
	def __init__(self):
		self.time_elapsed = 0

	def move(self, game_board, old_move, type):
		# game_board.board_status is a 16x16 matrix of all moves
		# game_board.block_status is a 4 x 4 matrix of all blocks status
		# old_move is the move made by the opponent (is a tuple of length 2)