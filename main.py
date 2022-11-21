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
import gcodedrawer
import draw_filling

app = Flask(__name__)

app.config['SECRET_KEY'] = '0000'

filedict={'3':1,'4':1,'5':1,'6':5,'7':93}
acfiledict={'5':1,'6':1,'7':1,'8':1,'9':1,'10':4}

list_num = ['3','4','5','6','7']
aclist_num = ['5','6','7','8','9','10']

diag_inv={
    'gcode': 'Gauss code',
    'r3_orbit': 'R3 orbit',
    'r3_orbit_length': 'R3 orbit length',
    'inv': 'Gauss code of inv(K)',
    'bar': 'Gauss code of bar(K)',
    'invbar': 'Gauss code of invbar(K)',
    'diag_sym_type': 'diagrammatic symmetry type'}

matrix_inv={
    'bsMtxNoSrt':'based matrix from Gauss code',
    'primMatrix':'primitive based matrix',
    'isPrim':'if based matrix primitive',
    'phi':'phi of primitive based matrix',
    'phi_sym':'phi over symmetry',
    'inv_phi': 'phi of inv(K)',
    'bar_phi': 'phi of bar(K)',
    'invbar_phi': 'phi of invbar(K)',
    'matrix_sym_type': 'symmetry type of based matrix'}


poly_inv={
    'inPoly': 'inner characteristic polynomial',
    'outPoly': 'outer characteristic polynomial',
    'arrowpoly': 'arrow polynomial',
    'cable_arr_poly': '2-strand cable arrow polynomial'}

concor_inv={
    'alg_genus': 'genus of based matrix',
    'fillings': 'Fillings of based matrix that gives the genus',
    'slice': 'if K is slice'}

dict_inv={ 'diagrammatic invariants': diag_inv,
    'matrix invariants': matrix_inv,
    'polynomial invariants': poly_inv,
    'concordance invariants': concor_inv,}


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
def inv(invname):
    return f'''
    <p>You are checking flat knot invariant {invname},
    but we have not updated it yet. Sorry.
    </p>
    '''

@app.route('/glossary')
def glossary():
    return f'''
    <p> We have not updated it yet. Sorry. </p>
    <div><a href='/calculator'> Check the flat knot diagram calculator !</a></div>
    <div><a href='/'> Go back</a></div>
    '''


@app.route('/todo')
def todo():
    return f'''
    <p> We have not updated it yet. Sorry. </p>
    <div><a href='/calculator'> Check the flat knot diagram calculator !</a></div>
    <div><a href='/'> Go back</a></div>
    '''

@app.route('/conjecture')
def conjecture():
    return f'''
    <p> We have not updated it yet. Sorry. </p>
    <div><a href='/calculator'> Check the flat knot diagram calculator !</a></div>
    <div><a href='/'> Go back</a></div>
    '''

@app.route('/ref')
def ref():
    return f'''
    <p> We have not updated it yet. Sorry. </p>
    <div><a href='/calculator'> Check the flat knot diagram calculator !</a></div>
    <div><a href='/'> Go back</a></div>
    '''





@app.route('/diagram/<gcode>')
def drawer(gcode):
    return render_template(
        'diagram.html',
        text=gcodedrawer.draw_arc(gcode)
    )

@app.route('/fillings/<gcode>/<fillings>')
def fillings(gcode,fillings):
    return render_template(
        'fillings.html',
        text=draw_filling.draw_fillings(gcode, fillings)
    )

@app.route('/crossref/<int:pagenum>')
def crossref(pagenum):
    return render_template(
        'crossref.html',
        tables=[pd.read_csv('./csv/crossref.csv',dtype=str)[pagenum*200:pagenum*200+200].to_html(
                index=None,
                render_links=True,
                escape=False)], 
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
    <h>Hey</h>
    <div><a href='/flatknot/4.1'>FK 4.1 </a></div>
<a style='display:block;' href='/flatknot/4.4'><div>4.4</div></a>
    '''


@app.route('/flatknot/<knotname>')
def flatknot(knotname):
    if knotname=='0':
        return render_template(
            'flatknot.html',
            knotname=knotname,
            r3_orbit='',
            content='You are checking the trivial flat knot. All the invariants are trivial as well.',
               )
    if int( knotname[0] ) <6:
        in_path = './csv/fksame_%s.csv' % (5)
        df= pd.read_csv(in_path, dtype=str)
    elif int( knotname[0] )<8:
        in_path = './csv/fksame_%s.csv' % knotname[0]
        df= pd.read_csv(in_path, dtype=str, skiprows=range(1,int(knotname[2:])), nrows=4)
    df=df[df['name']==knotname]
    content='Min(phi) over symmetries of the knot is: '+df.iloc[0]['phi_sym'] +\
            '\n'+'Knots (up to 7 crossings) with same phi are :'+df.iloc[0]['same_phi']+'\n'+\
             'Outer characteristic polynomial of the knot is: '+\
             df.iloc[0]['outPoly'] +'\n'+'Knots (up to 7 crossings) with same outer characteristic polynomial are :'+df.iloc[0]['same_outpoly']+'\n'
    if int(knotname[0])<7:
        content+='2-strand cable arrow polynomial of the knot is: '+df.iloc[0]['cable_arr_poly']\
            +'\n'+'Knots (up to 6 crossings) with same 2-strand cable arrow polynomial are :'+df.iloc[0]['same_cable_arr_poly']\
            +'\n'+'Virtual knots (up to 6 crossings) projecting to this knot are :'+df.iloc[0]['sameflatknot']

    rownum=int(knotname[2:]) % 500
    filenum=int((int(knotname[2:])-rownum)/500)+1
    in_path2 = './csv/fk_%s_%d.csv' % (knotname[0],filenum)
    df2= pd.read_csv(in_path2, dtype=str, skiprows=range(1,rownum), nrows=2)
    fillings=df2[df2['name']==knotname].iloc[0]['fillings']
    gcode=df2[df2['name']==knotname].iloc[0]['gcode']
    data=df2[df2['name']==knotname].transpose().reset_index().rename(columns={0:'','index':''})
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
                escape=False)],
           )





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
        rownum=int(knotname[3:]) % 500
        filenum=int((int(knotname[3:])-rownum)/500)+1
    else:
        crNum=int(knotname[0])
        rownum=int(knotname[2:]) % 500
        filenum=int((int(knotname[2:])-rownum)/500)+1
    in_path2 = './csv/ac_%d_%d.csv' % (crNum,filenum)
    df2= pd.read_csv(in_path2, dtype=str, skiprows=range(1,rownum), nrows=2)
    fillings=df2[df2['name']==knotname].iloc[0]['fillings']
    gcode=df2[df2['name']==knotname].iloc[0]['gcode']
    data=df2[df2['name']==knotname].transpose().reset_index().rename(columns={0:'','index':''})

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
                    escape=False)],
               )


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
    crNum=int(len(gcode)/4)
    if 3<=crNum<=5:
        crNum=5
    df= pd.read_csv('./csv/fksame_%d.csv' %crNum,usecols=['name','gcode'], dtype=str)
    if crNum>8:
        return 'Not yet updated for cr>=8'
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
    name=''
    gcode = request.form.get("gcode", type=str, default='')
    todraw=[]
    if question== 'gvk2fk':
        question2='Please input the Gauss code for virtual knot:'
        placeholdertext='O1+O2+O3+U1+U3+U2+'
        ifchecked1='checked'
        if gcode != '':
            fgcode=checksymmetry.vk2fk(gcode)
            mingcode= checksymmetry.checkr2r1_recursive_orbit(fgcode)
            if mingcode !='':
                minsibling= checksymmetry.minsibling(mingcode)
                content = r'Your input is virtual knot '\
                    + gcode + '.\nIt projects to flat knot diagram '\
                    + fgcode+'.\n Its minimal representation is '\
                    + mingcode+'.\n Its minimal sibling is '\
                    +minsibling+'.\n The flat knot name is:'
                todraw=[fgcode,mingcode,minsibling]
                name=findgcode(minsibling)
            else:
                content == r'Your input is virtual knot '\
                    + gcode + '.\nIt projects to the trivial flat knot.'



    elif question== 'gfk2fk':
        question2='Please input the Gauss code for flat knot:'
        placeholdertext='O1O2O3U1U3U2'
        ifchecked2='checked'
        if gcode != '':
            mingcode= checksymmetry.checkr2r1_recursive_orbit(gcode)
            if mingcode !='':
                minsibling= checksymmetry.minsibling(mingcode)
                content = r'Your input is flat knot '\
                    + gcode+'.\n Its minimal representation is '\
                    + mingcode+'.\n Its minimal sibling is '\
                    +minsibling+'.\n The flat knot name is:'
                todraw=[gcode,mingcode,minsibling]
                name=findgcode(minsibling)
            else:
                content = r'Your input is flat knot '\
                    + gcode + ',\n which is the trivial flat knot.'


    elif question== 'nfk2fk':
        question2='Please input a flat knot name here'
        placeholdertext='5.22'
        ifchecked3='checked'
        content= "If your input is valid, the information of the flat knot is:"
        name=gcode


    return render_template('calculatorpage2.html',
            name=name,
            question2=question2,
            todraw=todraw,
            content=content,
            placeholdertext=placeholdertext)








if __name__ == '__main__':
    app.run(debug=True)
