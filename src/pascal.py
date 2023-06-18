# Token types
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
EOF = 'EOF'
LPAREN = '('
RPAREN = ')'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    # Representação do objeto em string
    # Token(INTEGER, 3)
    # Token(PLUS, '+')
    
    def __str__(self):
        return 'Token({type}, {value})'.format(
            type = self.type,
            value = repr(self.value)
        )
    
    def __repr__(self):
        return self.__str__()
    
class Lexer:
    def __init__(self, text):
        # Input/Source
        self.text = text
        # Posição do cursor
        self.pos = 0
        self.currentChar = self.text[self.pos]

    def error(self):
        raise Exception("Error parsing input")
    
    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.currentChar = None #EOF
        else:
            self.currentChar = self.text[self.pos]

    
    def skipWhitespace(self):
        while self.currentChar is not None and self.currentChar.isspace():
            self.advance()

    def integer(self):
        #Retorna um inteiro multidigito
        result = ''
        while self.currentChar is not None and self.currentChar.isdigit():
            result += self.currentChar
            self.advance()
        return int(result)
    
    def getNextToken(self):

        while self.currentChar is not None:
            if self.currentChar.isspace():
                self.skipWhitespace()
                continue

            if self.currentChar.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.currentChar == '+':
                self.advance()
                return Token(PLUS, '+')
            
            if self.currentChar == '-':
                self.advance()
                return Token(MINUS, '-')
            
            if self.currentChar == '*':
                self.advance()
                return Token(MUL, '*')
            
            if self.currentChar == '/':
                self.advance()
                return Token(DIV, '/')
            
            if self.currentChar == '(':
                self.advance()
                return Token(LPAREN, '(')
            
            if self.currentChar == ')':
                self.advance()
                return Token(RPAREN, ')')
        
        #self.error()

        return Token(EOF, None)

class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        # Recebe o primeiro token do input
        self.currentToken = self.lexer.getNextToken()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, tokenType):
        # compara o token type com o tokenType passado como argumento
        # se eles combinarem, então "eat" o token atual e avança para
        # o próximo token no self.currentToken, caso contrário, exceção

        if self.currentToken.type == tokenType:
            self.currentToken = self.lexer.getNextToken()
        else:
            self.error()

    def factor(self):
        token = self.currentToken
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
    
    def term(self):
        # Term tem prioridade por ser multiplicação
        result = self.factor()

        while self.currentToken.type in (MUL, DIV):
            token = self.currentToken
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()

        return result

    def expr(self):
        # expr := INTEGER PLUS INTEGER
        # expr := INTEGER MINUS INTEGER
        # Primeiro do token do input

        #^^^prioridade
        result = self.term() # resultado da multiplicaçAo ou divisão

        while self.currentToken.type in (PLUS, MINUS):
            token = self.currentToken
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result
    

def main():
    source = "7 + 3"

    lexer = Lexer(source)
    interpreter = Interpreter(lexer)
    result = interpreter.expr()
    print(result)


if __name__ == "__main__":
    main()