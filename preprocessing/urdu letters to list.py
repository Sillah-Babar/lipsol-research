
file1=open("urdu-letters.txt",'r',encoding='utf-8')
Lines = file1.readlines()
letters=[]
unicode=[]
digits_map=[]
x=0
for i in range(len(Lines)):
    Lines[i]=Lines[i].strip()
    if(i%2==0):
        letters.append(Lines[i])
        digits_map.append(x)
        x+=1
    else:
        unicode.append(int(Lines[i]))


print(letters)
print(unicode)
print(digits_map)
print(len(letters))
print(len(unicode))
print(len(digits_map))
