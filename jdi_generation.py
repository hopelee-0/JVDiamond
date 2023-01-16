filename = '220726_AR01_4.jdi'
savename = 'test_save.txt'
path = "C:\\Users\\makaa\\Documents\\Lab Documents\\Projects\\Diamond\\Scripts\\dose_arrays\\"

view_jdi_bool = 0

bd=175
num_doses = 4
iteration = 25
mod_name = "M4"

### Reads jdi file as generated from the JEOL ###

# f.split('))')[0] -> delete everything after '))'
# .split(')') split in entries that are separated by ')'
# txtline.strip() -> remove leading and trailing spaces
#.split(',')[-1] -> split entries with ',' separator and use last entry [-1] corresponding to dose percentage
#.strip()  -> remove leading and trailing spaces

f = open(path+filename)
txtcrp=f.read().split('))')[0].split(')')
i=0
doseprc=[]
for txtline in txtcrp:
    doseprc.append(float(txtline.strip().split(',')[-1].strip()))
    i+=1
f.close()
if view_jdi_bool == 1:
    print('number of entries: '+str(i)) # number of entries
    print(doseprc) # entries
    f = open(path+filename)
    print('\n'+'file content:'+'\n'+f.read())
    f.close()

### Normalizes ###
doseprcnorm=[]
for i in range(len(doseprc)):
    doseprcnorm.append(round(((doseprc[i]+100)/(doseprc[0]+100)-1)*100,1))
if view_jdi_bool == 1:
    print('dose array:'+'\n'+str(doseprc)+'\n')
    print('normalize:'+'\n'+str(doseprcnorm))

### Creates Modulation ###
for i in range(num_doses):
    nbd=round(bd+i*iteration) #new base dose
    doseprcnew=[]
    for i in range(len(doseprc)):
        doseprcnew.append(round(((doseprcnorm[i]/100+1)*nbd/bd-1)*100,1))
    #print("new dose array:\n"+str(doseprcnew))
    #print("prev dose array:\n"+str(doseprc))
    txtjdi=mod_name+str(nbd)+": MODULAT ("
    for i in range(len(doseprcnew)-1):
        if i>0:
            if (i%5)==0:
                txtjdi=txtjdi+"\n-"
        txtjdi=txtjdi+"("+str(i)+", "+str(doseprcnew[i])+") , "
    txtjdi=txtjdi+"("+str(len(doseprcnew)-1)+", "+str(doseprcnew[len(doseprcnew)-1])+"))"
    #print("new .jdi text:\n"+txtjdi)
    f = open(path+savename,'a')
    f.write(txtjdi+"\n\n")
    f.close()
