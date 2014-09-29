def FindCategoryNum(f3):
    lines = f3.readlines()
    for l in lines:
        if l.startswith('@attribute cert_category'):
            fields = l.split(' ')
            categories = fields[2].replace('\n','').replace('{','').replace('}','').split(',')
            return categories

def calValue(f1,f2,f3):
    f2.write('function decide_class(attr) {\nvar container = new Array();\n')
    f2.write('var i = 0;\n')
    categories = FindCategoryNum(f3)
    f2.write('while(i < %d) container[i++] = 0;\n' %(len(categories)))
    line = f1.readline();
    i = 0
    while(1):
        while not line.startswith("Class "):
            if line == '':
                f2.write('var i=0;\n')
                f2.write('var index = 0;\nvar max = -10000;\n')
                f2.write('while(i < %d) {\n' %(len(categories)))
                f2.write('if(container[i] > max) {\nmax = container[i];\nindex=i;}\ni++;}\n')
                f2.write('if(index == 0) return "%s";\n' %(categories[0]))
                i = 1
                while i < len(categories):
                    f2.write('else if(index == %d) return "%s";\n' %(i,categories[i]))
                    i = i+1
                f2.write('}')
                return
            line = f1.readline()
        line = f1.readline()
        data = line.split()
        f2.write('container['+str(i)+'] = ' + data[0] +';\n')
        line = f1.readline()
        while line != '\n':
            data = line.split()
            data[0] = data[0].replace(']','').replace('[','')
            index = data[0][9:11]
            val = data[0][12:]
            if len(data[0]) > 11 and data[0][11] == '=':
                f2.write('if(attr[' + index + '] == '+ '\"'+val + '\"'+') container['+str(i)+']+= 1'+data[1]+ '('+data[2]+')'+';\n')
            else:
                if index in ('1','2','7','8','9','10','13','17','18','19','20','22','23','24','25','26','42'):
                    f2.write('container[' + str(i) +'] += ' + 'attr[' + index + ']'+data[1] +'('+data[2]+')' +';\n')
                else:
                    f2.write('container[' + str(i) +'] += ' + '1'+data[1] +'('+data[2]+')' +';\n')
            line = f1.readline()

        i = i+1









if __name__ == '__main__':
    f1 = open('../SL.txt','r')
    f2 = open('SLtest.js','w')
    f3 = open('../SL.txt','r')

    calValue(f1,f2,f3)

