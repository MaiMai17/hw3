# python calculator.py
# coding: UTF-8
# 目標:()付きの式を計算できるようにする

def readNumber(line, index): # 数字を読み取る
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index): # +を読み取る
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index): # -を読み取る
    token = {'type': 'MINUS'}
    return token, index + 1

def readMulti(line, index): # *を読み取る
    token = {'type': 'MULTI'}
    return token, index + 1

def readDivision(line, index): # /を読み取る
    token = {'type': 'DIVI'}
    return token, index + 1

def readLeftParenthesis(line, index): # (を読み取る
    token = {'type': 'LEFT'}
    return token, index + 1
    
def readRightParenthesis(line, index): # )を読み取る
    token = {'type': 'RIGHT'}
    return token, index + 1

def readWhitespace(line, index): # 空白文字を読み取る
    token = {'type': 'SPACE'}
    return token, index + 1
    
def readQuit(line, index): # 終了文字'q'を読み取る->強制終了
    token = {'type': 'QUIT'}
    exit(1)

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMulti(line, index)
        elif line[index] == '/':
            (token, index) = readDivision(line, index)
        elif line[index] == '(':
            (token, index) = readLeftParenthesis(line, index)
        elif line[index] == ')':
            (token, index) = readRightParenthesis(line, index)
        elif line[index] == ' ':
            (token, index) = readWhitespace(line, index)
        elif line[index] =='q':
            (token, index) = readQuit(line, index)        
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token) # リストの末尾にtokenを追加する
        # print token
    return tokens


def evaluateMultiAndDivi(tokens): # * / を計算する
    tokens2 = []
    index = 0

    while index < len(tokens): # tokensの端っこまで

        if tokens[index]['type'] == 'NUMBER': # 数字の場合          
            number = tokens[index]['number'] # 数字をnumberに受け取らせ
            if index == len(tokens)-1: # 端っこなら
                token = {'type': 'NUMBER', 'number': number} # tokenに代入
                index += 1 # indexを進める
            else: # 端っこではないなら
                while tokens[index+1]['type'] in {'MULTI', 'DIVI'}: 
                    index += 2
                    if tokens[index-1]['type'] == 'MULTI': # '*' なら
                        number = number * tokens[index]['number']
                    else: # '/' なら
                        number = number*1.0/tokens[index]['number']
                        
                    if index >= len(tokens)-1:
                        break;                    
                token = {'type': 'NUMBER', 'number': number}
                index += 1
                
        elif tokens[index]['type'] in {'PLUS', 'MINUS'}: # 数字ではなく+ - の場合        
            token = {'type': tokens[index]['type']}
            index += 1
            
        else: # それ以外の文字の場合
            print 'Invalid syntax(md_evaluate)'
            exit(1)

        tokens2.append(token) # tokenをtokens2に追加
               
    return tokens2


def evaluatePlusAndMinus(tokens): # + - を計算する
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # 先頭にダミーの+を挿入 <- 先頭に（）ありのときは意味なし？
    index = 1
        
    #tokens2 = md_evaluate(tokens) # * / を計算する
    
    while index < len(tokens):        
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index-1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index-1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print 'Invalid syntax(pm_evaluate)'
                exit(1)
        index += 1
    return answer

def evaluate(tokens): # ()に対応させる用
    answer = 0
    index = 0
    tokens2 = [] # ()の計算部分を格納する
    tokens3 = [] # ()内計算の途中経過を格納する
    ftokens = [] # ()を全部外した状態のtokensが入る
    
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER': # 数字なら          
            number = tokens[index]['number']
            token = {'type': 'NUMBER', 'number': number}
            index += 1
        elif tokens[index]['type'] in {'PLUS', 'MINUS', 'MULTI', 'DIVI', 'LEFT'}: # {+,-,*,/,(} なら
            token = {'type': tokens[index]['type']}
            index += 1
        elif tokens[index]['type'] == 'RIGHT': # tokenが ')' のとき
            range = 1
            while length - range >= 0:
                if ftokens[length - range]['type'] == 'LEFT': # '(' が見つかったら
                    tokens2 = ftokens[length - range +1: length] # ftokens から計算範囲を読み取る
                    del ftokens[length - range : length] # ftokens から()部分を消去
                    #print tokens2
                    tokens3 = evaluateMultiAndDivi(tokens2) # ()を計算する
                    #print tokens3
                    number = evaluatePlusAndMinus(tokens3)
                    token = {'type': 'NUMBER', 'number': number}
                    #print token
                    index += 1
                    break;
                elif length - range == 0: # ')' があるのに、端まで '(' が見つからなかったら
                        print 'It is not a correct fomula. Not Found "("!!'
                        exit(1)
                else:
                    range += 1

        else:
            print 'Invalid syntax(evaluate)'
            exit(1)
    
        ftokens.append(token)
        #print 'ftokens'
        #print ftokens
        length = len(ftokens) # 現在のftokensの長さを保持
    
    if {'type': 'LEFT'} in ftokens: # '(' があるのに、端まで ')' が見つからなかったら
        print 'It is not a correct fomula. Not Found ")"!!'
        exit(1)
    else:
        ftokens = evaluateMultiAndDivi(ftokens)
        answer = evaluatePlusAndMinus(ftokens) # ()がすべて取れた状態の式を計算する
    return answer       

def test(line, expectedAnswer): # テスト用関数
    tokens = tokenize(line)
    actualAnswer = evaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)

def runTest(): # テスト実行関数
    print "==== Test started! ===="
    test("1.0", 1.0q)
    test("-1", -1)
    print ''
    test("1+2", 3)
    test("1.0+2.0", 3)
    test("1-2", -1)
    test("1.0-2.0", -1)
    test("1*2", 2)
    test("1.0*2.0", 2)
    test("1/2", 0.5)
    test("1.0/2.0", 0.5)    
    print ''
    test("1+2*3", 7)
    test("1-2*3", -5)
    test("1+2/3", 5.0/3)
    test("1-2/3", 1.0/3)
    test("1*2+3", 5)
    test("1/2+3", 3.5)
    test("1*2-3", -1)
    test("1/2-3", -2.5)
    print ''
    test("5+6*(6+8)", 89)
    test("8+9/(7+2)", 9)
    test("2*(9+7)*4",128)
    test("(6-4)/(3-2)", 2)
    test("(2-2)*(8-7)", 0)
    test("(9-3)/2-3", 0)
    test("(9-9)*5-3", -3)
    test("(3+1)/(3-1)", 2)
    test("7*(9-9)*7", 0)
    test("(6+9)/5-3", 0)
    test("(1+7)*(8-4)", 32)
    test("(8+4)*9-5", 103)
    test("(2+1)*(8+5)", 39)
    test("8+9/(5-2)", 11)
    test("6+7*(4-2)", 20)
    test("(8+4)/(1+1)", 6)
    test("(1+1)*9+7", 25)
    test("(9+3)/3+5", 9)
    print ''
    test("(2/3-7/3*0.1-0.02)/(31/25)", 1.0/3)
    test("2/3*(3/4-(0.75-1/2))/(3/8)", 8.0/9)
    test("((1/2)/0.25-16/9)/(2/3)", 1.0/3)
    test("((1+2)*(3-4)+5)/(8-6)", 1)
    print "==== Test finished! ====\n"
    
runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print "answer = %f\n" % answer