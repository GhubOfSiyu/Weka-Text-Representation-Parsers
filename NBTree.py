import sys
import math

def isNum(value):
    try:
        value + 1
    except TypeError:
        return False
    else:
        return True

def SyNum(str):
    index = 0
    data = str.split(" ")
    num = 0
    while data[index] == '|' or data[index] == '':
        if(data[index] == '|'):
            num +=1
        index = index+1
    return num

flag = list()
for i in range(0,500):
    flag.append(0)
    i = i+1

def parseline(f2, line, index, place, flag):
    interval = 4*place
    if flag == 1:
        f2.write(" "*interval)
        f2.write("if")
    else:
        f2.write(" "*interval)
        f2.write("else if")

    line = line[4*place:]
    data = line.split(' ')

    f2.write('(')
    attNum = data[0].replace("_days","").replace("_num","")[9:]

    f2.write("attribute[")
    f2.write(attNum)
    f2.write(']')
    t = data[1]
    if data[1] == "=":
        t = "=="
    f2.write(t)
    temp = data[2].replace(':','').replace('\n','')
    if temp.replace('.','').replace('-','').isdigit():
        f2.write(temp)
    else:
        f2.write('\"'+temp+'\"')
    f2.write(')')
    if ":" in data[2]:
        f2.write("{\n   ")
        f2.write(" "*(interval+4))
        #f2.write("NB = ")
        nbValue = data[4].replace('\n','')
       # f2.write(nbValue)
       # f2.write(";")
        #f2.write("\n")
        #f2.write(" "*(interval+4))
        f2.write("return " + nbValue+";")
        f2.write('\n')
    else:
        f2.write("{\n   ")

def iore(prev, now):
    if prev < now:
        return 1
    else:
        return 0


def loopTree(f1, f2):
    indent = 0
    index = 3
    line = f1.readline()[indent:]
    while not line.startswith("attribute"):
        line = f1.readline()[indent:]
    flag = 1
    while line.startswith("attribute"):
        parseline(f2,line,index,0,flag)
        flag = 0
        #f2.write(line)
        prev = SyNum(line)
        line = f1.readline()
        N = 1
        while 1:
            len = SyNum(line)
            if N==0:
                break
            elif len == N:
                flag = iore(prev,len)
                parseline(f2,line,index,len,flag)
                #f2.write(line)
                prev = len
                line = f1.readline()
                N = N+1
            else:
                f2.write(" "*(4*N))
                N = N-1
                f2.write("}\n")
    f2.write('}')
    f2.write("\n")


def FindCategoryNum(f3):
    lines = f3.readlines()
    for l in lines:
        if l.startswith('@attribute cert_category'):
            fields = l.split(' ')
            categories = fields[2].replace('\n','').replace('{','').replace('}','').split(',')
            return categories

def decClass(f1,f2,f3):
    cert_categories = FindCategoryNum(f3)
    f2.write('function decide_class(attribute){\n var NB = decide_branch(attribute);\n')
    line = f1.readline()
    while not line.startswith("Leaf"):
            line = f1.readline()
    data = line.split()
    f2.write('if(NB == ')
    f2.write(data[2])
    f2.write('){\n')
    f1.readline()
    f1.readline()
    f1.readline()
    line = f1.readline()
    line = line.replace('(','').replace(')','')
    dataIndex = line.split()
    index = 0
    num = 0
    max = 0
    while(num < len(cert_categories)):
        if float(dataIndex[num]) > max:
            max = float(dataIndex[num])
            index = num
        num = num+1
    flag = cert_categories[index]
    f2.write('return ')
    f2.write('"'+flag+'"')
    f2.write(';}\n')
    while(1):
        while not line.startswith("Leaf"):
            if line == '':
                return
            line = f1.readline()
        data = line.split()
        f2.write('else if(NB == ')
        f2.write(data[2])
        f2.write('){\n')
        f1.readline()
        f1.readline()
        f1.readline()
        line = f1.readline()
        line = line.replace('(','').replace(')','')
        dataIndex = line.split()
        index = 0
        num = 0
        max = 0
        while(num < len(cert_categories)):
                if float(dataIndex[num]) > max:
                    max = float(dataIndex[num])
                    index = num
                num = num+1
        flag = cert_categories[index]
        f2.write('return ')
        f2.write('"'+flag+'"')
        f2.write(';}\n')









def beginParse(f1,f2,f3):
    f2.write("function decide_branch(attribute) {\n")
    #f2.write("var NB;")
    #f2.write("\n")
    loopTree(f1,f2)
    decClass(f1,f2,f3)
    f2.write("}\n")

    f2.write("function run()\n\
{\n\
   \n\
     \n\
   var i = 0;\n\
    while(i < 1) {     \n\
      var t = decide_class(attr[i]);  \n\
      document.write(t + ',')\n\
      i++;    \n\
  }\n\
\n\
}\n")   


if __name__ == '__main__':

    f1 = open('../NBTree.txt','r')
    f2 = open('../NBtest.js','w')
    f3 = open('../NBTree.txt','r')
    beginParse(f1,f2,f3)
  
