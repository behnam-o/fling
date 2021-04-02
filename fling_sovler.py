import sys
import numpy as np
DIRECTION =["up","down","left","right"]

def create_board():
	""" 
		reads stdin and creates a board. boards are 
		expected in the following format:
		11000
		00100
		10000
		where 1's indicate where balls are.
	"""
	in_list=sys.stdin.read().splitlines()
	size_v=len(in_list)
	size_h=len(in_list[0])

	board=np.zeros(shape=(size_v,size_h)).astype(bool)

	for k in range(len(in_list)):
		line=in_list[k]
		row=list(line)
		for i in range(len(row)):
			row[i]=bool(int(row[i]))
		board[k]=np.array([row])
	return board


def print_board(board):
	""" 
		prints the board to stdout in a human-readable way
	"""
	print("_" * (np.shape(board)[1]*2+1))
	line=""
	for i in range(len(board)):
		for j in range(len(board[i])):
			line+="|"
			if board[i][j]==0:
				line+="_"
			else:
				line+="#"
		line+="|\n"
	print(line)


def applicable_actions(board):
	""" 
		gives allowed actions for a given board
		actions are 3-tuples indicating (x-location,y-location,direction)
		e.g. (1,1,3) means flicking the ball in square (1,1) to the left
	"""
	actions=[]
	for i in range(np.shape(board)[0]):
		for j in range(np.shape(board)[1]):
			if board[i][j]!=0:

				if i!=0 and board[i-1][j]==0:
					for k in range(i-1):
						if board[k][j]!=0:
							actions.append((i,j,0))
							break
				if i!=np.shape(board)[0]-1 and board[i+1][j]==0:
					for k in range(i+2,np.shape(board)[0]):
						if board[k][j]!=0:
							actions.append((i,j,1))
							break
				if j!=0 and board[i][j-1]==0:
					for k in range(j-1):
						if board[i][k]!=0:
							actions.append((i,j,2))
							break
				if j!=np.shape(board)[1]-1 and board[i][j+1]==0:
					for k in range(j+2,np.shape(board)[1]):
						if board[i][k]!=0:
							actions.append((i,j,3))
							break
	return actions

def print_action(action):
	""" 
		prints an action in a human-readable way
	"""
	print("Move: "+"["+str((action[0],action[1]))+" - "+DIRECTION[action[2]]+"]")


def update_board(board_in,action):
	""" 
		Applies a given action to a given board 
		and returns the resulting board.
	"""
	board=np.array(board_in)
	x=action[0]
	y=action[1]
	board[x][y]=0
	if action[2]==0:
		for i in range(x-1,-1,-1):
			if board[i][y]!=0:
				board[i][y]=0
				board[i+1][y]=1
	if action[2]==1:
		for i in range(x+1,np.shape(board)[0],1):
			if board[i][y]!=0:
				board[i][y]=0
				board[i-1][y]=1
	if action[2]==2:
		for i in range(y-1,-1,-1):
			if board[x][i]!=0:
				board[x][i]=0
				board[x][i+1]=1
	if action[2]==3:
		for i in range(y+1,np.shape(board)[1],1):
			if board[x][i]!=0:
				board[x][i]=0
				board[x][i-1]=1
	return board


def find_sol(board,board_action_pairs=[]):
	""" 
		Finds and prints the solution to a given board
		if and only if the board is solvable. Uses the
		well-known 'uninformed search' algorithm,
		emplying recursion and a stack to keep track of
		actions taken in each step of the solution.
	"""
	balls=0
	for i in range(np.shape(board)[0]):
		for j in range(np.shape(board)[1]):
			if board[i][j]==1:
				balls+=1
	if balls==1:
		for i in range(len(board_action_pairs)):
			print_action(board_action_pairs[i][1])
			print_board(board_action_pairs[i][0])
		return True

	actions=applicable_actions(board)
	for i in range(len(actions)):
		next_board=update_board(board,actions[i])
		board_action_pairs.append((next_board,actions[i]))
		if find_sol(next_board,board_action_pairs)==False:
			board_action_pairs.pop()
		else:
			return True
	return False

def main():
	""" 
		Creates a board, prints it, and finds a solution to it if one exists.
	"""
	board=create_board()
	print_board(board)
	find_sol(board)


if __name__ == "__main__":
    main()