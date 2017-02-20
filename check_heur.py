class board():
	def __init__(self):
		self.board_status = [['-' for i in range(0,16)]for i in range(0,16)]
		self.block_status = [['-' for i in range(0,4)]for i in range(0,4)]
		self.type = 'x'

	def heuristic(self):
		ans = 0

		for r in range(0,4):
			for c in range(0,4):

				if self.block_status[r][c] == self.type:
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

				if (((r_t*4)+c_t) in arr) and self.board_status[r][c] == self.type:
					ans += 3

					if (((r/4)*4) + (c/4)) in arr:
						ans += 3

				if (((r/4)*4) + (c/4)) in arr and self.board_status[r][c] == self.type:
					ans += 2

		# checking 2 or 3 in row/col rest empty
		for r in range(0,4):
			cross, ow = 0, 0
			
			for c in range(0,4):
				if self.block_status[r][c] == self.type:
					cross += 1
				elif self.block_status[r][c] != '-':
					ow += 1
			
			if cross == 2 and ow == 0:
				ans += 4

			if cross == 3 and ow == 0:
				ans += 6

		for c in range(0,4):
			cross, ow = 0, 0
			
			for r in range(0,4):
				if self.block_status[r][c] == self.type:
					cross += 1
				elif self.block_status[r][c] != '-':
					ow += 1
			
			if cross == 2 and ow == 0:
				ans += 4

			if cross == 3 and ow == 0:
				ans += 6

		# checking 2 or 3 in dioganal rest empty
		cross, ow = 0, 0
		for r in range(0,4):

			if self.block_status[r][r] == self.type:
				cross+=1;
			elif self.block_status[r][r] != '-':
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
						if self.board_status[r][c] == self.type:
							cross += 1
						elif self.board_status[r][c] != '-':
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
						if self.board_status[r][c] == self.type:
							cross += 1
						elif self.board_status[r][c] != '-':
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
					if self.board_status[r][r+(4*z)-(zz*4)] == self.type:
						cross+=1;
					elif self.board_status[r][r+(4*z)-(zz*4)] != '-':
						ow += 1
				if cross == 2 and ow == 0:
					ans += 4
				if cross == 3 and ow == 0:
					ans += 6

		return ans;


a = board()
c = 0
for i in range(0,16):
	b = raw_input('>>').split(' ')
	for j in range(0,16):
		a.board_status[c][j] = b[j]
	c+=1
	print

for r in a.board_status:
	print r
ans = a.heuristic()
print ans