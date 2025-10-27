import random 

case_empty = " "

board = [case_empty for i in range (9)]

symboles = ("❌", "⭕")

placeholder = ("1️⃣ ", "2️⃣ ", "3️⃣ ", "4️⃣ ", "5️⃣ ", "6️⃣ ", "7️⃣ ", "8️⃣ ", "9️⃣ ")

player = symboles[0]

def board_print():
	print(" ----+----+----")
	for i in range (9): 
		print("|", board[i] if board[i] != case_empty else placeholder[i], end=" ")
		if i % 3 == 2:
			print("|")
			print(" ----+----+----")
			
while True:
	board_print()
	choise_player = 0


	while choise_player < 1 or choise_player > 9 or board[choise_player -1] != case_empty:
		if player == symboles[0] :  
			choise_player = int(input(" Choisir une case entre 1 à 9 : "))
		if player == symboles[1] :
			choise_player = random.randint(1,9)
			
	board[choise_player -1] = player


	if case_empty != board[0] == board [1] == board[2] \
	or case_empty != board[3] == board [4] == board[5] \
	or case_empty != board[6] == board [7] == board[8] \
	or case_empty != board[0] == board [3] == board[6] \
	or case_empty != board[1] == board [4] == board[7] \
	or case_empty != board[2] == board [5] == board[8] \
	or case_empty != board[0] == board [4] == board[8] \
	or case_empty != board[2] == board [4] == board[6] :
		print("Le joueur ", player, "gagne la partie !")
		board_print()
		break
	if all(cell != case_empty for cell in board):
		print("Match nul !")
		board_print()
		break

	player = symboles[1] if player == symboles[0] else symboles[0]