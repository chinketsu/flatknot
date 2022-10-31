"""
=============================================================
Created on Jun 2 2021
modified on Oct 31 2022
@author: c
=============================================================
"""



def draw_arc(strFlat):
    textpiece=[]
    textpiece.append(r'\begin{tikzpicture}')
    # textpiece.append('\n')
    textpiece.append(r'\draw[] (0:1cm) arc (0:360:1cm);')
    # textpiece.append('\n')
    if '10' in strFlat:
        strFlat=strFlat.replace('10', 'x')
    rank_num=int(len(strFlat)/4)
    half=360/(4*rank_num)
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
