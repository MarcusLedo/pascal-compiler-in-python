from pascal import Lexer

interpreter = Lexer("4 - 5 / 7")

token = Lexer.getNextToken(interpreter)

while token.type != 'EOF':
    print(token)
    token = interpreter.getNextToken()