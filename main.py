"""
Wed oct 19
Powered by Jie Chen.
# main.py
This is the main flask app
To run this on local laptop:
conda activate flask
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
"""
from flask import Flask, render_template, request, redirect
import pandas as pd
import checksymmetry
import draw_filling

app = Flask(__name__)

app.config['SECRET_KEY'] = '0000'

filedict={'3':1,'4':1,'5':1,'6':5,'7':93}
acfiledict={'5':1,'6':1,'7':1,'8':1,'9':1,'10':4}

list_num = ['3','4','5','6','7']
aclist_num = ['5','6','7','8','9','10']

noexist='Under construction. Coming soon...'

diag_inv={
    'gcode': 'Gauss code',
    'r3_orbit': 'R3 orbit',
    'r3_orbit_length': 'R3 orbit length',
    'inv': 'Gauss code of inv(K)',
    'bar': 'Gauss code of bar(K)',
    'invbar': 'Gauss code of invbar(K)',
    'diag_sym_type': 'Diagrammatic symmetry type'}

matrix_inv={
    'bsMtxNoSrt':'Based matrix from Gauss code',
    'primMatrix':'Primitive based matrix',
    'isPrim':'If based matrix primitive',
    'phi':'Phi of primitive based matrix',
    'phi_sym':'Phi over symmetry',
    'inv_phi': 'Phi of inv(K)',
    'bar_phi': 'Phi of bar(K)',
    'invbar_phi': 'Phi of invbar(K)',
    'matrix_sym_type': 'Symmetry type of based matrix'}


poly_inv={
    'inPoly': 'Inner characteristic polynomial',
    'outPoly': 'Outer characteristic polynomial',
    'arrowpoly': 'Arrow polynomial',
    'cable_arr_poly': '2-strand cable arrow polynomial'}

concor_inv={
    'alg_genus': 'Genus of based matrix',
    'fillings': 'Fillings of based matrix',
    'slice': 'If K is slice'}

dict_inv={ 'diagrammatic invariants': diag_inv,
    'matrix invariants': matrix_inv,
    'polynomial invariants': poly_inv,
    'concordance invariants': concor_inv,}

all_dict = {**diag_inv, **matrix_inv, **poly_inv, **concor_inv}


all_inv= sum([list(value.keys()) for value in dict_inv.values()],[])

all_invname= sum([list(value.values()) for value in dict_inv.values()],[])


@app.route('/',methods=['GET','POST'])
def index():
    return render_template(
        'index.html',
        list_num=list_num,
        list_num_len=len(list_num),
        dict_inv=dict_inv,
        # diag_inv=diag_inv,
        # matrix_inv=matrix_inv,
        # poly_inv=poly_inv,
        # concor_inv=concor_inv,
    )


@app.route('/ac',methods=['GET','POST'])
def acindex():
    return render_template(
        'acindex.html',
        list_num=aclist_num,
        list_num_len=len(aclist_num),
        dict_inv=dict_inv,
        # diag_inv=diag_inv,
        # matrix_inv=matrix_inv,
        # poly_inv=poly_inv,
        # concor_inv=concor_inv,
    )


@app.route('/inv/<invname>')
def invpage(invname):
    content_list=[noexist]
    df=pd.read_csv('./csv/inv.csv',dtype=str)
    text=df.loc[df.invname==invname].iloc[0]['Definition']
    if text !='0':
        content_list.append(text)
    return render_template(
        'list.html',
        headname=all_dict[invname],
        content_list=content_list,
    )


@app.route('/glossary')
def glossary():
    content_list=[noexist]
    return render_template(
        'list.html',
        headname='Glossary',
        content_list=content_list,
    )


@app.route('/todo')
def todo():
    content_list=[noexist]
    return render_template(
        'list.html',
        headname='Todo List',
        content_list=content_list,
    )


@app.route('/conjecture')
def conjecture():
    content_list=[noexist]
    return render_template(
        'list.html',
        headname='Conjecture List',
        content_list=content_list,
    )



@app.route('/ref')
def ref():
    content_list=[noexist]
    return render_template(
        'list.html',
        headname='Reference List',
        content_list=content_list,
    )



@app.route('/diagram/<gcode>')
def drawer(gcode):
    return render_template(
        'diagram.html',
        text=checksymmetry.draw_arc(gcode)
    )


@app.route('/fillings/<gcode>/<fillings>')
def fillings(gcode,fillings):
    return render_template(
        'fillings.html',
        text=draw_filling.draw_fillings(gcode, fillings)
    )


@app.route('/crossref/<int:pagenum>')
def crossref(pagenum):
    df= pd.read_csv(
        './csv/crossref.csv',
        dtype=str,
        skiprows=range(1,600*pagenum+1),
        nrows=600)
    return render_template(
        'crossref.html',
        tables=[
            df[200*i:200*i+200].
            to_html(index=None, render_links=True, escape=False)
            for i in range(0,int(df.shape[0]/200.0+0.5))
        ],
        pagenum=pagenum,
    )


@app.route('/result',methods=['POST', 'GET'])
def result():
    num_list=[]
    val_list=[]
    if request.method == 'POST':
        # result = request.form
        for i in range(len(list_num)):
            num_list.append(request.form.get('num%d' %i))
        for invname in all_inv:
            val_list.append(request.form.get(invname))

        num_list=[j for j in num_list if j is not None]
        val_list=[j for j in val_list if j is not None]
        if num_list==[]:
            return '''
    <h>Please input a crossing number!</h>
    <div><a href='/calculator'> Check the flat knot diagram calculator !</a></div>
    <div><a href='/'> Go back</a></div>
    '''
        else:
            morelink=False
            dflst=[]
            dfsize=0
            pagenum=1
            for crNum in num_list:
                for fileNum in range(1,filedict[crNum]+1):
                    in_path = './csv/fk_%s_%d.csv' % (crNum,fileNum)
                    df= pd.read_csv(
                        in_path,
                        usecols=['namelink']+val_list,
                        dtype=str)
                    dfsize+=df.shape[0]
                    dflst.append(df)
                    if dfsize>=500:
                        num_index=num_list.index(crNum)
                        morelink=True
                        pagenum=1
                        return render_template(
                            'table.html',
                            tables=[pd.concat(dflst)[['namelink']+val_list].to_html(
                                index=None,
                                render_links=True,
                                escape=False)],
                            # titles=[],
                            pagenum=pagenum,
                            num_list=num_list[num_index:],
                            val_list=val_list,
                            morelink=morelink
                        )
            return render_template(
                'table.html',
                tables=[pd.concat(dflst)[['namelink']+val_list].to_html(
                    index=None,
                    render_links=True,
                    escape=False)],
                # titles=[],
                pagenum=pagenum,
                val_list=val_list,
                num_list=num_list,
                morelink=morelink
            )


@app.route('/result/<int:pagenum>/<numlist>/<invlist>')
def result_i(pagenum,numlist,invlist):
    morelink=True
    num_list=numlist.replace('[','').replace(']','').replace("'","").replace(" ","").split(',')
    if invlist=='[]':
        val_list=[]
    else:
        val_list=invlist.replace('[','').replace(']','').replace("'","").replace(" ","").split(',')

    if pagenum==0:
        return redirect(f'/result/{filedict[num_list[0]]}/{num_list}/{val_list}')

    if filedict[num_list[0]]<pagenum:
        # pagenum=1
        # num_list=num_list[1:]
        if len(num_list)==1:
            # morelink=False
            return redirect(f'/result/{filedict[num_list[0]]}/{num_list}/{val_list}')
        else:
            num_list=num_list[1:]
            pagenum=filedict[num_list[0]]-pagenum
            return redirect(f'/result/{pagenum}/{num_list}/{val_list}')
    morelink=filedict[num_list[0]]>pagenum or len(num_list)>1
    in_path = './csv/fk_%s_%d.csv' % (num_list[0],pagenum)
    data= pd.read_csv(in_path,usecols=['namelink']+val_list, dtype=str)
    return render_template('table.html',
            tables=[data[['namelink']+val_list].to_html(
                index=None,
                render_links=True,
                escape=False)],
            pagenum=pagenum,
            num_list=num_list,
            val_list=val_list,
            morelink=morelink
            )


@app.route('/acresult',methods=['POST', 'GET'])
def acresult():
    num_list=[]
    val_list=[]
    if request.method == 'POST':
        # result = request.form
        for i in range(len(aclist_num)):
            num_list.append(request.form.get('num%d' %i))
        for invname in all_inv:
            val_list.append(request.form.get(invname))

        num_list=[j for j in num_list if j is not None]
        val_list=[j for j in val_list if j is not None]
        if num_list==[]:
            return '''
    <h>Please input a crossing number!</h>
    <div><a href='/calculator'> Check the flat knot diagram calculator !</a></div>
    <div><a href='/'> Go back</a></div>
    '''
        else:
            morelink=False
            dflst=[]
            dfsize=0
            pagenum=1
            for crNum in num_list:
                for fileNum in range(1,acfiledict[crNum]+1):
                    in_path = './csv/ac_%s_%d.csv' % (crNum,fileNum)
                    df= pd.read_csv(
                        in_path,
                        usecols=['namelink']+val_list,
                        dtype=str)
                    dfsize+=df.shape[0]
                    dflst.append(df)
                    if dfsize>=500:
                        num_index=num_list.index(crNum)
                        morelink=True
                        pagenum=1
                        return render_template(
                            'actable.html',
                            tables=[pd.concat(dflst)[['namelink']+val_list].to_html(
                                index=None,
                                render_links=True,
                                escape=False)],
                            # titles=[],
                            pagenum=pagenum,
                            num_list=num_list[num_index:],
                            val_list=val_list,
                            morelink=morelink
                        )
            return render_template(
                'actable.html',
                tables=[pd.concat(dflst)[['namelink']+val_list].to_html(
                    index=None,
                    render_links=True,
                    escape=False)],
                # titles=[],
                pagenum=pagenum,
                val_list=val_list,
                num_list=num_list,
                morelink=morelink
            )





@app.route('/acresult/<int:pagenum>/<numlist>/<invlist>')
def acresult_i(pagenum,numlist,invlist):
    morelink=True
    num_list=numlist.replace('[','').replace(']','').replace("'","").replace(" ","").split(',')
    if invlist=='[]':
        val_list=[]
    else:
        val_list=invlist.replace('[','').replace(']','').replace("'","").replace(" ","").split(',')

    if pagenum==0:
        return redirect(f'/acresult/{acfiledict[num_list[0]]}/{num_list}/{val_list}')

    if acfiledict[num_list[0]]<pagenum:
        # pagenum=1
        # num_list=num_list[1:]
        if len(num_list)==1:
            # morelink=False
            return redirect(f'/acresult/{acfiledict[num_list[0]]}/{num_list}/{val_list}')
        else:
            num_list=num_list[1:]
            pagenum=acfiledict[num_list[0]]-pagenum
            return redirect(f'/acresult/{pagenum}/{num_list}/{val_list}')

    morelink=acfiledict[num_list[0]]>pagenum or len(num_list)>1

    in_path = './csv/ac_%s_%d.csv' % (num_list[0],pagenum)
    data= pd.read_csv(in_path,usecols=['namelink']+val_list, dtype=str)
    return render_template('actable.html',
            tables=[data[['namelink']+val_list].to_html(
                index=None,
                render_links=True,
                escape=False)],
            pagenum=pagenum,
            num_list=num_list,
            val_list=val_list,
            morelink=morelink
            )


@app.route('/download/<numlist>/<invlist>')
def download(numlist,invlist):
    return '''
    <h>Coming Soon!</h>
    <div><a href='/#contact'>
    Email us if you need it sooner.
    </a>
    </div>
    '''






@app.route('/citeus')
def citeus():
    return render_template( 'citeus.html')


@app.route('/error')
def hello():
    return '''
    <h>Hey, it seems like you are checking something new</h>
    <h>Or your input is not formatted.</h>
    <h>Please try again.</h>
    <h>Or contact me and I will calculate for you.</h>
    <div><a href='/'> Go to the Main Page</a></div>
    <div><a href='/calculator'> Go to Calculator</a></div>
    <div><a href='/#contact'>Contact us</a></div>
    '''


@app.route('/flatknot/<knotname>')
def flatknot(knotname):
    if knotname=='0':
        return render_template(
            'flatknot.html',
            knotname=knotname,
            r3_orbit='',
            content='Trivial flat knot.')
    elif int(knotname[0])>7:
        return redirect('/error')
    else:
        rownum=(int(knotname[2:])-1) % 500 +1
        filenum=int((int(knotname[2:])-rownum)/500)+1
        in_path2 = './csv/fk_%s_%d.csv' % (knotname[0],filenum)
        df= pd.read_csv(in_path2, dtype=str, skiprows=range(1,rownum), nrows=2)

        df=df[df['name']==knotname]
        content='Min(phi) over symmetries of the knot is: '+df.iloc[0]['phi_sym'] +\
            '\n'+'Flat knots (up to 7 crossings) with same phi are :'+df.iloc[0]['same_phi']+'\n'+\
            'Arrow polynomial of the knot is: '+df.iloc[0]['arrowpoly'] +'\n'+\
            'Flat knots (up to 7 crossings) with same arrow polynomial are :'+df.iloc[0]['same_arrowpoly']+'\n'+\
             'Outer characteristic polynomial of the knot is: '+\
             df.iloc[0]['outPoly'] +'\n'+'Flat knots (up to 7 crossings) with same outer characteristic polynomial are :'+df.iloc[0]['same_outPoly']+'\n'
        if int(knotname[0])<7:
            content+='2-strand cable arrow polynomial of the knot is: '+df.iloc[0]['cable_arr_poly']\
            +'\n'+'Flat knots (up to 6 crossings) with same 2-strand cable arrow polynomial are :'+df.iloc[0]['same_cable_arr_poly']\
            +'\n'+'Virtual knots (up to 6 crossings) projecting to this knot are :'+df.iloc[0]['sameflatknot'].replace("[\'","\'vk").replace(" \'"," \'vk")
        fillings=eval(df.iloc[0]['fillings'])
        if len(fillings)>10:
            fillings=fillings[:10]
        gcode=df.iloc[0]['gcode']
        data=df[all_inv].transpose().reset_index().rename(columns={0:'value'})
        data['invariant']=data['index'].apply(lambda x: all_dict[x])
        data=data[['invariant','value']]
        return render_template(
            'flatknot.html',
            knotname=knotname,
            r3_orbit=df.iloc[0]['r3_orbit'],
            diag_sym_type=df.iloc[0]['diag_sym_type'],
            inv=df.iloc[0]['inv'],
            bar=df.iloc[0]['bar'],
            invbar=df.iloc[0]['invbar'],
            gcode=gcode,
            fillings=fillings,
            content=content,
            tables=[data.to_html(
                    index=None,
                    render_links=True,
                    escape=False)])


@app.route('/acflatknot/<knotname>')
def acflatknot(knotname):
    if knotname=='0':
        return render_template(
            'flatknot.html',
            knotname=knotname,
            r3_orbit='',
            content='You are checking the trivial flat knot. All the invariants are trivial as well.',
            )
    if knotname[:2]=='10':
        crNum=10
        # rownum=int(knotname[3:]) % 500
        rownum=(int(knotname[3:])-1)% 500 +1
        filenum=int((int(knotname[3:])-rownum)/500)+1
    else:
        crNum=int(knotname[0])
        # rownum=int(knotname[2:]) % 500
        rownum=( int(knotname[2:])-1 ) % 500 +1
        filenum=int((int(knotname[2:])-rownum)/500)+1
    in_path2 = './csv/ac_%d_%d.csv' % (crNum,filenum)
    df2= pd.read_csv(in_path2, dtype=str, skiprows=range(1,rownum), nrows=2)
    df=df2[df2['name']==knotname]
    fillings=eval(df.iloc[0]['fillings'])
    if len(fillings)>10:
        fillings=fillings[:10]
    gcode=df.iloc[0]['gcode']
    data=df[all_inv].transpose().reset_index().rename(columns={0:'value'})
    data['invariant']=data['index'].apply(lambda x: all_dict[x])
    data=data[['invariant','value']]
    if knotname[:2]=='10':
        return render_template(
            'acflatknot.html',
            knotname=knotname,
            r3_orbit='',
            diag_sym_type='',
            inv='',
            bar='',
            invbar='',
            gcode=gcode,
            fillings=fillings,
            tables=[data.to_html(
                    index=None,
                    render_links=True,
                    escape=False)])
    return render_template(
        'acflatknot.html',
        knotname=knotname,
        r3_orbit=df2.iloc[0]['r3_orbit'],
        diag_sym_type=df2.iloc[0]['diag_sym_type'],
        inv=df2.iloc[0]['inv'],
        bar=df2.iloc[0]['bar'],
        invbar=df2.iloc[0]['invbar'],
        gcode=gcode,
        fillings=fillings,
        tables=[data.to_html(
                index=None,
                render_links=True,
                escape=False)],
           )


# @app.route('/calculator0', methods=['POST', 'GET'])
# def calculator0():
    # var_1 = request.form.get("vgcode", type=str, default='O1+O2+O3+U1+U3+U2+')
    # var_2 = request.form.get("gcode", type=str, default='O1O2O3U1U3U2')
    # operation = request.form.get("operation")
    # try:
        # if operation == 'Min representation':
            # result = checksymmetry.checkr2r1_recursive_orbit(var_2)
        # elif operation == 'Symmetries':
            # result = checksymmetry.checkmirrorimg(
                # checksymmetry.checkr2r1_recursive_orbit(var_2))
        # elif operation == 'R3 orbit':
            # result = str(checksymmetry.checkR3(
                # {checksymmetry.checkr2r1_recursive_orbit(var_2)}))
        # elif operation == 'Virtual knot to flat knot':
            # result = checksymmetry.vk2fk(var_1)
        # else:
            # result = ''
    # except:
        # result = 'Please check your Gauss code'
    # entry = result
    # return render_template('calculator0.html',
            # gcode=var_2,
            # entry=entry)


def findgcode(gcode):
    if '8' in gcode:
        return 'Currently cannot search for 8 crossing or larger'
    crNum=int(len(gcode)/4)
    pdlist=[]
    for i in range(1,filedict['%d' %crNum]+1):
        out_path = './csv/fk_%d_%d.csv' % (crNum,i)
        pdlist.append(pd.read_csv(out_path,dtype=str,usecols=['name','gcode']))
    df=pd.concat(pdlist)
    return df[df.gcode==gcode].iloc[0]['name']



@app.route('/calculator', methods=['POST', 'GET'])
def calculator():
    question = request.form.get("question")
    return render_template('calculator.html',question=question)




@app.route('/calculator/<question>', methods=['POST', 'GET'])
def calculatorpage2(question):
    question2=''
    content= ''
    placeholdertext=''
    name='Not yet input'
    gcode = request.form.get("gcode", type=str, default='')
    gcode = gcode.replace(' ','')
    todraw=[]
    r3todraw=[]
    if question== 'gvk2fk':
        question2='Please input the Gauss code for virtual knot:'
        placeholdertext='O1+O2+O3+U1+U3+U2+'
        # ifchecked1='checked'
        if gcode != '':
            name=''
            fgcode=checksymmetry.vk2fk(gcode)
            if not checksymmetry.checkvalidgcode(fgcode):
                return redirect('/error')
            mingcode= checksymmetry.checkr2r1_recursive_orbit(fgcode)
            pretty_mingcode= checksymmetry.let2int(mingcode)
            if mingcode !='':
                minsibling= checksymmetry.let2int(
                    checksymmetry.minsibling(mingcode))
                r3set=[
                    checksymmetry.let2int(code)
                    for code in checksymmetry.checkR3(mingcode)]
                content = r'Your input is virtual knot '\
                    + gcode + '.\nIt projects to flat knot diagram '\
                    + fgcode+'.\n Its minimal representation is '\
                    + pretty_mingcode\
                    +'.\n Its minimal sibling is '\
                    + minsibling+'.\n Its R3 orbit is '\
                    + str(r3set)
                todraw=[fgcode,pretty_mingcode,minsibling]
                r3todraw=list(r3set)
                name=findgcode(minsibling)
            else:
                content = r'Your input is virtual knot '\
                    + gcode + '.\nIt projects to the trivial flat knot.'
    elif question== 'gfk2fk':
        question2='Please input the Gauss code for flat knot:'
        placeholdertext='O1O2O3U1U3U2'
        # ifchecked2='checked'
        if gcode != '':
            name=''
            if not checksymmetry.checkvalidgcode(gcode):
                return redirect('/error')
            mingcode= checksymmetry.checkr2r1_recursive_orbit(gcode)
            pretty_mingcode= checksymmetry.let2int(mingcode)
            if mingcode !='':
                minsibling= checksymmetry.let2int(
                    checksymmetry.minsibling(mingcode))
                r3set=[
                    checksymmetry.let2int(code)
                    for code in checksymmetry.checkR3(mingcode)]
                content = r'Your input is flat knot '\
                    + gcode+'.\n Its minimal representation is '\
                    + pretty_mingcode\
                    + '.\n Its minimal sibling is '\
                    + minsibling+'.\n Its R3 orbit is '\
                    + str(r3set)
                todraw=[pretty_mingcode,minsibling]
                r3todraw=list(r3set)
                name=findgcode(minsibling)
            else:
                content = r'Your input is flat knot '\
                    + gcode + ',\n which is the trivial flat knot.'
    elif question== 'nfk2fk':
        question2='Please input a flat knot name here'
        placeholdertext='5.22'
        # ifchecked3='checked'
        content= "If your input is valid, the information of the flat knot is:"
        name=gcode
    return render_template(
        'calculatorpage2.html',
        name=name,
        question2=question2,
        todraw=todraw,
        r3todraw=r3todraw,
        content=content,
        placeholdertext=placeholdertext)








if __name__ == '__main__':
    app.run(debug=True)
