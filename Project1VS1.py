case_empty = " "

board = [case_empty for i in range (9)] 

symboles = ("❌", "⭕") #just esthetic 

placeholder = ("1️⃣ ", "2️⃣ ", "3️⃣ ", "4️⃣ ", "5️⃣ ", "6️⃣ ", "7️⃣ ", "8️⃣ ", "9️⃣ ") #just esthetic

player = symboles[0]

# print board before begin the program
def board_print():
	print(" ----+----+----")
	for i in range (9): 
		print("|", board[i] if board[i] != case_empty else placeholder[i], end=" ") # end use for choise to make a space and not a empty line after all number
		if i % 3 == 2: # for return at the next line after 2 cases
			print("|")
			print(" ----+----+----")

def check_game():
	#all win conditions
	if case_empty != board[0] == board[1] == board[2] \
	or case_empty != board[3] == board[4] == board[5] \
	or case_empty != board[6] == board[7] == board[8] \
	or case_empty != board[0] == board[3] == board[6] \
	or case_empty != board[1] == board[4] == board[7] \
	or case_empty != board[2] == board[5] == board[8] \
	or case_empty != board[0] == board[4] == board[8] \
	or case_empty != board[2] == board[4] == board[6]:
		print("Le joueur", player, "gagne la partie !")
		board_print()
		return True
	#draw conditions
	if all(cell != case_empty for cell in board):
		print("Match nul !")
		board_print()
		return True
	
	return False			

while True:
	board_print() # reapat the fonction for print in the while 
	choise_player = 0
	#input conditions
	while choise_player < 1 or choise_player > 9 or board[choise_player -1] != case_empty:
		choise_player = int(input(" Choisir une case entre 1 à 9 : "))

	board[choise_player -1] = player
    # all win conditions 

	if check_game():
			break
	
	player = symboles[1] if player == symboles[0] else symboles[0] # switch player 