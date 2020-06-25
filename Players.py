'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''

class Player:
	def __init__(self, symbol):
		self.symbol = symbol
		
	#PYTHON: use obj.symbol instead
	def get_symbol(self):
		return self.symbol
		
	#parent get_move should not be called
	def get_move(self, board):
		raise NotImplementedError()
		
		
		
class HumanPlayer(Player):
	def __init__(self, symbol):
		Player.__init__(self, symbol);
		
	def clone(self):
		return HumanPlayer(self.symbol)
		
#PYTHON: return tuple instead of change reference as in C++
	def get_move(self, board):
		col = int(input("Enter col:"))
		row = int(input("Enter row:"))
		return  (col, row)
		
		
class MinimaxPlayer(Player):

	def __init__(self, symbol):
		Player.__init__(self, symbol);
		if symbol == 'X':
			self.oppSym = 'O'
		else:
			self.oppSym = 'X'
	
	
	# function determines the "goodness" of a terminal state
	# # currently written with the assumption that minimax is 2nd player
	def utility(self, terminalBoard):
		utility = terminalBoard.count_score('O') - terminalBoard.count_score('X')
		
		return utility
		
		
	# function generates all successors that can be reached within one move of the current state
	# returns a list of valid moves
	def successorMoves(self, board, symbol):
		successorList = []
		
		# look for open spaces adjacent to a spaces occupied by the other player, with minimax player occupying opposite end of the piece
		for row in range(0, 4):
			for col in range(0, 4):
				if board.is_legal_move(col, row, symbol):
					successorList.append((col, row))
					
		return successorList
		
		
		
	# returns maximum utility value
	# written with assumption that minimax is 2nd player
	def maxValue(self, board):
#		print("maxValue()")
		if not board.has_legal_moves_remaining('O'):
#			print("MAX TERMINAL")
			# board is terminal
			return self.utility(board)
			
		# finding maximum utility value
		successors = self.successorMoves(board, 'O')
		
		maxUtility = -20 # minimum actual value is -16 (other player has all spaces)
		for successor in successors:
#			print("Max checking successor")
			tempBoard = board.cloneOBoard()
			tempBoard.play_move(successor[0], successor[1], 'O')
			maxUtility = max(maxUtility, self.minValue(tempBoard))
		
#		print("max returning value")	
		return maxUtility
		
		
	# returns minimum utility value
	def minValue(self, board):
#		print("minValue()")
		
#		board.display()
		
		if not board.has_legal_moves_remaining('X'):
#			print("MIN TERMINAL")
			# board is terminal
			return self.utility(board)
			
		successors = self.successorMoves(board, 'X')
		minUtility = 20 # max actual value is 16 (minimax player has all spaces)
		for successor in successors:
#			print("Min checking successor")
			tempBoard = board.cloneOBoard()
			tempBoard.play_move(successor[0], successor[1], 'X')
			minUtility = min(minUtility, self.maxValue(tempBoard))
		
#		print("min returning value")
		return minUtility
		
	# function returns (col, row) tuple for next move
	# # uses minimax
	def get_move(self, board):
		maxUtility = -20
		
		successors = self.successorMoves(board, 'O')
		successorIndex = 0
		
		print("successors", successors)
		
		maxUtilitySuccessorIndex = 0
		
		for successor in successors:
			tempBoard = board.cloneOBoard()
			tempBoard.play_move(successor[0], successor[1], 'O')
			
			successorMin = self.minValue(tempBoard)
#			print("successorMin:", successorMin)
			
			tempMaxUtility = max(maxUtility, successorMin)
			
#			print("currentMax:", maxUtility)
#			print("tempMax:", tempMaxUtility)
			
			# if the new max is actually higher, update the value and the index of the successor
			if tempMaxUtility > maxUtility:
#				print("UPDATING SUCCESSOR")
#				print("new maxUtility:", tempMaxUtility)
				
				maxUtility = tempMaxUtility
				maxUtilitySuccessorIndex = successorIndex
				
			successorIndex += 1
		
		
		print("selected successor:", maxUtilitySuccessorIndex)
		return successors[maxUtilitySuccessorIndex]

