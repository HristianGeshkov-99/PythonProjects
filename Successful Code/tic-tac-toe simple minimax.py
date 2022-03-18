from math import inf as infinity
import platform
from os import system

moveBoard = {1: '1', 2: '2', 3: '3',
             4: '4', 5: '5', 6: '6',
             7: '7', 8: '8', 9: '9'}


newBoard = {1: '-', 2: '-', 3: '-',
            4: '-', 5: '-', 6: '-',
            7: '-', 8: '-', 9: '-'}

HUMAN = "X"
COMP = "O"
winner = None
gameOn = True
currentPlayer = HUMAN


def printBoard(board):
    """
    Print the board on console
    :param board: current state of the board
    """
    print(board[1] + " | " + board[2] + " | " + board[3])
    print("--+---+--")
    print(board[4] + " | " + board[5] + " | " + board[6])
    print("--+---+--")
    print(board[7] + " | " + board[8] + " | " + board[9])


# Take a player input and confirm if it is in the correct range and if the position is free, sets it as the current player
def playerMove(board):
    """
    The Human player selects a valid move and applies it to the board.
    :param board: The current state of the board
    """
    printBoard(moveBoard)
    printBoard(board)
    if currentPlayer == HUMAN:
        try:
            move = int(input("Enter an input from 1-9: "))
            if move >= 1 and move <= 9 and board[move] == '-':
                board[move] = HUMAN
                checkFinalResult(board)
                switchPlayer()
            else:
                clean()
                print("Player is already in that position!")
                playerMove(board)
        except (EOFError, KeyboardInterrupt):
            clean()
            print('Thank you for playing!')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def computerMove(board):
    """
    It calls the minimax function and applies the best move according
    to what it returns.
    :param board: The current state of the board
    """
    if currentPlayer == COMP:
        clean()
        bestScore = -infinity
        bestMove = None
        for i in board.keys():
            if (board[i] == '-'):
                board[i] = COMP
                score = minimax(board, 0, False)
                board[i] = '-'
                if (score > bestScore):
                    bestScore = score
                    bestMove = i
        board[bestMove] = COMP

        checkFinalResult(board)
        switchPlayer()


def checkRow(board):
    """
    Checks if there is a winner on any row
    :param board: The current state of the board
    """
    global winner
    if board[1] == board[2] == board[3] and board[1] != '-':
        winner = board[1]
        return True
    elif board[4] == board[5] == board[6] and board[4] != '-':
        winner = board[4]
        return True
    elif board[7] == board[8] == board[9] and board[7] != '-':
        winner = board[7]
        return True


def checkColumn(board):
    """
    Checks if there is a winner on any column
    :param board: The current state of the board
    """
    global winner
    if board[1] == board[4] == board[7] and board[1] != "-":
        winner = board[1]
        return True
    elif board[2] == board[5] == board[8] and board[2] != "-":
        winner = board[2]
        return True
    elif board[3] == board[6] == board[9] and board[3] != "-":
        winner = board[3]
        return True


def checkDiagonal(board):
    """
    Checks if there is a winner on any diagonal
    :param board: The current state of the board
    """
    global winner
    if board[1] == board[5] == board[9] and board[1] != "-":
        winner = board[1]
        return True
    elif board[3] == board[5] == board[7] and board[3] != "-":
        winner = board[3]
        return True


def checkTie(board):
    """
    Checks if there is draw on the board
    :param board: The current state of the board
    """
    global gameOn
    for i in board.keys():
        if (board[i] == '-'):
            return False
    return True

# check the outcome of the game, if there is a winner -> announce it. If not, it's a tie


def checkWinner(board):
    """
    Checks if there is winner on the board
    :param board: The current state of the board
    :return: the winner value
    """
    global gameOn
    if checkColumn(board) or checkRow(board) or checkDiagonal(board):
        return winner


def checkFinalResult(board):
    """
    Checks what is the final result of the game.
    :param board: The current state of the board
    """
    if checkWinner(board) == COMP:
        clean()
        printBoard(board)
        print("Sorry, the computer won!")
        exit()
    elif checkWinner(board) == HUMAN:
        clean()
        printBoard(board)
        print("Congratulations! You beat the computer!")
        exit()
    elif checkTie(board):
        clean()
        printBoard(board)
        print("DRAW!")
        exit()


def switchPlayer():
    """
    Switches between HUMAN and COMP players
    """
    global currentPlayer
    if currentPlayer == HUMAN:
        currentPlayer = COMP
    else:
        currentPlayer = HUMAN


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def minimax(board, depth, isMaximizing):
    """
    Algorithm function that plays with itself until an end state
    and determines the best move.
    :param board: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9)
    :param isMaximizing: essentially which player turn it is,
    whether they are trying to maximize(COMP) or minimize(HUMAN) their score.
    """
    if checkWinner(board) == HUMAN:
        return -1
    elif checkWinner(board) == COMP:
        return 1
    elif checkTie(board):
        return 0

    if (isMaximizing):
        bestScore = -infinity
        for i in board.keys():
            if (board[i] == '-'):
                board[i] = COMP
                score = minimax(board, depth + 1, False)
                board[i] = '-'
                if (score > bestScore):
                    bestScore = score
        return bestScore

    else:
        bestScore = infinity
        for i in board.keys():
            if (board[i] == '-'):
                board[i] = HUMAN
                score = minimax(board, depth + 1, True)
                board[i] = '-'
                if (score < bestScore):
                    bestScore = score
        return bestScore


def main():
    """
    Main function that calls all functions
    """
    global currentPlayer
    clean()
    first = ''  # if human is the first
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    if first == 'N':
        currentPlayer = COMP
    else:
        currentPlayer = HUMAN

    while gameOn:
        computerMove(newBoard)
        playerMove(newBoard)
        clean()


main()
