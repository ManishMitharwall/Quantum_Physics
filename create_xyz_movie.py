#!/storage/praha1/home/manishkumar/.conda/envs/kumarpython3/bin/python3.8

import sys
f2=open('movie.xyz','w')

def skipline():
    for j in range(5):
        line=f1.readline()


with open(sys.argv[1]) as f1:
    counter=0
    all_coords = []
    for line in f1:
        if 'Number of species' in line:
            line=f1.readline()
            split=line.split()
            no_of_atom=split[5]
        if 'Updated' in line:
            counter+=1
            f2.write(no_of_atom+'\n'+'iteration'+'\t'+str(counter)+'\n')
            for i in range(1):
                skipline()
                for j in range(int(no_of_atom)):
                    coord_line=f1.readline()
                    (atom,x,y,z,aname)=coord_line.split()
                    f2.write(aname+'\t'+x+'\t'+y+'\t'+z+'\n')
            # if not line.strip():
            #     break
f2.close()
