numbers = (1,2,7,8,9,10,13,17,18,19,20,22,23,24,25,26,42)
nominals = (3,4,5,6,11,12,14,15,16,21,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41)

def findIndex(array, ele):
    i = 0
    while i<len(array):
        if(array[i] == ele):
            return i
        i = i+1
    return -1

temparray = []
fields = []
def sortfload(array):
    i = 0
    if len(array) < 2:
        return
    while i< len(array) -1:
        j = 0
        while j < len(array) - i -1:
            if array[j] > array[j+1]:
                temp = array[j]
                array[j] = array[j+1]
                array[j+1] = temp
            j = j+1
        i = i+1


def strtofloat(array):
    i = 0
    while i<len(array):
        j = 0
        while(j < len(array[i])):
            array[i][j] = float(array[i][j])
            j = j+1
        i = i+1

def strtoint(array):
    i = 0
    while i<len(array):
        array[i][0] = int(array[i][0])
        i =i+1

#==================================
#fields contains attributes chosen
#to classify
#==================================
def findcut(f1):
    global fields
    line = f1.readline()
    while not line.startswith('='):
        line = f1.readline()
    while not line.startswith('attribute'):
        line = f1.readline()
    line = line.replace('attribute23_days','attribute23').replace('attribute24_days','attribute24').replace('attribute25_days','attribute25').replace('\n','').replace('cert_category','').replace(' ','')
    fields = line.split('attribute')
    fields.pop(0)
      
    array = [[] for i in range(len(fields))]
    while not line.startswith('\''):
        line = f1.readline()
    while(1):
        if line.startswith('='):
            break;
        data = line.replace('\'','').replace('(','').replace(']','').split()
        i=0
        while i<len(data) -1:
            index = int(fields[i])
            if index in numbers:
                value = data[i].replace('\'','').replace('(','').replace(']','').replace(')','')
                temp = data[i].replace('\'','').replace('(','').replace(']','').replace(')','')[1:]
                loc = temp.find('-')+1
                left = value[0:loc]
                right = value[loc+1:]
                if (findIndex(array[i],right) == -1) and (right != 'inf'):
                    array[i].append(right)

            i = i+1
        line = f1.readline()
    strtofloat(array)
    j = 0
    while j<len(fields):
        sortfload(array[j])
        j = j+1

    numArray = []
    nominalArray = []
    nominal = []
    i = 0
    while i < len(fields):
        if int(fields[i]) in numbers:
            numArray.append(i)
        else:
            nominalArray.append(i)
        i = i+1
    for e in nominalArray:
        tmp = ['Y','N','A','sha1DSA','sha256RSA','sha384RSA','sha512RSA','md5RSA','sha1RSA','shaRSA']
        nominal.append(tmp)

    return array,numArray,nominalArray,nominal


data_len = 0

def preProcess(f1,cutPoints,numArray,nominalArray,nominal):
    global data_len
    line = f1.readline()
    while not line.startswith('\''):
        line = f1.readline()
    while(1):
        if line.startswith('='):
            break;
        array = []
        data = line.replace('\'','').replace('(','').replace(']','').split()
        i=0
        while i<len(data) -1:

            if not i in nominalArray:
                value = data[i].replace('\'','').replace('(','').replace(']','').replace(')','')
                temp = data[i].replace('\'','').replace('(','').replace(']','').replace(')','')[1:]
                loc = temp.find('-')+1
                left = value[0:loc]
                right = value[loc+1:]
                j = 0
                #index1 = findIndex(numArray,i)
                while(j < len(cutPoints[i])):
                    if cutPoints[i][j] == float(right):
                        break
                    j = j+1
                array.append(j)
            else:
                j = 0
                index2 = findIndex(nominalArray,i)
                while(j<len(nominal[index2])):
                    if nominal[index2][j] == data[i]:
                        break
                    j = j+1
                array.append(j)


            i = i+1

        array.append(data[len(data)-1])
        data_len = len(data)
        temparray.append(array)
        line = f1.readline()

hashArray = []

def hashCode(a):
    i = 0
    hv = 0
    while i<len(a) - 1:
        hv = (int)(hv + (i+1)*5*(int(a[i])+1))
        i = i+1
    return hv

def calHash():
    global data_len
    i = 0
    while i < len(temparray):
        array = []
        hv = hashCode(temparray[i])
        array = [hv, temparray[i][data_len - 1]]
        hashArray.append(array)
        i = i+1

def strtoint(array):
    i = 0
    while i<len(array):
        array[i][0] = int(array[i][0])
        i =i+1

def createArray(f5):
    j = 0
    i = 0
    strtoint(hashArray)
    hashArray.sort()
    while j< len(hashArray):
        while i< hashArray[j][0]:
            f5.write('[\"no result\"],\n')
            i = i+1
        if j == len(hashArray) -1:
            f5.write('[\"'+hashArray[j][1]+'\"]]\n')
        else:
            f5.write('[\"'+hashArray[j][1]+'\"],\n')
        i = i+1
        j = j+1

def ouputArray(f3,array):
    i=0
    while i<len(array):
        j = 0;
        f3.write('[')
        while(j < len(array[i])):
            f3.write(str(array[i][j]) + ',')
            j =j+1
        if i == len(array)-1:
            f3.write(']];\n')
        else:
            f3.write('],\n')
        i = i+1

def ouputArray_2(f3,array):
    i=0
    while i<len(array):
        j = 0;
        f3.write('[')
        while(j < len(array[i])):
            f3.write('"'+str(array[i][j])+'"' + ',')
            j =j+1
        if i == len(array)-1:
            f3.write(']];\n')
        else:
            f3.write('],\n')
        i = i+1

def printRemain(f6,cutPoints,numArray,nominalArray,nominal):
    i = 0
    aa = []
    na = []
    while i < len(fields):
        if int(fields[i]) in numbers:
            aa.append(int(fields[i]))
        else:
            na.append(int(fields[i]))
        i = i+1
    f6.write('var attArray = new Array(')
    i = 0
    while i < len(fields)-1:
        f6.write(fields[i]+',')
        i = i+1
    f6.write(fields[i]+');\n')

    if len(na) > 0:
        i = 0
        f6.write('var nominalArray = new Array(')
        while i < len(na)-1:
            f6.write(str(na[i])+',')
            i = i+1
        f6.write(str(na[i])+');\n')
    else:
        f6.write('var nominalArray = new Array();\n')

    f6.write('var cutPoints = [')
    ouputArray(f6,cutPoints)
    
    if len(na) == 0:
        f6.write('var nominal = [];\n')
    else:
        f6.write('var nominal = [')
        ouputArray_2(f6,nominal)

    f6.write('function findIndex(array, ele) {\nvar i = 0;\nwhile(i<array.length) {\nif(array[i] == ele) return i;\ni++;\n}\nreturn -1;\n}\n')
    f6.write('function convertData(attr) {\n\
    var i = 1;\n\
    while(i<attr.length) {\n                           var index_1 = findIndex(attArray,i);\n\
        if(index_1 > -1) {\n\
            var index_2 = findIndex(nominalArray,i);\n\
            if(index_2 == -1) {\n\
                var j = 0;\n\
                while(j<cutPoints[index_1].length -1) {\n if(attr[i]<cutPoints[index_1][j]) break;\n  j++;\n}\n   attr[i] = j;\n\
            }\n\
            else {\n\
                var k = 0;\n\
                while(k<nominal[index_2].length) {\n\
                    if(attr[i] == nominal[index_2][k]) {\n\
                        break;\n\
                    }\n\
                    k++;\n\
                }\n\
                attr[i] = k;\n\
            }       \n\
        }\n\
                i++;\n\
        \
    }\n\
}\n')

    f6.write('function hashCode(a) {\n\
    var i = 1;\n\
    var hv = 0;\n\
    var j = 1;\n\
    while(i<a.length) {\n\
        index = findIndex(attArray,i);\n\
        if(index > -1) {\n\
            hv = hv+ j * 5 *(a[i]+1);\n\
            j++;\n\
        }\n\
        i ++;\n\
\n\
    }\n\
    //document.write(hv+" ");\n\
    return hv;\n\
    \n\
}\n')

    f6.write('function run() {\n\
    var i = 0;\n\
     while(i < 1) {\n\
            convertData(attr[i]);\n\
            var index = hashCode(attr[i]);\n\
            var t = hashTable[index][0];    \n\
                        document.write(t+" ");\n\
            i++;        \n\
            \n\
    }\n\
    \n\
    \n\
}\n')
if __name__ == '__main__':
    
    f4 = open('../DT.txt','r')
    f6 = open('../DTtest.js','w')
    f5 = open('../DT.txt','r')
    a1,a2,a3,a4 = findcut(f4)
    preProcess(f5,a1,a2,a3,a4)
    calHash()
    f6.write('var hashTable = [')
    createArray(f6)
    printRemain(f6,a1,a2,a3,a4)

