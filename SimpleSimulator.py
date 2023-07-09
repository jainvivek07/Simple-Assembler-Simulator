import sys
import matplotlib.pyplot as plt
import numpy as nm

halt=False
progcnt=0
registers={"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6","111":"flagsregister"}

valuess={"R0":"0000000000000000",
"R1":"0000000000000000",
"R2":"0000000000000000",
"R3":"0000000000000000",
"R4":"0000000000000000",
"R5":"0000000000000000",
"R6":"0000000000000000",
"flagsregister":"0000000000000000"}

mem=[0]*256
j_pc=-1
x=[]
y=[]
z=[]
cycle=0

op = {'add':'10000','sub':'10001','movi':'10010','movr':'10011','ld':'10100','st':'10101','mul':'10110',
'div':'10111','rs':'11000','ls':'11001',
'xor':'11010','or':'11011','and':'11100','not':'11101','cmp':'11110','jmp':'11111','jlt':'01100',
'jgt':'01101','je':'01111','hlt':'01010', 'addf':'00000', 'subf':'00001', 'movf':'00010'}

def float_to_decimal(n):
    x = n[:3]
    y = n[3:]
    x1 = int(x,2)
    x1 += 1
    y1 = "1" + y
    if(x1 > 6):
        ans = y1 + "0"*(6-x1)
        return(int(ans,2))
    elif(x1 == 6):
        ans = y1
        return(int(ans,2))
    elif(x1 < 6):
        q = y1[:x1]
        q2 = y1[x1:]
        qin = int(q,2)
        w = 0
        for i in range (1,len(q2)+1):
            if(q2[i-1] == '1'):
                w += 2**(-i)
            elif(q2[i-1] == "0"):
                pass
        return(qin+w)
    
def decimal_to_floating(n):
    y = int(n)
    y1 = n-y
    ybin = bin(y)
    ybin = ybin[2:]
    exp = len(ybin) - 1
    expbin = bin(exp)[2:]
    if(len(expbin)<=3):
        q = 3 - len(expbin)
        an1 = "0"*q + expbin
    else:
        print("error")
    an = ""
    for d in range (5):
        y1 = y1*2
        if(y1>=1):
            an += "1"
            y1 -= 1
        else:
            an += "0"
    x = ybin + an
    x = x[:5]
    fin = an1 + x
    return fin

def rstflg():
     global valuess
     valuess["flagsregister"]="0000000000000000"
     
def add(rc1,rc2,rc3):
     rstflg()
     global progcnt,valuess
     sum=int(valuess[rc2],2)+int(valuess[rc3],2)
     sum=bin(sum).replace("0b", "")
     if len(sum)<=16:
          while len(sum)!=16:
               sum="0"+sum 
          valuess[rc1]=str(sum)
     elif len(sum)>16:
          valuess[rc1]=str(sum[len(sum)-16:])
          valuess["flagsregister"]="0000000000001000"


def fun1(x):
    sum=0
    for i in range(0,x):
        sum=x**i+sum 
    return sum         
    
def subtract(rc1,rc2,rc3):
     rstflg()
     global progcnt,valuess
     if int(valuess[rc2], 2) < int(valuess[rc3], 2):
          valuess[rc1]="0000000000000000"
          valuess["flagsregister"]="0000000000001000"
     else:
          subtract = bin(int(valuess[rc2], 2)-int(valuess[rc3], 2))
          subtract=subtract[2:]
          while len(subtract)!=16:
           subtract="0"+subtract
          valuess[rc1]=str(subtract)

def go(n,w):
     if n == 1:
          jumpequal(x)
     if n == 2:
          jumpgreater(x)
     if n == 3:
          jumpless(x)
     if n ==4 :
          uncondjump(x)


def rightshift(rc1,value):
    rstflg()
    global progcnt,valuess
    k = valuess[rc1]
    c = int(value,2)
    v= ""
    for i in range(16-c,16):
        v = v + "0"
    v = v + k[:16-c]
    valuess[rc1]= v

def radix_A_to_B (n,A,B):                   
    for i in n:
        if i.isdigit():
            if (ord(i) - 48) >= A :                        
                return ("Invalid Number for Radix A")

        elif i.isalpha():
            i = i.upper() 
            if ord(i) - 55 >= A:
                return ("Invalid Number for Radix A")
    
    d = 0
    c = len(n)-1
    l = []
    for i in n:
        if (ord(i))<65:
            l.append((ord(i))-48)
        else:
            i = i.upper()
            l.append((ord(i))-55)
    s = 0        
    for i in l:
        s += i*(A**c)           
        c -= 1

    l = []
    while s>0 :
        x = s%B
        s = s//B                
        if x>=10:
            x += 55
            x = chr(x)
        l.append(x)
    l.reverse()
    return l


def leftshift(rc1,value):
    rstflg()
    global progcnt,valuess
    k = valuess[rc1]
    c = int(value,2)
    v= ""
    for i in range((16-c),16):
        v = v + "0"
    v =  k[(c) :] + v
    valuess[rc1]= v

def cyclecounter1(x):
    threshold=0
    while not halt:
     formula=threshold+1
    base=1
    final=formula/base

    return (final)

def movi(rc1,im):
     global valuess
     while len(im)!=16:
          im="0"+im
     valuess[rc1]=im
     rstflg()

def mov(rc1,rc2):
     global valuess
     valuess[rc1]=valuess[rc2]
     rstflg()


def rightToLeft(l):     #some problem
    for i in range (len(l)):
        a = 0                       
        b = i                       
        while b>=0:
            z.append(l[a][b])  
            a += 1
            b -= 1

    for i in range (1,len(l)):
        a = i                      
        b = len(l)-1               
        while a<=len(l)-1:
            z.append(l[a][b])    
            a += 1
            b -= 1


def store(rc1,memadr):
     rstflg()
     global valuess,x,y
     mem[int(memadr,2)]= valuess[rc1]
     x.append(cycle)
     y.append(int(memadr,2))

def multiply(rc1,rc2,rc3):
     rstflg()
     mul=int(valuess[rc2],2)*int(valuess[rc3],2)
     mul=bin(mul)
     mul = mul[2:]
     if len(mul)<=16:
          while len(mul)!=16:
               mul="0"+mul
          valuess[rc1]=str(mul)
     elif len(mul)>16:
          valuess[rc1]=str(mul[len(mul)-16:])
          valuess["flagsregister"]="0000000000001000"

def find_root(l):
    x0=int(input("enter x0:")) 
    result=fun1(x0)/10
    while (result.real)>0.0001:
    
        result=fun1(x0)/10
        a=result.real
        x0=x0-a
    print(round(x0))

def divide(rc1,rc2):
     rstflg()
     global valuess
     q=int(int(valuess[rc1], 2) / int(valuess[rc2], 2))
     r=int(valuess[rc1], 2) % int(valuess[rc2], 2)
     q=bin(q)
     q = q[2:]
     while len(q)!=16:
          q="0"+q
     r=bin(r)
     r = r[2:]
     while len(r)!=16:
          r="0"+r
     valuess["R0"]=q
     valuess["R1"]=r

def compare(rc1,rc2):
    rstflg()
    global progcnt,valuess
    if int(valuess[rc1],2) < int(valuess[rc2],2):
          valuess["flagsregister"] = "0000000000000100"
    elif int(valuess[rc1],2) > int(valuess[rc2],2):
          valuess["flagsregister"] = "0000000000000010"  
    elif int(valuess[rc1],2) == int(valuess[rc2],2):
          valuess["flagsregister"] = "0000000000000001"

def load(rc1,memadr):
     rstflg()
     global valuess,x,y
     valuess[rc1]=mem[int(memadr,2)]
     x.append(cycle)
     y.append(int(memadr,2))


def generator(n):
     for i in range (len(n)):           
          ans = x                  
     for k in range (len(n)):
          if z[k] == ans[k]:
               q = 1
          elif ans[k] == "-":
               z.append(0)                
          else:
               z.append(-1)               
          if len(z) == len(z):
               total = sum(z)            
               z.append(total)
     return z

def bitand(rc1,rc2,rc3):
    rstflg()
    global progcnt,valuess

    l = ""
    for i in range(16):
      k =  int(valuess[rc2][i]) & int(valuess[rc3][i])
      l = l + str(k)
    valuess[rc1] = l
    

def bitxor(rc1,rc2,rc3):
    rstflg()
    global progcnt,valuess
    l = ""
    for i in range(0,16):
      k =  int(valuess[rc1][i]) ^ int(valuess[rc2][i])
      l = l + str(k)
    valuess[rc3] = l
   
def alternateTraversal(l):         
    flag = False
    for i in range (len(l)):
        if flag:
          l[i].reverse()     
          flag = not flag
          return l

def bitor(rc1,rc2,rc3):
    rstflg()
    global progcnt,valuess
    l = ""
    for i in range(0,16):
      k =  int(valuess[rc1][i]) | int(valuess[rc2][i])
      l = l + str(k)
    valuess[rc3] = l

def ans_list (q,l):           #Function that returns a list of students' answers
    with open (q,"w") as f:
        for k in range(l):
          f.write(l[k])
          f.write("\n")

def bitnot(rc1,rc2):
    rstflg()
    global progcnt,valuess
    l = ""
    for i in range(0,16):
        if valuess[rc2][i] == "1":
            l = l + "0"
        elif rc1[i] == "0":
            l = l + "1"
    valuess[rc1] = l
    
def uncondjump(memadr):
     rstflg()
     global progcnt,j_pc
     abcd=int(memadr,2)
     j_pc=abcd-1

def jumpless(memadr):
     if valuess["flagsregister"][13]=="1":
          global progcnt,j_pc
          abcd=int(memadr,2)
          j_pc=abcd-1
     rstflg()

def check (n):
     output = []
     for i in range (len(z)):
          a=z[i].split(" ")
          if a[0]=="add":
               count=0
               for g in range(1,len(a)):
                    count=count+1
               if count == 3:
                    if a[1] in z and a[2] in z and a[3] in z:
                         y = op["add"]+"00"+op[a[1]]+op[a[2]]+op[a[3]]
                         output.append(y)

def jumpgreater(memadr):
     if valuess["flagsregister"][14]=="1":
          global progcnt,j_pc
          abcd=int(memadr,2)
          j_pc=abcd-1
     rstflg()

def delayifneeded ():
     pass
     pass
     pass

def jumpequal(memadr):
     if valuess["flagsregister"][15]=="1":
          global progcnt,j_pc
          abcd=int(memadr,2)
          j_pc=abcd-1
     rstflg()

def addf(rc1,rc2,rc3):
     rstflg()
     global progcnt,valuess
     sum=float_to_decimal(valuess[rc2])+float_to_decimal(valuess[rc3])
     sum=bin(sum).replace("0b", "")
     if len(sum)<=16:
          while len(sum)!=16:
               sum="0"+sum 
          valuess[rc1]=str(sum)
     elif len(sum)>16:
          valuess[rc1]=str(sum[len(sum)-16:])
          valuess["flagsregister"]="0000000000001000"

def subf(rc1,rc2,rc3):
     rstflg()
     global progcnt,valuess
     if float_to_decimal(valuess[rc2]) < float_to_decimal(valuess[rc3]):
          valuess[rc1]="0000000000000000"
          valuess["flagsregister"]="0000000000001000"
     else:
          subtract = bin(float_to_decimal(valuess[rc2])-float_to_decimal(valuess[rc3]))
          subtract=subtract[2:]
          while len(subtract)!=16:
           subtract="0"+subtract
          valuess[rc1]=str(subtract)

def movf(rc1,im):
     global valuess
     ime = decimal_to_floating(im)
     while len(ime)!=16:
          ime="0"+ime
     valuess[rc1]=ime
     rstflg()

def mysort(lst):       
    n = len(lst)
    for i in range(n-1):                           
        for j in range(n-i-1):                    
            if lst[j] > lst[j+1]:                 
                lst[j], lst[j+1] = lst[j+1],lst[j]
    return lst
     
def hlt():
     rstflg()
     global progcnt,halt
     halt=True
     
def execute(instruction_using):
     if instruction_using[:5]==op['add']:
          a1,a2,a3 = registers[instruction_using[7:10]],registers[instruction_using[10:13]],registers[instruction_using[13:16]]
          add(a1,a2,a3)

     elif instruction_using[:5]==op['mul']:
          a1,a2,a3 = registers[instruction_using[7:10]],registers[instruction_using[10:13]],registers[instruction_using[13:16]]
          multiply(a1,a2,a3)

     elif instruction_using[:5]==op['div']:
          a1,a2 = registers[instruction_using[10:13]],registers[instruction_using[13:16]]
          divide()

     elif instruction_using[:5]==op['sub']:
          a1,a2,a3 = registers[instruction_using[7:10]],registers[instruction_using[10:13]],registers[instruction_using[13:16]]
          subtract(a1,a2,a3)    

     elif instruction_using[:5]==op['movi']:
          a1,a2 = registers[instruction_using[5:8]],instruction_using[8:16]
          movi()

     elif instruction_using[:5]==op['rs']:
          a1,a2 = registers[instruction_using[5:8]],instruction_using[8:16]
          rightshift(a1,a2)

     elif instruction_using[:5]==op['ls']:
          a1,a2 = registers[instruction_using[5:8]],instruction_using[8:16]
          leftshift(a1,a2)

     elif instruction_using[:5]==op['movr']:
          a1,a2 = registers[instruction_using[10:13]],registers[instruction_using[13:16]]
          mov(a1,a2)

     elif instruction_using[:5]==op['ld']:
          a1,a2 = registers[instruction_using[5:8]],instruction_using[8:16]
          load()

     elif instruction_using[:5]==op['st']:
          a1,a2 = registers[instruction_using[5:8]],instruction_using[8:16]
          store(a1,a2)

     elif instruction_using[:5]==op['cmp']:
          a1,a2 = registers[instruction_using[10:13]],registers[instruction_using[13:16]]
          compare(a1,a2)

     elif instruction_using[:5]==op['and']:
          registers[instruction_using[7:10]],registers[instruction_using[10:13]],registers[instruction_using[13:16]]
          bitand(a1,a2,a3)

     elif instruction_using[:5]==op['or']:
          a1,a2,a3 = registers[instruction_using[7:10]],registers[instruction_using[10:13]],registers[instruction_using[13:16]]
          bitor(a1,a2,a3)

     elif instruction_using[:5]==op['xor']:
          a1,a2,a3 = registers[instruction_using[7:10]],registers[instruction_using[10:13]],registers[instruction_using[13:16]]
          bitxor(a1,a2,a3)

     elif instruction_using[:5]==op['not']:
          a1,a2 = registers[instruction_using[10:13]],registers[instruction_using[13:16]]
          bitnot(a1,a2)

     elif instruction_using[:5]==op['jmp']:
          a1 = instruction_using[8:16]
          uncondjump(a1)

     elif instruction_using[:5]==op['jlt']:
          a1 = instruction_using[8:16]
          jumpless(a1)

     elif instruction_using[:5]==op['jgt']:
          a1 = instruction_using[8:16]
          jumpgreater(a1)

     elif instruction_using[:5]==op['je']:
          jumpequal(instruction_using[8:16])

     elif instruction_using[:5]==op['addf']:
          a1,a2,a3 = registers[instruction_using[7:10]],registers[instruction_using[10:13]],registers[instruction_using[13:16]]
          addf(a1,a2,a3)

     elif instruction_using[:5]==op['subf']:
          a1,a2,a3 = registers[instruction_using[7:10]],registers[instruction_using[10:13]],registers[instruction_using[13:16]]
          subf(a1,a2,a3)

     elif instruction_using[:5]==op['movf']:
          a1,a2 = registers[instruction_using[5:8]],instruction_using[8:16]
          movf(a1,a2)

     elif instruction_using[:5]==op['hlt']:
          hlt()


def pc_rf():
     p=bin(progcnt)
     p = p[2:]
     while len(p)!=8:
          p="0"+p
     outputwrite = p+" "+valuess["R0"]+" "+valuess["R1"]+" "+valuess["R2"]+" "+valuess["R3"]+" "+valuess["R4"]+" "+valuess["R5"]+" "+valuess["R6"]+" "+valuess["flagsregister"]
     sys.stdout.write(outputwrite +"\n")

def main():
     global mem

     input_bin_code = sys.stdin.read()
     abcd=input_bin_code.splitlines()
     for i in range(len(abcd)):
          mem[i]=abcd[i]
     x12 = len(abcd)
     for i in range (len(abcd),256):
          string0 = "0"*16
          mem[i]=string0
        
     global progcnt,j_pc,cycle,x,y

     while not halt:    
          execute(mem[progcnt])
          pc_rf()
          x.append(cycle)
          y.append(progcnt)
          cycle=cycle+1

          if(j_pc==-1):
               progcnt=progcnt+1
          else:
               progcnt=j_pc+1
               j_pc=-1

     for cm in mem:
          sys.stdout.write(cm+"\n")

     graph_x = nm.array(x)
     graph_y = nm.array(y)

     plt.scatter(graph_x, graph_y)
     plt.xlabel("Cycle Number")
     plt.ylabel("Address Accessed")
     plt.show()

if __name__ == '__main__':
     main()