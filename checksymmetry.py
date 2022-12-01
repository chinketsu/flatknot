# -*- coding: utf-8 -*-
"""
=============================================================
Created on Mar 13 2022
@author: c
=============================================================
"""
Lst1 = ['a','b','c','d','e','f','g','h','i','j','k', 'l','m',
        'n','o','p', 'q','r','s','t','u','v','w','x','y','z']
Lst2= ['%d' %i for i in range(10,10+26)]
Lst3= ['%d' %i for i in range(1,10)]+ Lst1

Let2int_dict=dict(zip(Lst1,Lst2))
Int2let_dict=dict(zip(Lst2,Lst1))


def checkvalidgcode(strFlat):
    try:
        strFlat.count('O')==strFlat.count('U')
        b=[]
        for a in strFlat.split('O'):
            b+=[int(x) for x in a.split('U') if x!= '']
        b.sort()
        len(b) %2==0
        b[-1]==len(b)/2
        set(b)==set(b[0::2])
        # print(set(b))
        return True
    except:
        return False


def let2int(gcode):
    # Input example:
    # Output:
    for i in Let2int_dict.items():
        gcode=gcode.replace(i[0],i[1])
    return gcode


def int2let(gcode):
    # Input example:
    # Output:
    for i in Int2let_dict.items():
        gcode=gcode.replace(i[0],i[1])
    return gcode


def mingcode(gcode):
    # This function do
    # Input example:
    # Output:
    if len(gcode)==0:
        return ''
    # -------
    # this works for up to 36 crossings:
    gcode=int2let(gcode)
    # validate the Gauss code:
    assert len(gcode) %4==0
    # now get the crossing number
    # -------
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
        chordn=0
        for i in range(1,len(newgcode),2):
            # print(newgcode[i] )
            if newgcode[i] in ihaveseen:
                verynewcode+=(newgcode[i-1]+perm[newgcode[i]])

                # print(verynewcode )
            else:
                verynewcode+=(newgcode[i-1]+Lst3[chordn])
                perm[newgcode[i]]=Lst3[chordn]
                ihaveseen.append(newgcode[i])
                chordn += 1
                # print('perm',perm )
                # print(verynewcode )
        tobecompared.append(verynewcode)
    return minlydon(tobecompared)


def inc12(gcode):
    # this function calculated inc12 type operation
    # Input example:
    # -------
    if len(gcode)==0:
        return ''
    # this works for up to 36 crossings:
    gcode=int2let(gcode)
    # validate the Gauss code:
    assert len(gcode) %4==0
    crNum=int(len(gcode)/4)
    lst=[]
    gcode=gcode+gcode[:2]
    for i in Lst3[:crNum]:
        pattern1='O%sO' %i
        if pattern1 in gcode:
            # print('i',i)
            # print(gcode[gcode.find(pattern1)+3])
            j= gcode[gcode.find(pattern1)+3]
            # print('j',j)
            for k in Lst3[:crNum]:
                pattern2='U%sU%s' %(k,i)
                # print(pattern2)
                if pattern2 in gcode:
                    # print('k',k)
                    pattern3='O%sU%s' % (k,j)
                    if pattern3 in gcode:
                        # print(i,j,k)
                        newcode=gcode.replace(pattern2, 'U%sU%s' %(j,k)).\
                            replace(pattern3, 'U%sO%s' %(i,k))
                        if i!=j and j!=k and i!=k:
                            if newcode[-2:]== gcode[-2:]:
                                lst.append(mingcode(newcode[:-2]))
                            else:
                                # print('careful: '+gcode+','+newcode)
                                lst.append(
                                    mingcode(
                                        newcode[-2:] + newcode[2:-2]
                                    )
                                )
    return lst


def dec12(gcode):
    # This function do
    # Input example:
    # Output:
    # -------
    if len(gcode)==0:
        return ''
    # this works for up to 36 crossings:
    gcode=int2let(gcode)
    # validate the Gauss code:
    assert len(gcode) %4==0
    crNum=int(len(gcode)/4)
    lst=[]
    gcode=gcode+gcode[:2]
    for i in Lst3[:crNum]:
        pattern1='O%sO' %i
        if pattern1 in gcode:
            j= gcode[gcode.find(pattern1)+3]
            for k in Lst3[:crNum]:
                pattern2='U%sU%s' %(j,k)
                if pattern2 in gcode:
                    pattern3='U%sO%s' % (i,k)
                    if pattern3 in gcode:
                        # print(i,j,k)
                        newcode=gcode.replace(pattern2, 'U%sU%s' %(k,i)).\
                            replace(pattern3, 'O%sU%s' %(k,j))
                        if i!=j and j!=k and i!=k:
                            if newcode[-2:]== gcode[-2:]:
                                lst.append(mingcode(newcode[:-2]))
                            else:
                                # print('careful: '+gcode+','+newcode)
                                lst.append(
                                    mingcode(
                                        newcode[-2:]+newcode[2:-2]))
    return lst


def inc3dec4(gcode):
    # This function do
    # Input example:
    # Output:
    # -------
    if len(gcode)==0:
        return ''
    # this works for up to 36 crossings:
    gcode=int2let(gcode)
    # validate the Gauss code:
    assert len(gcode) %4==0
    crNum=int(len(gcode)/4)
    lst=[]
    gcode=gcode+gcode[:2]
    for i in Lst3[:crNum]:
        pattern1='U%sO' %i
        if pattern1 in gcode:
            j= gcode[gcode.find(pattern1)+3]
            for k in Lst3[:crNum]:
                pattern2='U%sO%s' %(j,k)
                if pattern2 in gcode:
                    pattern3='U%sO%s' % (k,i)
                    if pattern3 in gcode:
                        newcode=gcode.\
                            replace(pattern1+str(j), 'O%sU%s' %(i,j)).\
                            replace(pattern2, 'O%sU%s' %(k,i)).\
                            replace(pattern3, 'O%sU%s' %(j,k))
                        if i!=j and j!=k and i!=k:
                            if newcode[-2:]== gcode[-2:]:
                                lst.append(mingcode(newcode[:-2]))
                            else:
                                # print('careful: '+gcode+','+newcode)
                                lst.append(
                                    mingcode(
                                        newcode[-2:]+newcode[2:-2]))
    return lst


def inc4dec3(gcode):
    # This function do
    # Input example:
    # Output:
    # -------
    if len(gcode)==0:
        return ''
    # this works for up to 36 crossings:
    gcode=int2let(gcode)
    # validate the Gauss code:
    assert len(gcode) %4==0
    crNum=int(len(gcode)/4)
    lst=[]
    gcode=gcode+gcode[:2]
    for i in Lst3[:crNum]:
        pattern1='O%sU' %i
        if pattern1 in gcode:
            j= gcode[gcode.find(pattern1)+3]
            for k in Lst3[:crNum]:
                pattern2='O%sU%s' %(j,k)
                if pattern2 in gcode:
                    pattern3='O%sU%s' % (k,i)
                    if pattern3 in gcode:
                        newcode=gcode.\
                            replace(pattern1+str(j), 'U%sO%s' %(i,j)).\
                            replace(pattern2, 'U%sO%s' %(k,i)).\
                            replace(pattern3, 'U%sO%s' %(j,k))
                        if i!=j and j!=k and i!=k:
                            if newcode[-2:]== gcode[-2:]:
                                lst.append(mingcode(newcode[:-2]))
                            else:
                                # print('careful: '+gcode+','+newcode)
                                lst.append(
                                    mingcode(
                                        newcode[-2:]+newcode[2:-2]))
    return lst


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


def inv_gauss(gcode):
    # This function do
    # Input example:
    # Output:
    # -------
    if len(gcode)==0:
        return ''
    # this works for up to 36 crossings:
    gcode=int2let(gcode)
    # validate the Gauss code:
    assert len(gcode) %4==0
    return "".join(map(str.__add__, gcode[-2::-2],gcode[-1::-2]))


def bar_gauss(gcode):
    # This function do
    # Input example:
    # Output:
    # -------
    if len(gcode)==0:
        return ''
    # this works for up to 36 crossings:
    gcode=int2let(gcode)
    # validate the Gauss code:
    assert len(gcode) %4==0
    return gcode.replace('O','M').replace('U','O').replace('M','U')


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
    # return pd.Series({
        # "inv": invcode,
        # "bar": barcode,
        # "barinv": barinv,
        # "dig_sym_type": symlst,
        # "r3_orbit": leastset,
        # "r3_orbit_length": len(leastset)})


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
        # [r3str[i+1] for i in range(len(r3str)) if r3str.startswith('U', i)]
        # is for getting a list of U?.
        # e.g. r3str='O1O2U6O3U2O4U8O5UxO6U5U1O7O8U3U7O9OxU4U9'
        # ['6', '2', '8', 'x', '5', '1', '3', '7', '4', '9']
    return lyndondict[min(lyndondict.keys())]


def reorderforlyn(gcode):
    if len(gcode)==0:
        return ''
    # -------
    # this works for up to 36 crossings:
    gcode=int2let(gcode)
    # validate the Gauss code:
    assert len(gcode) %4==0
    # This function do
    # Input example:
    # Output:
    crNum=int(len(gcode)/4)
    checklen=[]
    for i in Lst3[:crNum]:
        checklen.append(Lst3[gcode[:gcode.find('O%s' %i)].count('O')])
    for i in range(crNum):
        gcode=gcode.replace('O%s' %Lst3[i],'M%s' %checklen[i])
        gcode=gcode.replace('U%s' %Lst3[i],'N%s' %checklen[i])
    gcode=gcode.replace('M','O')
    gcode=gcode.replace('N','U')
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
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Caution: do not change gcode0 to gcode
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # This function do
    # Input example:
    # Output:
    crNum=int(len(gcode0)/4)
    for i in Lst3[:crNum]:
        for j in Lst3[:crNum]:
            # print(i,j, '\n')
            pattern1='O%sU%s' %(i,j)
            # print('pattern1: ',pattern1, '\n')
            pattern2='O%sU%s' %(j,i)
            # print('pattern2: ',pattern2, '\n')
            pattern3='U%sO%s' %(i,j)
            pattern4='U%sO%s' %(j,i)
            gcode=gcode0+gcode0[:2]
            if i==j:
                if pattern1 in gcode:
                    newcode=gcode.replace(pattern1,'')
                    if newcode[-2:]== gcode[-2:]:
                        return mingcode(newcode[:-2])
                    else:
                        # print('careful: '+gcode+','+newcode)
                        return mingcode(newcode[-2:]+newcode[2:-2])
                elif pattern3 in gcode:
                    newcode=gcode.replace(pattern3,'')
                    if newcode[-2:]== gcode[-2:]:
                        return mingcode(newcode[:-2])
                    else:
                        # print('careful: '+gcode+','+newcode)
                        return mingcode(newcode[-2:]+newcode[2:-2])
            elif i!=j:
                if pattern1 in gcode and pattern3 in gcode:
                    # print('pattern1 , pattern3 here')
                    newcode=gcode.replace(pattern1,'').replace(pattern3,'')
                    if newcode[-2:]== gcode[-2:]:
                        return mingcode(newcode[:-2])
                    else:
                        # print('careful: '+gcode+','+newcode)
                        return mingcode(newcode[-2:]+newcode[2:-2])
                elif pattern1 in gcode and pattern2 in gcode:
                    # print('pattern1 , pattern2 here')
                    newcode=gcode.replace(pattern1,'').replace(pattern2,'')
                    if newcode[-2:]== gcode[-2:]:
                        return mingcode(newcode[:-2])
                    else:
                        # print('careful: '+gcode+','+newcode)
                        return mingcode(newcode[-2:]+newcode[2:-2])
                elif pattern3 in gcode and pattern4 in gcode:
                    # print('pattern3 , pattern4 here')
                    newcode=gcode.replace(pattern3,'').replace(pattern4,'')
                    if newcode[-2:]== gcode[-2:]:
                        return mingcode(newcode[:-2])
                    else:
                        # print('careful: '+gcode+','+newcode)
                        return mingcode(newcode[-2:]+newcode[2:-2])
    return mingcode(gcode0)


def checkr2r1_recursive_orbit(gcode):
    # This function do
    # Input example:
    # Output:
    gcode=mingcode(gcode)
    len0=len(gcode)
    if len0<=8:
        return ''
    for gcode in checkR3({gcode}):
        newcode=checkr2r1_only_one_move(gcode)
        if len(newcode)<len0:
            return checkr2r1_recursive_orbit(newcode)
    return gcode


def vk2fk(strFlat0):
    # This function do
    # Input example:
    # Output:
    if len(strFlat0)==0:
        return ''
    # -------
    # this works for up to 36 crossings:
    gcode=int2let(strFlat0)
    gcode='g'+strFlat0+'g'
    rank_num=len(gcode)
    switcher ={'O': 'U', 'U':'O'}
    for i in range(rank_num):
        if i %3==0 and gcode[i]=='-':
            gcode=gcode[:i-2] + switcher[gcode[i-2]]+ gcode[i-1:]
    return let2int(gcode[1:].replace('-','').replace('+','')[:-1])


def gcode2parity(gcode,modn):
    """
    this matrix calculation follows Gibson's convention,
    so the n:=#heads-#tails
    2022-8-8: I changed all convention to make it the same as Gibson's
    'Over' or 'tail' always means +1 in counting intersections.
    """
    gcode=mingcode(gcode)
    # print(gcode)
    rank_num = int(len(gcode)/4)
    assert rank_num == len(gcode)/4
    tails = []
    heads = []
    for i in Lst3[:rank_num]:
        tails.append(int(gcode.rindex("O%s" %i)/2+1))
    # now we make a list for heads:
        heads.append(int(gcode.rindex("U%s" %i)/2+1))
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
        try:
            newgcode= df[df.gcode==newgcode].iloc[0]['name']
        except:
            print(newgcode)
    else:
        newgcode=='0'
        # --------^^ for df check
    return newgcode


def draw_arc(strFlat):
    textpiece=[]
    textpiece.append(r'\begin{tikzpicture}')
    # textpiece.append('\n')
    textpiece.append(r'\draw[] (0:1cm) arc (0:360:1cm);')
    # textpiece.append('\n')
    gcode=int2let(strFlat)
    rank_num=int(len(gcode)/4)
    half=360/(4*rank_num)
    tails = []
    heads = []
    for i in Lst3[:rank_num]:
        tails.append(int(gcode.rindex("O%s" %i)/2+1))
        heads.append(int(gcode.rindex("U%s" %i)/2+1))

    for i in range(0,rank_num):
        textpiece.append(
                r'\draw[-to] (%d:1cm) to[out=%d,in=%d] (%d:1cm);'
                %(
                    90+(2*tails[i]-1)*half,
                    (2*tails[i]-1)*half-90,
                    (2*heads[i]-1)*half-90,
                    90+(2*heads[i]-1)*half)
                )
    # textpiece.append('\n')
    textpiece.append(r'  \node at (270:1.25cm) {%s};' %strFlat)
    # textpiece.append('\n')
    textpiece.append(r'\end{tikzpicture}')
    return(' '.join(textpiece))

if __name__ == "__main__":
    pass
