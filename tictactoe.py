import random
import argparse

class TicTacToe:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.turn = random.choice(['O', 'X'])
        self.board = [['#' for _ in range(3)] for _ in range(3)]
        
    def play(self, index, letter):
        x = index // 3
        y = index % 3
        
        if self.board[x][y] != '#':
            print(f'{letter} at {(x, y)} is a Invalid Move!')
        elif self.turn != letter:
            print(f'{letter} it is not your turn yet.')
        else:
            self.board[x][y] = letter
            self.turn = "O" if letter == "X" else "X"
            
        return self.gameset(), self.draw()
        
    def gameset(self):
        for index in range(3):
            if self.board[index][0] == self.board[index][1] == self.board[index][2] != '#':
                return True
                
            if self.board[0][index] == self.board[1][index] == self.board[2][index] != '#':
                return True
                
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '#':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '#':
            return True
            
        return False
            
    def draw(self):
        for item in self.board:
            if '#' in item:
                return False
                
        return True
        
    def render(self):
        for index in range(3):
            print(f"   {self.board[index][0]} | {self.board[index][1]} | {self.board[index][2]} ")
            if index != 2:
                print("  ---+---+--- ")
                
        print()
            
class Player:
    def __init__(self, letter: str):
        self.letter = letter
        self.isAI = False
        
    def getInput(self):
        try:
            index = int(input('What is your move? (0 - 8): '))
            if 0 <= index <= 8:
                return index
            else:
                print('Invalid! The choice must be between 0 and 8.')
                return None
        except ValueError:
            print('That is not a valid index.')
            return None
            
class AI:
    def __init__(self, letter: str, epsilon: float):
        self.letter = letter
        self.opponent = "O" if letter == 'X' else 'X'
        
        self.isAI = True
        self.epsilon = epsilon
        
    def getInput(self, board):
        avail = self.avail(board)
        if len(avail) == 9 or random.random() < self.epsilon:
            bx, by = random.choice(avail)
            return self.logger(bx, by)
        
        bestVal = float('-inf')
        bx = -1
        by = -1
        
        for x, y in avail:
            if board[x][y] == '#':
                board[x][y] = self.letter
                
                moveVal = self.minimax(board, 0, False)
                board[x][y] = '#'
                
                if moveVal > bestVal:
                    bx = x
                    by = y
                    bestVal = moveVal
        
        return self.logger(bx, by)
        
    def logger(self, bx, by):
        move = bx * 3 + by
        print(f'AI: {self.letter} at {move}')
        return move
        
    def avail(self, board):
        pos = []
        for x in range(3):
            for y in range(3):
                if board[x][y] == '#':
                    pos.append((x, y))
        
        return pos
        
    def evaluate(self, board):
        for index in range(3):
            if board[index][0] == board[index][1] == board[index][2] != '#':
                return 1 if board[index][0] == self.letter else -1
                
            if board[0][index] == board[1][index] == board[2][index] != '#':
                return 1 if board[0][index] == self.letter else -1
                
        if board[0][0] == board[1][1] == board[2][2] != '#':
            return 1 if board[0][0] == self.letter else -1
        if board[0][2] == board[1][1] == board[2][0] != '#':
            return 1 if board[0][2] == self.letter else -1
            
        return 0
        
    # https://www.geeksforgeeks.org/dsa/finding-optimal-move-in-tic-tac-toe-using-minimax-algorithm-in-game-theory/
    # I modified it a bit with avail function so its not aiming at anywhere
    def minimax(self, board, depth, isMax):
        score = self.evaluate(board)
        
        if score == 1:
            return score - (depth * 0.1)
            
        if score == -1:
            return score + (depth * 0.1)
            
        avail = self.avail(board)
        if not avail:
            return 0
            
        if isMax:
            best = float('-inf')
            for x, y in avail:
                board[x][y] = self.letter
                best = max(best, self.minimax(board, depth+1, not isMax));
                
                board[x][y] = '#'
            return best
        else:
            best = float('inf')
            for x, y in avail:
                board[x][y] = self.opponent
                best = min(best, self.minimax(board, depth + 1, not isMax))
                
                board[x][y] = '#'
            return best
            
def play(t, x, o, log=True):
    if log:
        t.render()
        
    subInput = lambda x: x.getInput(t.board) if x.isAI else x.getInput()
    while True:    
        if 'X' == t.turn:
            index = subInput(x)
            letter = x.letter
        else:
            index = subInput(o)
            letter = o.letter
            
        if index is None:
            continue
        gameset, draw = t.play(index, letter)
        
        if log:
            t.render()
        
        if gameset:
            if log:
                print(f'{letter} has won the game!')
            break
        elif draw:
            if log:
                print("It's a draw!")
            break

def playerVsAI(epsilon: float):
    x = Player('X')
    o = AI('O', epsilon)
    t = TicTacToe()
    while True:
        play(t, x, o, log=True)
        if not input('Do you want to play again? (Enter/Any): '):
            t.reset()
        else:
            print('Thank you for playing!')
            break
        
def aiVsai(epsilon: float):
    x = AI('X', epsilon)
    o = AI('O', epsilon)
    t = TicTacToe()
    play(t, x, o, log=True)
    
def playerVsplayer():
    x = Player('X')
    o = Player('O')
    t = TicTacToe()
    while True:
        play(t, x, o, log=True)
        if not input('Do you want to play again? (Enter/Any): '):
            t.reset()
        else:
            print('Thank you for playing!')
            break
        
def main():
    parser = argparse.ArgumentParser(description='Play TicTacToe!')
    parser.add_argument('--mode', choices=['pvp', 'pvai', 'aivai'], default='pvai')
    parser.add_argument('--level', type=int, default=2, choices=range(0, 4), help='AI difficulty: 0=Easy, 1=Medium, 2=Hard, 3=Impossible (perfect)')
    args = parser.parse_args()
    
    DIFFICULTY = {
        0: 0.5,     # Easy
        1: 0.2,     # Medium
        2: 0.05,    # Hard
        3: 0.0,     #Imposible
    }
    epsilon = DIFFICULTY[args.level]
    if args.mode == 'pvp':
        playerVsplayer()
    elif args.mode == 'pvai':
        playerVsAI(epsilon)
    elif args.mode == 'aivai':
        aiVsai(epsilon)
        
if __name__ == "__main__":
    main()