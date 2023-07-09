from sys import stdin

def decimal_to_binary(n):
    l = []
    if n.isdigit():
        n = int(n)
    else:
        return ("Invalid Decimal.")
    while n>0 :
        a = n%2
        n = n//2
        l.append(a)
    l.reverse()
    return l

def func(n):
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

op = {'add':'10000','sub':'10001','movi':'10010','movr':'10011','ld':'10100','st':'10101','mul':'10110',
'div':'10111','rs':'11000','ls':'11001',
'xor':'11010','or':'11011','and':'11100','not':'11101','cmp':'11110','jmp':'11111','jlt':'01100',
'jgt':'01101','je':'01111','hlt':'01010', 'addf':'00000', 'subf':'00001', 'movf':'00010',
'r0':'000','r1':'001','r2':'010','r3':'011','r4':'100','r5':'101','r6':'110','flags':'111'}
flg=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# reg=['R0','R1','R2','R3','R4','R5','R6']
reg=['r0','r1','r2','r3','r4','r5','r6']
var_count=0
instruction_count=0
line_counter=[]
l_input=[]
while(True):
    try:
        ax=input()
        ax5 = ax.split()
        # if ax != "" or ax != "\n" or ax != "\t" or ax != " ":
        if ax5 != []:
            axx = ""
            for i in ax:
                if i.isalpha():
                    axx += i.lower()
                    # i = i.lower()
                else:
                    # ax[i] = ax[i]
                    axx += i
            ax3 = axx.split()
            ax4 = " ".join(ax3)
            instruction_count+=1
            l_input.append(ax4)
    except EOFError:
        break
    except KeyboardInterrupt:
        break

ins_c_1 = instruction_count
# for i in stdin:
# 	# try:
#     if i == []:
#         continue
#     l1 = input().split()
#     l_input.append(l1)
# 	# except EOFError:
#     #     break
#     # except KeyboardInterrupt:
# 	# 	break
    
len_input=len(l_input)
var_name=[]
var_value=[]
label_name=[]
label_position=[]
w = []
count = 0

if len_input == 0:
    print("ERROR : No instructions given.")
    quit()

for i in range (len_input):
    if l_input[i] == "hlt":
        count += 1
        w.append(i+1)

if count != 1 and count != 0:
    print(f"ERROR : More than one halt statement present in the code in the lines :",*w,".",sep=" ")
    quit()

haha = l_input[-1].split()

if count == 1:
    if haha[-1] != "hlt":
        for n in range(len(l_input)):
            if l_input[n] == "hlt":
                print(f"ERROR: Halt statement present in line {n+1}, It should be in the last line i.e. line {ins_c_1}")
                quit()

if l_input[-1]=="hlt" or haha[-1]=="hlt":
    # for i in range(len_input):
    vc=0
    if l_input[0][0:3] == "var":
        k = 0
        count=0
        # for j in range(1,len(l_input[i])):
        while(l_input[k][0:3] == "var" and l_input[k][3] == " "):
            count=count+1
            # if count == 1:
            ins_sp = l_input[k].split(" ")
            if(len(ins_sp) == 2):
                vc+=1
                k+=1
    

        

    for i in range(len_input):
        ins_sp = l_input[i].split(" ")
        if ins_sp[0] != "var" and ins_sp[0] not in op and ins_sp[0] != "mov" and "\t" not in ins_sp[0]:
            if ins_sp[0][-1]==":" and ins_sp[0][-2] != " ":
                if ins_sp[0][:-1] not in op:
                    l_input_slice=ins_sp[0][:-1]
                    label_name.append(l_input_slice)
                    # x = i + 1
                    x=i-vc
                    label_position.append(x)
                else:
                    print(f"ERROR : reserved keyword used as label name in line {i+1}")
                    quit()
            else:
                print(f"ERROR : label name incorrectly initialised in line {i+1}")
                quit()

    for i in range (len_input):
        ins_sp = l_input[i].split()
        for j in range (len(label_name)):
            if(ins_sp[0][:-1] == label_name[j]):
                x = len(label_name[j])
                ins_sp = ins_sp[1:]
                # for k in range (len(ins_sp)):
                y = " ".join(ins_sp)
                l_input[i] = y

    # if l_input[0][0:3] == "var" and l_input[0][3] == " ":
    if l_input[0][0:3] == "var" and l_input[0] not in label_name:
        k = 0
        count=0
        # for j in range(1,len(l_input[i])):
        while(l_input[k][0:3] == "var" and l_input[k][3] == " "):
            count=count+1
            # if count == 1:
            ins_sp = l_input[k].split(" ")
            if(len(ins_sp) == 2):
                var_count+=1
                var_name.append(ins_sp[1])
                instruction_count-=1
                k += 1
            else:
                print(f"ERROR : incorrect initialisation of variable in line {k+1}.")
                quit()

        dup_var = []
        newlst = []
        for i in range (var_count):
            if var_name[i] not in newlst:
                newlst.append(var_name[i])
            else:
                print(f"ERROR : variable {var_name[i]} initialised more than once (initialised again in line {i+1}).")
                quit()
        ic1=instruction_count
        # ic1 += 1
        for i in range(var_count):
            var_value.append(ic1+i)

        var_dict = dict(zip(var_name,var_value))

    if l_input[0][0:3] == "var" and l_input[0][3] == " ":        #check var in mid
        k = 0
        count=0
        while(l_input[k][0:3] == "var"):
            count=count+1
            k += 1
        for m in range(k,len_input):
            if l_input[m][0:3] == "var" and l_input[m][3] == " ":
                print(f"ERROR : variable initialised at wrong place at line {m+1}")
                quit()

    output = []
    for i in range(var_count,instruction_count+var_count):
        a=l_input[i].split(" ")
        if a[0]=="add":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count == 3:
                if a[1] in reg and a[2] in reg and a[3] in reg:
                    y = op["add"]+"00"+op[a[1]]+op[a[2]]+op[a[3]]
                    output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i + 1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()
            
        elif a[0]=="sub":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count == 3:
                if a[1] in reg and a[2] in reg and a[3] in reg:
                    y = op["sub"]+"00"+op[a[1]]+op[a[2]]+op[a[3]]
                    output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="mov":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count == 2 :
                if a[1] in reg or a[1] == "flags":
                    if a[2] not in reg and a[2] != "flags":
                        aa1=a[2]
                        aa2=aa1[1:]
                        try:
                            aa=int(aa2)
                        except ValueError:
                            print(f"ERROR : invalid argument in line {i+1}")
                            quit()
                        if type(aa) == int:
                            if aa <= 255 and aa >= 0:
                                x=decimal_to_binary(aa2)
                                y=len(x)
                                if y<8 :
                                    q=8-y
                                    q1=[]
                                    for i in range(0,q):
                                        q1.append("0")
                                    for i in range(y):
                                        q1.append(str(x[i]))
                                    y1 = "".join(q1)
                                y = op['movi']+op[a[1]]+y1
                                output.append(y)
                            else:
                                print(f"ERROR : Immediate value of bounds in line {i+1}")
                                quit()

                    elif a[2] in reg or a[2] == "flags":
                        y = op["movr"]+"00000"+op[a[1]]+op[a[2]]
                        output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
                    
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0] == "ld":
            if var_name == [] or a[2] not in var_name:
                print(f"ERROR : uninitialised variable used in line {i+1}")
                quit()
            count=0
            c = 0
            for g in range(1,len(a)):
                count=count+1
            if count == 2:
                for i in range (len(var_name)):
                    if a[2] == var_name[i]:
                        c = 1
                        x=decimal_to_binary(str(var_value[i]))
                        y=len(x)
                        if y<8 :
                            q=8-y
                            q1=[]
                            # q1 = ""
                            for i in range(0,q):
                                q1.append("0")
                                # q1 = q1+"0"
                            for i in range(y):
                                q1.append(str(x[i]))
                                # q1 = q1+str(x[i])
                            y1 = "".join(q1)
                            y = op["ld"]+op[a[1]]+y1
                            output.append(y)
                            break
                        else:
                            y1 = "".join(x)
                            y = op["ld"]+op[a[1]]+y1
                            output.append(y)
                            break
                    # else:
                    #     print(f"ERROR : invalid variable used in line {i+1}")
                    #     quit()
                else:
                    print(f"ERROR : register is not valid in line {i + 1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0] == "st":
            if var_name == [] or a[2] not in var_name:
                print(f"ERROR : uninitialised variable used in line {i+1}")
                quit()
            # if a[2] not in var_name:
            #     print("ERROR : ")
            #     quit()
            count=0
            c = 0
            for g in range(1,len(a)):
                count=count+1
            if count == 2:
                for i in range (len(var_name)):
                    if a[2] == var_name[i]:
                        c = 1
                        x=decimal_to_binary(str(var_value[i]))
                        y=len(x)
                        if y<8 :
                            q=8-y
                            q1=[]
                            # q1 = ""
                            for i in range(0,q):
                                q1.append("0")
                                # q1 = q1+"0"
                            for i in range(y):
                                q1.append(str(x[i]))
                                # q1 = q1+str(x[i])
                            y1 = "".join(q1)
                            y = op["st"]+op[a[1]]+y1
                            output.append(y)
                            break
                        else:
                            y1 = "".join(x)
                            y = op["st"]+op[a[1]]+y1
                            output.append(y)
                            break
                    # else:
                    #     print(f"ERROR : invalid variable used in line {i+1}")
                    #     quit()
                else:
                    print(f"ERROR : variable is not valid in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="mul":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count ==3:
                if a[1] in reg and a[2] in reg and a[3] in reg:
                    y = op["mul"]+"00"+op[a[1]]+op[a[2]]+op[a[3]]
                    output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="div":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count ==2:
                if a[1] in reg and a[2] in reg:
                    y = op["div"]+"00000"+op[a[1]]+op[a[2]]
                    output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="rs":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count ==2:
                if a[1] in reg:
                    aa1=a[2]
                    aa2=aa1[1:]
                    try:
                        aa=int(aa2)
                    except ValueError:
                        print(f"ERROR : invalid argument in line {i+1}")
                        quit()
                    x=decimal_to_binary(aa2)
                    y=len(x)
                    if y<8 :
                        q=8-y
                        q1=[]
                        for i in range(0,q):
                            q1.append("0")
                        for i in range(y):
                            q1.append(str(x[i]))
                        y1 = "".join(q1)
                        y = op["rs"]+op[a[1]]+y1
                    else:
                        y = op["rs"]+op[a[1]]+x
                    output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="ls":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count ==2:
                if a[1] in reg:
                    aa1=a[2]
                    aa2=aa1[1:]
                    try:
                        aa=int(aa2)
                    except ValueError:
                        print(f"ERROR : invalid argument in line {i+1}")
                        quit()
                    x=decimal_to_binary(aa2)
                    y=len(x)
                    if y<8 :
                        q=8-y
                        q1=[]
                        for i in range(0,q):
                            q1.append("0")
                        for i in range(y):
                            q1.append(str(x[i]))
                        y1 = "".join(q1)
                        y = op["ls"]+op[a[1]]+y1
                    else:
                        y = op["ls"]+op[a[1]]+x
                    output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()


        elif a[0]=="xor":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count == 3:
                if a[1] in reg and a[2] in reg and a[3] in reg:
                    print(op["xor"],op[a[1]],op[a[2]],op[a[3]],sep='')
                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="or":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count == 3:
                if a[1] in reg and a[2] in reg and a[3] in reg:
                    y = op["or"]+"00"+op[a[1]]+op[a[2]]+op[a[3]]
                    output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="and":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count == 3:
                if a[1] in reg and a[2] in reg and a[3] in reg:
                    y = op["and"]+"00"+op[a[1]]+op[a[2]]+op[a[3]]
                    output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="not":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count ==2:
                if a[1] in reg and a[2] in reg:
                    y = op["not"]+"00000"+op[a[1]]+op[a[2]]
                    output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="cmp":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count ==2:
                if a[1] in reg and a[2] in reg:
                    y = op["cmp"]+"00000"+op[a[1]]+op[a[2]]
                    output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="jmp":
            if label_name == [] or a[1] not in label_name:
                print(f"ERROR : uninitialised label used in line {i+1}")
                quit()
            count=0
            c = 0
            for g in range(1,len(a)):
                count=count+1
            if count ==1:
                for i in range (len(label_name)):
                    if a[1] == label_name[i]:
                        c = 1
                        x=decimal_to_binary(str(label_position[i]))
                        y=len(x)
                        if y<8 :
                            q=8-y
                            q1=[]
                            # q1 = ""
                            for i in range(0,q):
                                q1.append("0")
                                # q1 = q1+"0"
                            for i in range(y):
                                q1.append(str(x[i]))
                                # q1 = q1+str(x[i])
                            y1 = "".join(q1)
                            y = op["jmp"]+"000"+y1
                        else:
                            y = op["jmp"]+"000"+x
                        output.append(y)
                if c != 1:
                    print(f"ERROR : invalid label used in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="jlt":
            if label_name == [] or a[1] not in label_name:
                print(f"ERROR : uninitialised label used in line {i+1}")
                quit()
            count=0
            c = 0
            for g in range(1,len(a)):
                count=count+1
            if count ==1:
                for i in range (len(label_name)):
                    if a[1] == label_name[i]:
                        c = 1
                        x=decimal_to_binary(str(label_position[i]))
                        y=len(x)
                        if y<8 :
                            q=8-y
                            q1=[]
                            # q1 = ""
                            for i in range(0,q):
                                q1.append("0")
                                # q1 = q1+"0"
                            for i in range(y):
                                q1.append(str(x[i]))
                                # q1 = q1+str(x[i])
                            y1 = "".join(q1)
                            y = op["jlt"]+"000"+y1
                        else:
                            y = op["jlt"]+"000"+x
                        output.append(y)
                if c != 1:
                    print(f"ERROR : invalid label used in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="jgt":
            if label_name == [] or a[1] not in label_name:
                print(f"ERROR : uninitialised label used in line {i+1}")
                quit()
            count=0
            c = 0
            for g in range(1,len(a)):
                count=count+1
            if count ==1:
                for h in range (len(label_name)):
                    if a[1] == label_name[h]:
                        c = 1
                        x=decimal_to_binary(str(label_position[i]))
                        y=len(x)
                        if y<8 :
                            q=8-y
                            q1=[]
                            # q1 = ""
                            for qw in range(0,q):
                                q1.append("0")
                                # q1 = q1+"0"
                            for qw in range(y):
                                q1.append(str(x[i]))
                                # q1 = q1+str(x[i])
                            y1 = "".join(q1)
                            y = op["jgt"]+"000"+y1
                        else:
                            y = op["jgt"]+"000"+x
                        output.append(y)
                if c != 1:
                    print(f"ERROR : invalid label used in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="je":
            if label_name == [] or a[1] not in label_name:
                print(f"ERROR : uninitialised label used in line {i+1}")
                quit()
            count=0
            c = 0
            for g in range(1,len(a)):
                count=count+1
            if count ==1:
                for h in range (len(label_name)):
                    if a[1] == label_name[h]:
                        c = 1
                        x=decimal_to_binary(str(label_position[h]))
                        y=len(x)
                        if y<8 :
                            q=8-y
                            q1=[]
                            # q1 = ""
                            for qw in range(0,q):
                                q1.append("0")
                                # q1 = q1+"0"
                            for qw in range(y):
                                q1.append(str(x[i]))
                                # q1 = q1+str(x[i])
                            y1 = "".join(q1)
                            y = op["je"]+"000"+y1
                        else:
                            y = op["je"]+"000"+x
                        output.append(y)
                if c != 1:
                    print(f"ERROR : invalid label used in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="hlt":
            y = op["hlt"] + "00000000000"
            output.append(y)
            break

        elif a[0] == "addf":
            # y = op["addf"] + "00"
            count = 0
            for g in range(1,len(a)):
                count=count+1
            if count == 3:
                if a[1] in reg and a[2] in reg and a[3] in reg:
                    y = op["addf"]+"00"+op[a[1]]+op[a[2]]+op[a[3]]
                    output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i + 1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="subf":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count == 3:
                if a[1] in reg and a[2] in reg and a[3] in reg:
                    y = op["sub"]+"00"+op[a[1]]+op[a[2]]+op[a[3]]
                    output.append(y)
                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()

        elif a[0]=="movf":
            count=0
            for g in range(1,len(a)):
                count=count+1
            if count == 2 :
                if a[1] in reg or a[1] == "flags":
                    if a[2] not in reg and a[2] != "flags":
                        aa1=a[2]
                        aa2=aa1[1:]
                        try:
                            aa=float(aa2)
                        except ValueError:
                            print(f"ERROR : invalid argument in line {i+1}")
                            quit()
                        if type(aa) == float:
                            if aa <= 252 and aa >= 0:
                                xw=func(float(aa2))
                                y = op['movf']+op[a[1]]+xw
                                output.append(y)
                            else:
                                print(f"ERROR: value out of bounds in line {i+1}")
                                quit()

                else:
                    print(f"ERROR : register is not valid in line {i+1}")
                    quit()
                    
            else:
                print(f"ERROR : invalid number of registers/arguments in line {i+1}")
                quit()
                        


        else:
            print(f"ERROR : invalid instruction in line {i+1}")
            quit()

    
    for id in range (len(output)):
        print(output[id])

else:
    print(f"ERROR : halt statement missing/incorrect. It should be present in last line i.e. line {ins_c_1}")
    quit()