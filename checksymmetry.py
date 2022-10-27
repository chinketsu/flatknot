# -*- coding: utf-8 -*-
"""
=============================================================
Created on Mar 13 2022
@author: c
=============================================================
"""
# import csv
import copy
import numpy as np
import pandas as pd
# from ast import literal_eval

def inc12(gcode0):
    crNum=int(len(gcode0)/4) 
    lst=[]
    gcode=gcode0+gcode0[:2]
    for i in range(1, crNum+1 ) :
        pattern1='O%dO' %i
        if pattern1 in gcode:
            # print('i',i)
            # print(gcode[gcode.find(pattern1)+3])
            j= int(gcode[gcode.find(pattern1)+3])
            # print('j',j)
            for k in range(1,crNum+1):
                pattern2='U%dU%d' %(k,i)
                # print(pattern2)
                if pattern2 in gcode:
                    # print('k',k)
                    pattern3='O%dU%d' % (k,j)
                    if pattern3 in gcode:
                        # print(i,j,k)
                        newcode=gcode.replace(pattern2, 'U%dU%d' %(j,k)).replace(pattern3, 'U%dO%d' %(i,k))
                        assert i!=j and j!=k and i!=k
                        if newcode[-2:]== gcode[-2:]: 
                            lst.append( mingcode(newcode[:-2]))
                        else: 
                            #print('careful: '+gcode0+','+newcode)
                            lst.append( mingcode(newcode[-2:]+newcode[2:-2]))
    return lst

def dec12(gcode0):
    crNum=int(len(gcode0)/4) 
    lst=[]
    gcode=gcode0+gcode0[:2]
    for i in range(1, crNum+1 ) :
        pattern1='O%dO' %i
        if pattern1 in gcode:
            j= int(gcode[gcode.find(pattern1)+3])
            for k in range(1,crNum+1):
                pattern2='U%dU%d' %(j,k)
                if pattern2 in gcode:
                    pattern3='U%dO%d' % (i,k)
                    if pattern3 in gcode:
                        # print(i,j,k)
                        newcode=gcode.replace(pattern2, 'U%dU%d' %(k,i)).replace(pattern3, 'O%dU%d' %(k,j))
                        assert i!=j and j!=k and i!=k
                        if newcode[-2:]== gcode[-2:]: 
                            lst.append( mingcode(newcode[:-2]))
                        else: 
                            #print('careful: '+gcode0+','+newcode)
                            lst.append( mingcode(newcode[-2:]+newcode[2:-2]))
    return lst

def inc3dec4(gcode0):
    crNum=int(len(gcode0)/4) 
    lst=[]
    gcode=gcode0+gcode0[:2]
    for i in range(1, crNum+1 ) :
        pattern1='U%dO' %i
        if pattern1 in gcode:
            j= int(gcode[gcode.find(pattern1)+3])
            for k in range(1,crNum+1):
                pattern2='U%dO%d' %(j,k)
                if pattern2 in gcode:
                    pattern3='U%dO%d' % (k,i)
                    if pattern3 in gcode:
                        newcode=gcode.replace(pattern1+str(j), 'O%dU%d' %(i,j))\
                        .replace(pattern2, 'O%dU%d' %(k,i)).replace(pattern3, 'O%dU%d' %(j,k))
                        assert i!=j and j!=k and i!=k
                        if newcode[-2:]== gcode[-2:]: 
                            lst.append( mingcode(newcode[:-2]))
                        else: 
                            #print('careful: '+gcode0+','+newcode)
                            lst.append( mingcode(newcode[-2:]+newcode[2:-2]))
    return lst

def inc4dec3(gcode0):
    crNum=int(len(gcode0)/4) 
    lst=[]
    gcode=gcode0+gcode0[:2]
    for i in range(1, crNum+1 ) :
        pattern1='O%dU' %i
        if pattern1 in gcode:
            j= int(gcode[gcode.find(pattern1)+3])
            for k in range(1,crNum+1):
                pattern2='O%dU%d' %(j,k)
                if pattern2 in gcode:
                    pattern3='O%dU%d' % (k,i)
                    if pattern3 in gcode:
                        newcode=gcode.replace(pattern1+str(j), 'U%dO%d' %(i,j))\
                        .replace(pattern2, 'U%dO%d' %(k,i)).replace(pattern3, 'U%dO%d' %(j,k))
                        assert i!=j and j!=k and i!=k
                        if newcode[-2:]== gcode[-2:]: 
                            lst.append( mingcode(newcode[:-2]))
                        else: 
                            #print('careful: '+gcode0+','+newcode)
                            lst.append( mingcode(newcode[-2:]+newcode[2:-2]))
    return lst


def mingcode(gcode):
    crNum=int(len(gcode)/4)
    str0=(gcode[0::2]+gcode[0::2]).replace('U','1').replace('O','0')
    lst=[int(str0[i:i+2*crNum]) for i in range(2*crNum)]
    #print(lst)
    #minindex=lst.index(min(lst))
    minlist=[i for i, v in enumerate(lst) if v == min(lst)]
    tobecompared=[]
    for minindex in minlist:
        newgcode=(gcode+gcode)[2*minindex:2*minindex+4*crNum ]
        #print('newgcode',newgcode)
        ihaveseen=[]
        verynewcode=''
        perm={}
        chordn=1
        for i in range(1,len(newgcode),2):
            #print(newgcode[i] )
            if newgcode[i] in ihaveseen:
                verynewcode+=(newgcode[i-1]+perm[newgcode[i]])

                #print(verynewcode )
            else:
                verynewcode+=(newgcode[i-1]+str(chordn))
                perm[newgcode[i]]=str(chordn)
                ihaveseen.append(newgcode[i])
                chordn += 1
                #print('perm',perm )
                #print(verynewcode )
        tobecompared.append(verynewcode)
    return(minlydon(tobecompared))

def checkR3(r3set):
    if r3set=={'Same'}:
        return {'Same'}
    len0=len(r3set)
    newr3set=r3set.copy()
    for gcode in r3set:
        newr3set.update(inc12(gcode))
        newr3set.update(dec12(gcode))
        newr3set.update(inc3dec4(gcode))
        newr3set.update(inc4dec3(gcode))
    if len(newr3set)==len0:
        return newr3set
    else:
        #print(newr3set)
        return checkR3(newr3set)

def inv_gauss(strFlat0):
    return("".join(map(str.__add__, strFlat0[-2::-2] ,strFlat0[-1::-2])))

def bar_gauss(strFlat0):
    return(strFlat0.replace('O','M').replace('U','O').replace('M','U'))


def checkmirrorimg(gcode):
    r3set={mingcode(gcode)}
    leastset=checkR3(r3set)
    invcode = mingcode(inv_gauss(gcode))
    barcode = mingcode(bar_gauss(gcode))
    barinv = mingcode(bar_gauss( inv_gauss(gcode)))
    if invcode in leastset:
        invcode="Same"
    if barcode in leastset:
        barcode="Same"
    if barinv in leastset:
        barinv="Same"
    return "inv:"+ minlydon(checkR3({invcode}))+",bar:"+ minlydon(checkR3({barcode}))+",barinv:"+ minlydon(checkR3({barinv}))


def minlydon(r3set):
    if r3set=={'Same'}:
        return 'Same' 
    if len(r3set)==1:
        return(list(r3set)[0])
    r3list=list(r3set)
    lyndondict={}
    for r3str in r3list:
        lyndondict.update({r3str[0: :2]+''.join([r3str[i+1] for i in range(len(r3str)) if r3str.startswith('U', i)]):r3str})
    return  lyndondict[min(lyndondict.keys())]

def symtype(gcode):
    r3set={mingcode(gcode)}
    leastset=checkR3(r3set)
    invcode = mingcode(inv_gauss(gcode))
    barcode = mingcode(bar_gauss(gcode))
    barinv = mingcode(bar_gauss( inv_gauss(gcode)))
    symlst=[0,0,0]
    if invcode in leastset:
        symlst[0]=1
    if barcode in leastset:
        symlst[1]=1
    if barinv in leastset:
        symlst[2]=1
    return symlst

def checkr2r1_only_one_move(gcode0):
    crNum=int(len(gcode0)/4) 
    for i in range(1,crNum+1):
        for j in range(1,crNum+1):
            # print(i,j, '\n')
            pattern1='O%dU%d' %(i,j)
            # print('pattern1: ',pattern1, '\n')
            pattern2='O%dU%d' %(j,i)
            # print('pattern2: ',pattern2, '\n')
            pattern3='U%dO%d' %(i,j)
            pattern4='U%dO%d' %(j,i)
            lst=[]
            gcode=gcode0+gcode0[:2]
            if i==j: 
                if pattern1 in gcode:
                    newcode=gcode.replace(pattern1,'')
                    if newcode[-2:]== gcode[-2:]: 
                        return mingcode(newcode[:-2])
                    else: 
                        # print('careful: '+gcode0+','+newcode)
                        return mingcode(newcode[-2:]+newcode[2:-2])
                elif pattern3 in gcode:
                    newcode=gcode.replace(pattern3,'')
                    if newcode[-2:]== gcode[-2:]: 
                        return mingcode(newcode[:-2])
                    else: 
                        # print('careful: '+gcode0+','+newcode)
                        return mingcode(newcode[-2:]+newcode[2:-2])
            elif i!=j: 
                if pattern1 in gcode and pattern3 in gcode:
                    # print('pattern1 , pattern3 here')
                    newcode=gcode.replace(pattern1,'').replace(pattern3,'')
                    if newcode[-2:]== gcode[-2:]: 
                        return mingcode(newcode[:-2])
                    else: 
                        # print('careful: '+gcode0+','+newcode)
                        return mingcode(newcode[-2:]+newcode[2:-2])
                elif pattern1 in gcode and pattern2 in gcode:
                    # print('pattern1 , pattern2 here')
                    newcode=gcode.replace(pattern1,'').replace(pattern2,'')
                    if newcode[-2:]== gcode[-2:]: 
                        return mingcode(newcode[:-2])
                    else: 
                        # print('careful: '+gcode0+','+newcode)
                        return mingcode(newcode[-2:]+newcode[2:-2])
                elif pattern3 in gcode and pattern4 in gcode:
                    # print('pattern3 , pattern4 here')
                    newcode=gcode.replace(pattern3,'').replace(pattern4,'')
                    if newcode[-2:]== gcode[-2:]: 
                        return mingcode(newcode[:-2])
                    else: 
                        # print('careful: '+gcode0+','+newcode)
                        return mingcode(newcode[-2:]+newcode[2:-2])

    return mingcode(gcode0)


def checkr2r1_recursive(gcode0):
    len0=len(gcode0)
    newcode=checkr2r1_only_one_move(gcode0)
    if len(newcode)==len0:
        return newcode
    else:
        return checkr2r1_recursive(newcode)



if __name__ == "__main__":
    for crNum in range(3,8):
        in_path = '../results/result_%dcrossings_1.csv' % crNum
        out_path = './mirrorimage_%dcrossings.csv' % crNum
        # in_path = '../results/result_AC_%dcrossings_1.csv' % crNum
        # out_path = './mirrorimage_AC_%dcrossings.csv' % crNum
        df = pd.read_csv(in_path,dtype=str,usecols=['name','gcode'])
        df2 = df.merge(df['gcode'].apply(checkmirrorimg),left_index=True, right_index=True)
        df2.to_csv(out_path,index=None)

