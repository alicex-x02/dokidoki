#set 자료형: 변수 목록에서 중복 제거 용도
var = set()

#연산자 우선 순위 함수
#우선 순위 매겨서 return
def operator_priority(op):
    if op == '¬':
        return 5
    if op == '∧':
        return 4
    if op == '∨':
        return 3
    if op == '⊕':
        return 2
    if op == '→':
        return 1
    if op == '↔':
        return 0
    
    return -1


#연산자 계산 함수
#단항 연산일때는 num2=False
#연산해서 결과값을 return
def operator_exec(op, num1, num2=False):
    if op == '¬':
        return not num1
    if op == '∧':
        return num1 and num2
    if op == '∨':
        return num1 or num2
    if op == '⊕':
        return not num1 and num2 or num1 and not num2 
    if op == '→':
        return not num2 or num1
    if op == '↔':
        return (not num2 or num1) and (not num1 or num2)
    
    return False

#중위 표기 -> 후위 표기 변환 함수
def conversion(expression):
    global var

    ret = ""        #변환된 후위 표기식
    stack = []      #stack을 list로 구현
    for i in expression:        #명제를 반복문으로 하나씩 읽음
        if i.isalpha():         #isalpha: 읽은 값이 알파벳인 경우 -> 변수
            var.add(i)          #변수 목록 var에 i를 추가
            ret += i            #후위표기식 ret에 i를 추가
        elif (len(stack)==0)or(operator_priority(i)>operator_priority(stack[-1])):                  #stack이 비어있거나 연산자 i의 우선순위가 stack의 top보다 높으면
            stack.append(i)                                                                         #i를 stack에 push
        else:
            while (len(stack) != 0) and (operator_priority(i)<=operator_priority(stack[-1])):       #stack이 비어있지 않고 연산자 i의 우선순위가 stack의 top보다 작거나 같으면
                ret+=stack.pop()                                                                    #stack이 비거나 i의 우선 순위가 더 커질때까지 stack에서 pop한 값을 후위표기식에 추가
            stack.append(i)                                                                         #i를 stack에 push
    while (len(stack)!=0):                                                                          #stack이 빌때까지
        ret += stack.pop()                                                                          #후위표기식 ret에 stack.pop()값을 추가

    var = list(var)             #set 자료형 var를 list로 변환
    var.sort(reverse=True)      #정렬

    return ret                  #후위표기식 ret을 return

#후위 표기식 계산 함수
def create_table(k, expression):                                                                    #몇번째 행인지를 나타내는 k랑 후위표기식 expression을 받음
    table={}                                                                                        #dictionary table을 선언
    stack =[]                                                                                       #list로 stack을 구현
    for i in expression:                                                                            #후위표기식 expression을 하나씩 읽음
        if i.isalpha():                                                                             #i가 알파벳이면 변수
            for j in range(len(var)):                                                               #list var에서 들어온 i가 몇번째인지 찾는 로직 
                if var[j] == i:                                                                     
                    table[i] = not(k & (1 << j))                                                    #2^j과 k를 비트단위 and 연산
            stack.append(i)                                                                         #변수 i를 stack에 push
        elif i=='¬':                                                                                #연산자가 not일때
            temp = i + stack[-1]                                                                    #temp = 중위표기식으로 되돌린 표현: 연산자 (not) + 변수 를 저장
            table[temp] = operator_exec(i, table[stack.pop()])                                      #연산 결과를 dictionary table에 등록
            stack.append(temp)                                                                      #변환식 temp를 stack에 push
        else:                                                                                       #not말고 다른 연산자들인 경우 -> 다항 연산
            num1 = stack.pop()                                                                      #첫번째 연산 대상 pop
            num2 = stack.pop()                                                                      #두번째 연산 대상 pop

            temp = num2 + i + num1                                                                  #temp = 중위표기식으로 되돌린 표현: 변수 + 연산자 + 변수 를 저장
            table[temp] = operator_exec(i, table[num1], table[num2])                                #연산 결과를 dictionary table에 등록
            stack.append(temp)                                                                      #변환식 temp를 stack에 push

            if i=='↔':                                                                              #쌍방 조건 명제
                table[num2 + '→' + num1] = operator_exec('→', num1, num2)                           #중간 과정을 dictionary table에 저장
                table[num2 + '←' + num1] = operator_exec('←', num1, num2)                           

    ret = sorted(table.items(), key = lambda item: (len(item[0]), item[0]))                         #보기 깔끔하게 출력되도록 논리식 정렬
    return ret                                                                                      #최종 결과값 list ret을 return

#출력 형식 함수
def print_tf(x):
    print("T" if x else "F", end='\t')                                                              #삼항연산자 사용해서 T/F 형식으로 출력

#파일 입력
file = open('C:/Users/iamal/Desktop/파이썬/test2.txt', encoding='utf-8')                  #명제가 담긴 파일을 읽어오기

for line in file:                                                                                   #파일 내용을 한줄씩 읽어오기
    post = conversion(line)                                                                         #줄에 있는걸 "중위 표기 -> 후위 표기 변환 함수"에 삽입

    for i in range(2**len(var)):                                                                    #2^(변수 갯수) 만큼 연산 수행
        table = create_table(i, post)                                                               #후위표기식을 "후위 표기식 계산 함수"에 삽입

        if i == 0:
            for e in table:                                                                         #논리식을 출력
                print(e[0], end="\t")                                                               #사이 공백
            print()
    
        for e in table:
            print_tf(e[1])                                                                          #연산 결과
        print()
