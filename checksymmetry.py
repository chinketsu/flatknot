# -*- coding: utf-8 -*-
"""
=============================================================
Created on Mar 13 2022
@author: c
=============================================================
"""


def inc12(gcode0):
    # this function calculated inc12 type operation
    # Input example:
    # Output:
    crNum=int(len(gcode0)/4)
    lst=[]
    gcode=gcode0+gcode0[:2]
    for i in range(1, crNum+1):
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
                        newcode=gcode.replace(pattern2, 'U%dU%d' %(j,k)).\
                            replace(pattern3, 'U%dO%d' %(i,k))
                        if i!=j and j!=k and i!=k:
                            if newcode[-2:]== gcode[-2:]:
                                lst.append(mingcode(newcode[:-2]))
                            else:
                                # print('careful: '+gcode0+','+newcode)
                                lst.append(
                                    mingcode(
                                        newcode[-2:] + newcode[2:-2]
                                    )
                                )
    return lst


def dec12(gcode0):
    # This function do
    # Input example:
    # Output:
    crNum=int(len(gcode0)/4)
    lst=[]
    gcode=gcode0+gcode0[:2]
    for i in range(1, crNum+1):
        pattern1='O%dO' %i
        if pattern1 in gcode:
            j= int(gcode[gcode.find(pattern1)+3])
            for k in range(1,crNum+1):
                pattern2='U%dU%d' %(j,k)
                if pattern2 in gcode:
                    pattern3='U%dO%d' % (i,k)
                    if pattern3 in gcode:
                        # print(i,j,k)
                        newcode=gcode.replace(pattern2, 'U%dU%d' %(k,i)).\
                            replace(pattern3, 'O%dU%d' %(k,j))
                        if i!=j and j!=k and i!=k:
                            if newcode[-2:]== gcode[-2:]:
                                lst.append(mingcode(newcode[:-2]))
                            else:
                                # print('careful: '+gcode0+','+newcode)
                                lst.append(
                                    mingcode(
                                        newcode[-2:]+newcode[2:-2]))
    return lst


def inc3dec4(gcode0):
    # This function do
    # Input example:
    # Output:
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
                        newcode=gcode.\
                            replace(pattern1+str(j), 'O%dU%d' %(i,j)).\
                            replace(pattern2, 'O%dU%d' %(k,i)).\
                            replace(pattern3, 'O%dU%d' %(j,k))
                        if i!=j and j!=k and i!=k:
                            if newcode[-2:]== gcode[-2:]:
                                lst.append(mingcode(newcode[:-2]))
                            else:
                                # print('careful: '+gcode0+','+newcode)
                                lst.append(
                                    mingcode(
                                        newcode[-2:]+newcode[2:-2]))
    return lst


def inc4dec3(gcode0):
    # This function do
    # Input example:
    # Output:
    crNum=int(len(gcode0)/4)
    lst=[]
    gcode=gcode0+gcode0[:2]
    for i in range(1, crNum+1):
        pattern1='O%dU' %i
        if pattern1 in gcode:
            j= int(gcode[gcode.find(pattern1)+3])
            for k in range(1,crNum+1):
                pattern2='O%dU%d' %(j,k)
                if pattern2 in gcode:
                    pattern3='O%dU%d' % (k,i)
                    if pattern3 in gcode:
                        newcode=gcode.\
                            replace(pattern1+str(j), 'U%dO%d' %(i,j)).\
                            replace(pattern2, 'U%dO%d' %(k,i)).\
                            replace(pattern3, 'U%dO%d' %(j,k))
                        if i!=j and j!=k and i!=k:
                            if newcode[-2:]== gcode[-2:]:
                                lst.append(mingcode(newcode[:-2]))
                            else:
                                # print('careful: '+gcode0+','+newcode)
                                lst.append(
                                    mingcode(
                                        newcode[-2:]+newcode[2:-2]))
    return lst


def mingcode(gcode):
    # This function do
    # Input example:
    # Output:
    if len(gcode)==0:
        return ''
    crNum=int(len(gcode)/4)
    str0=(gcode[0::2]+gcode[0::2]).replace('U','1').replace('O','0')
    lst=[int(str0[i:i+2*crNum]) for i in range(2*crNum)]
    # print(lst)
    # minindex=lst.index(min(lst))
    minlist=[i for i, v in enumerate(lst) if v == min(lst)]
    tobecompared=[]
    for minindex in minlist:
        newgcode=(gcode+gcode)[2*minindex:2*minindex+4*crNum]
        # print('newgcode',newgcode)
        ihaveseen=[]
        verynewcode=''
        perm={}
        chordn=1
        for i in range(1,len(newgcode),2):
            # print(newgcode[i] )
            if newgcode[i] in ihaveseen:
                verynewcode+=(newgcode[i-1]+perm[newgcode[i]])

                # print(verynewcode )
            else:
                verynewcode+=(newgcode[i-1]+str(chordn))
                perm[newgcode[i]]=str(chordn)
                ihaveseen.append(newgcode[i])
                chordn += 1
                # print('perm',perm )
                # print(verynewcode )
        tobecompared.append(verynewcode)
    return minlydon(tobecompared)


def checkR3(r3set):
    # This function do
    # Input example:
    # Output:
    if type(r3set)==str:
        r3set={r3set}
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
        # print(newr3set)
        return checkR3(newr3set)


def inv_gauss(strFlat0):
    # This function do
    # Input example:
    # Output:
    return "".join(map(str.__add__, strFlat0[-2::-2],strFlat0[-1::-2]))


def bar_gauss(strFlat0):
    # This function do
    # Input example:
    # Output:
    return strFlat0.replace('O','M').replace('U','O').replace('M','U')


def checkmirrorimg(gcode):
    # This function do
    # Input example:
    # Output:
    r3set={mingcode(gcode)}
    leastset=checkR3(r3set)
    invcode = mingcode(inv_gauss(gcode))
    barcode = mingcode(bar_gauss(gcode))
    barinv = mingcode(bar_gauss(inv_gauss(gcode)))
    symlst=[0,0,0]
    if invcode in leastset:
        invcode="Same"
        symlst[0]=1
    if barcode in leastset:
        barcode="Same"
        symlst[1]=1
    if barinv in leastset:
        barinv="Same"
        symlst[2]=1
    return "inv: "+ invcode +"\n bar: "+ barcode+"\n barinv: "+barinv


def minsibling(gcode):
    # This function do
    # Input example:
    # Output:
    invcode = mingcode(inv_gauss(gcode))
    barcode = mingcode(bar_gauss(gcode))
    barinv = mingcode(bar_gauss(inv_gauss(gcode)))
    return minlydon(checkR3({mingcode(gcode),invcode,barcode,barinv}))


def minlydon(r3set):
    # This function do
    # Input example:
    # Output:
    if r3set=={'Same'}:
        return 'Same'
    if len(r3set)==1:
        return list(r3set)[0]
    r3list=list(r3set)
    lyndondict={}
    for r3str0 in r3list:
        r3str=reorderforlyn(r3str0)
        lyndondict.update({
            r3str[0::2]+''.join([r3str[i+1]
                                for i in range(len(r3str))
                                if r3str.startswith('U', i)]):r3str0})
    return lyndondict[min(lyndondict.keys())]


def reorderforlyn(gcode):
    # This function do
    # Input example:
    # Output:
    crNum=int(len(gcode)/4)
    checklen=[]
    for i in range(1,crNum+1):
        checklen.append(gcode[:gcode.find('O%d' %i)].count('O')+1)
    for i in range(1,crNum+1):
        gcode=gcode.replace('O%d' %i,'o%d' %checklen[i-1])
        gcode=gcode.replace('U%d' %i,'u%d' %checklen[i-1])
    gcode=gcode.replace('o','O')
    gcode=gcode.replace('u','U')
    return gcode


def symtype(gcode):
    # This function do
    # Input example:
    # Output:
    r3set={mingcode(gcode)}
    leastset=checkR3(r3set)
    invcode = mingcode(inv_gauss(gcode))
    barcode = mingcode(bar_gauss(gcode))
    barinv = mingcode(bar_gauss(inv_gauss(gcode)))
    symlst=[0,0,0]
    if invcode in leastset:
        symlst[0]=1
    if barcode in leastset:
        symlst[1]=1
    if barinv in leastset:
        symlst[2]=1
    return symlst


def checkr2r1_only_one_move(gcode0):
    # This function do
    # Input example:
    # Output:
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


def checkr2r1_recursive_orbit(gcode0):
    # This function do
    # Input example:
    # Output:
    gcode0=mingcode(gcode0)
    len0=len(gcode0)
    if len0<=4:
        return ''
    for gcode in checkR3({gcode0}):
        newcode=checkr2r1_only_one_move(gcode)
        if len(newcode)<len0:
            return checkr2r1_recursive_orbit(newcode)
    return gcode0


def vk2fk(strFlat0):
    # This function do
    # Input example:
    # Output:
    strFlat='g'+strFlat0+'g'
    rank_num=len(strFlat)
    switcher ={'O': 'U', 'U':'O'}
    for i in range(rank_num):
        if i %3==0 and strFlat[i]=='-':
            strFlat=strFlat[:i-2] + switcher[strFlat[i-2]]+ strFlat[i-1:]
    return strFlat[1:].replace('-','').replace('+','')[:-1]


def gcode2parity(gcode0,modn):
    """
    this matrix calculation follows Gibson's convention,
    so the n:=#heads-#tails
    2022-8-8: I changed all convention to make it the same as Gibson's
    'Over' or 'tail' always means +1 in counting intersections.
    """
    gcode=mingcode(gcode0)
    # print(gcode)
    if '10' in gcode:
        gcode=gcode.replace('10', 'x')
    rank_num = int(len(gcode)/4)
    assert rank_num == len(gcode)/4
    tails = []
    for i in range(1,rank_num+1):
        if i < 10:
            tails.append(int(gcode.rindex("O%i" %i)/2+1))
        elif i ==10:
            tails.append(int(gcode.rindex("O%s" %'x')/2+1))
    # now we make a list for heads:
    heads = []
    for i in range(1,rank_num+1):
        if i < 10:
            heads.append(int(gcode.rindex("U%i" %i)/2+1))
        elif i ==10:
            heads.append(int(gcode.rindex("U%s" %'x')/2+1))
    # now calculate theta, which represent the lower triangle of the matrix:
    # firstly, we calculate the first column n(e_i)=B(e_i,s)
    theta = []
    for i in range(0,rank_num):
        # i is 1 less than the arrow number
        if tails[i]<heads[i]:
            substr = gcode[(tails[i]*2): (heads[i]*2-2)]
        else:
            substr = gcode[(tails[i]*2):]+ gcode[:(heads[i]*2-2)]
        # print(substr)
        theta.append((substr.count("O")- substr.count("U")) %modn)
        # n=#tails-#heads
    for i in range(0,rank_num):
        if theta[i]!=0:
            gcode=gcode[:tails[i]*2-2]+'__'+gcode[tails[i]*2:]
            gcode=gcode[:heads[i]*2-2]+'__'+gcode[heads[i]*2:]
    # print('flag_0',gcode.replace('__',''))
    newgcode=checkr2r1_recursive_orbit(gcode.replace('__',''))
    # newgcode=checkr2r1_recursive_orbit(  newgcode)
    # print('flag_1',newgcode)
    # print(minsibling(newgcode))
    if f"{rank_num}" in newgcode or 'x' in newgcode:
        newgcode='same'
    elif newgcode !='':
        newgcode=minsibling(newgcode)
        # print('flag_2',newgcode)
        # print(newgcode,len(newgcode),len(gcode))
        # --------vv for df check
        # try:
            # newgcode= df[df.gcode==newgcode].iloc[0]['name']
        # except:
            # print(newgcode)
    else:
        newgcode=='0'
        # --------^^ for df check
    return newgcode


if __name__ == "__main__":
    pass
