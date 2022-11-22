# -*- coding: utf-8 -*-
"""
=============================================================
Created on Nov 16 2022
@author: c
=============================================================
"""
# import copy
# import numpy as np
Colordict={1:'ultra thick,black',2:'ultra thick,densely dotted,blue',3:'thick,brown,dashed',4:'red',5:'ultra thick,green,dashdotted',6:'black',7:'dashed',8:'gray',9:'ultra thick, blue'}



def draw_one_filling(strFlat,fill):
    filldict=dict({})
    i=1
    for item in fill:
        for x in list(item):
            filldict.update({x:i})
        i+=1
    # print(filldict)
    if '10' in strFlat:
        strFlat=strFlat.replace('10', 'x')
    rank_num=int(len(strFlat)/4)
    half=360/(4*rank_num)
    texpiece=[]
    tails = []
    for i in range(1,rank_num+1):
        if i < 10:
            tails.append(int(strFlat.rindex("O%i" %i)/2+1))
        elif i ==10:
            tails.append(int(strFlat.rindex("O%s" %'x')/2+1))
    # now we make a list for heads:
    heads = []
    for i in range(1,rank_num+1):
        if i < 10:
            heads.append(int(strFlat.rindex("U%i" %i)/2+1))
        elif i ==10:
            heads.append(int(strFlat.rindex("U%s" %'x')/2+1))

    # for i in range(1,rank_num+1):
        # tails.append(int(gcode.rindex("O%i" %i)/2+1))
    # for i in range(1,rank_num+1):
        # heads.append(int(gcode.rindex("U%i" %i)/2+1))
    for i in range(0,rank_num):
        # print( filldict)
        # print( filldict[i+1])
        # print( Colordict[filldict[i+1]])
        texpiece.append(
                r'\draw[-to,%s ] (%d:1cm) to[out=%d,in=%d] (%d:1cm);' %(
                    Colordict[filldict[i+1]],
                    90+(2*tails[i]-1)*half,
                    (2*tails[i]-1)*half-90,
                    (2*heads[i]-1)*half-90,
                    90+(2*heads[i]-1)*half
                    )
                )
    return '\n'.join(texpiece)


def draw_fillings(strFlat,fillings):
    textpiece=[]
    i=1
    for fill in eval(fillings):
        texpiece=[]
        texpiece.append(r'\begin{tikzpicture}')
        texpiece.append(r'\draw[] (0:1cm) arc (0:360:1cm);')
        texpiece.append(draw_one_filling(strFlat,fill))
        # texpiece.append(r'  \node at (270:1.25cm) {%s};' %strFlat)
        fill_str='%s' %fill
        fill_str=fill_str.replace('{', '(').replace('}', ')')
        texpiece.append(r'  \node at (270:1.25cm) {%s};' % fill_str)
        texpiece.append(r'  \node at (290:1.25cm) { };')
        texpiece.append(r'\end{tikzpicture}')
        textpiece.append(''.join(texpiece))
        i+=1
        if i>10:
            break
    return textpiece



