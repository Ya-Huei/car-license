import random
import string

def card_random_func():
	str=""
	letter_card=str.join(random.sample(letter, 3))
	number_card=str.join(random.sample(number, 4))
	card=letter_card+"-"+number_card
	return card

if __name__ == '__main__':
	letter=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
	number=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
	f = open('card_random.txt', 'w')
	for i in range(0, 200):
		card=card_random_func()
		f.write(card+",M\n")
	f.close()


# MAY-0001～PZZ-9999
# JAA-0001～JZZ-9999
# XAA-0001～ZZZ-9999
# WFA-0001～WZZ-9999
# QNA-0001～QZZ-9999
# LNA-0001～LZZ-9999
# HEA-0001～HZZ-9999
# KUA-0001～KZZ-9999
# KQE-0001～KQZ-9999
# SFA-0001～SZZ-9999