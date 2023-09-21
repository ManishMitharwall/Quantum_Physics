#!/storage/praha1/home/manishkumar/.conda/envs/kumarpython3/bin/python3.8
from gettext import npgettext
from re import A
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class MO:
    """ The MO object has to initialised with index of the MO,it's energy and occupancy. 
    The type(alpha or beta) is not going to help here"""
    def __init__(self,index,occupancy,energy):
        """Defination of the MO"""
        self.ind=index
        self.occ=occupancy
        self.en=energy
#        self.compo={}


fi = open('cohc.out', 'r')

amos,bmos=[],[]
while "SPIN UP ORBITALS" not in fi.readline():
    continue
fi.readline()
for line in fi:
    if not line.strip():
        break
    else:
        split=line.split()
        amos.append(MO(int(split[0]),float(split[1]),float(split[3])))
for i in range(2):
    fi.readline()
for line in fi:
    if not line.strip():
        break
    else:
        split=line.split()
        bmos.append(MO(int(split[0]),float(split[1]),float(split[3])))
#for k in amos:
#    print(k.ind,(k.en)/27, k.occ, k.en)


def find_fmo(mos):
    for mo in mos:
        if mo.occ < 1.0:
            lumo=mo.ind
            break
    homo=lumo-1
    return homo
def del_en(mos):
    homo=find_fmo(mos)
    del_en=mos[homo+1].en-mos[homo].en
    return del_en



ax1,ax2,ax3,w=np.asarray([-2,-1]),np.asarray([0,1]),np.asarray([-1,0]),2.5
tick,lab=[],[]
low_lim,up_lim=-7,-1
ylab=np.linspace(low_lim+1,up_lim-1.00,5)
mpl.rcParams['figure.figsize'] = 5.0, 14
color=['red','green','blue']
ax,bx,w=np.asarray([-2,-1]),np.asarray([-0.5,0.5]),2.5
ax=ax+4
bx=bx+4
ahomo,aden=find_fmo(amos),del_en(amos)
bhomo,bden=find_fmo(bmos),del_en(bmos)
for mo in amos:
    if mo.en >= low_lim and mo.en <=  up_lim:
        y=[mo.en,mo.en] 

        if mo.occ == 1.0 and mo.ind > bhomo:

            plt.plot(ax,y,color='purple', linewidth=w)  
        elif mo.occ == 1.0:
            plt.plot(ax,y,color='blue', linewidth=w)
        else:
            plt.plot(ax,y,color='crimson', linewidth=w)
        
for mo in bmos:
    if mo.en >= low_lim and mo.en <=  up_lim:
        y=[mo.en,mo.en]
        if mo.occ == 1.0:
            plt.plot(bx,y,color='blue', linewidth=w)  
        else:
            plt.plot(bx,y,color='crimson', linewidth=w)
plt.annotate(text='',xy=((bx[0]+bx[1])/2,bmos[bhomo].en), xytext=((bx[0]+bx[1])/2,bmos[bhomo+1].en), arrowprops={'arrowstyle':'<->','ls': 'dashed'})
plt.annotate(text='',xy=((ax[0]+ax[1])/2,amos[ahomo].en), xytext=((ax[0]+ax[1])/2,amos[ahomo+1].en), arrowprops={'arrowstyle':'<->','ls': 'dashed'})
plt.text((ax[0]+ax[1])/2,(amos[ahomo].en+amos[ahomo+1].en)/2,'{:.2f}'.format(aden))
plt.text((bx[0]+bx[1])/2,(bmos[bhomo].en+bmos[bhomo+1].en)/2,'{:.2f}'.format(bden))
tick.append((ax[0]+ax[1])/2)
lab.append(r'$\alpha$-MO')
tick.append((ax[0]+bx[1])/2)
lab.append('\n'+ 'name')
tick.append((bx[0]+bx[1])/2)
lab.append(r'$\beta$-MO')
    
plt.xlim(1,bx[1]+1)
plt.ylim(low_lim,up_lim)
plt.xticks(tick,lab,size=12)
#ylab=np.linspace(int(min([aMOS[ahomo-low_lim].en,bMOS[ahomo-low_lim].en]))-1,int(max([aMOS[ahomo+high_lim+1].en,aMOS[ahomo+high_lim+1].en]))+1,5,endpoint=True)
plt.yticks(size=12)
plt.ylabel("Energy(eV)",fontweight='bold',size=14)
#plt.savefig("FMO_plot.png",dpi=400)
plt.tick_params(axis='both',which='major',direction='in',length=6,top=False,bottom=False,left=True,right=False,width=2.0)
plt.savefig("FMO_plot.pdf",bbox_inches='tight',pad_inches=0.0)
plt.show()







