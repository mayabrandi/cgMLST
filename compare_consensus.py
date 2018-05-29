
f1 = open("MIC3553A16/cns.fq","r").readlines()
f2 = open("MIC3551A7/cns.fq","r").readlines()

dict1 = {}
dict2 = {}
currentID = ""
sequence = False
for l in f1:
    line = l.strip()
    if line[0:4] == "@lcl":
        currentID = line[5:]
        dict1[currentID] = ""
        sequence=True
    elif line[0] == '+':
        sequence=False
    elif sequence:
        dict1[currentID] = dict1[currentID]+line

currentID = ""

for l in f2:
    line = l.strip()
    if line[0:4] == "@lcl":
        currentID = line[5:]
        dict2[currentID] = ""
        sequence=True
    elif line[0] == '+':
        sequence=False
    elif sequence:
        dict2[currentID] = dict2[currentID]+line


diff={}
ambigous = ['n','a','t','c','g']
diff_len=[]
not_in_both=[]
all_keys= dict1.keys()+dict2.keys()
all_keys = list(set(all_keys))
for key in all_keys:
    if key not in dict2 or key not in dict1:
        not_in_both.append(key)
    else:
        if dict1[key] != dict2[key]:
            varinats=[]
            if len(dict1[key])== len(dict2[key]):
                for i in range(len(dict1[key])):
                    b1 = dict1[key][i]
                    b2 = dict2[key][i]
                    if b1 != b2 and b1 not in ambigous and b2 not in ambigous:
                        varinats.append((i,b1,b2))
                        print(key, i, b1, b2)
            if varinats:
                diff[key] = varinats
            else:
                diff_len.append(key)


