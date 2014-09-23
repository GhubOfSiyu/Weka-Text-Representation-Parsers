
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
    temp1 = temp.replace('.','').replace('-','')
    if temp1.isdigit():
        f2.write(temp)
        f2.write(")")
    else:
        f2.write("\"")
        f2.write(temp)
        f2.write('\")')
    if len(data) > 3:
        f2.write("{\n   ")
        f2.write(" "*(interval+4))
        f2.write("container[i] = \"")
        f2.write(data[4])
        f2.write('\";')
        f2.write("\n")
    else:
        f2.write("{\n   ")

def iore(prev, now):
    if prev < now:
        return 1
    else:
        return 0

categories = []
def loopTree(f1, f2):
    global categories
    category_num = 0
    indent = 0
    index = 3
    line = f1.readline()[indent:]
    while(1):
        while not line.startswith("RandomTree"):
            if line.startswith("@attribute cert_category"):
                line = line.replace('{','').replace('}','').replace('\n','')
                categories = line.split(' ')[2]
                categories = categories.split(',')              
            if line == '':
                return
            line = f1.readline()[indent:]
        f1.readline()
        f1.readline()
        line = f1.readline()
        flag = 1
        while line.startswith("attribute"):
            parseline(f2,line,index,0,flag)
            flag = 0
            #f2.write(line)
            prev = SyNum(line)
            line = f1.readline()
            N = 1
            while 1:
                length = SyNum(line)
                if N==0:
                    break
                elif length == N:
                    flag = iore(prev,length)
                    parseline(f2,line,index,length,flag)
                    #f2.write(line)
                    prev = length
                    line = f1.readline()
                    N = N+1
                else:
                    f2.write(" "*(4*N))
                    N = N-1
                    f2.write("}\n")
        f2.write('i++;\n')
        f2.write("\n")

def beginParse(f1, f2):
    f2.write("function decide_class(attribute) {\n")
    f2.write('var container = new Array();\n var i = 0;\n')
    loopTree(f1,f2)
    f2.write("result = [")
    #at least two categories
    i = 0
    while i < len(categories)-1:
        f2.write("0,")
        i = i+1
    f2.write("0]\n")
    f2.write ("var j = 0;\n    while(j<i) {\n")
    f2.write('if(container[j] == "%s") result[0]++;\n' %(categories[0]))
    i = 1
    while i < len(categories):
        f2.write('else if(container[j] == "%s") result[%d]++;\n' %(categories[i],i))
        i = i+1
    f2.write('j++;\n}\n')
    f2.write('var k = 0;\n var index = 0;\n var max = 0;\n')
    f2.write('while(k<%d) {\n if(result[k]>max) {\n max =result[k];\n index = k;\n }\n k++;\n}\n' %(len(categories)))
    f2.write('if(index == 0) return "%s";\n' %(categories[0]))
    i = 1
    while i < len(categories):
        f2.write('else if(index == %d) return "%s";\n' %(i,categories[i]))
        i = i+1
    f2.write('}')






if __name__ == '__main__':

    f1 = open('../RF.txt','r')
    f2 = open('RFtest.js','w')
    #test(f1,f2)
    #parseTree(f1,f2)
    beginParse(f1,f2)
    #recurTree(f1,f2, f1.readline(),0)
