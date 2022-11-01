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
from flask import Flask, render_template, request
import pandas as pd
import checksymmetry
import gcodedrawer

app = Flask(__name__)

app.config['SECRET_KEY'] = '0000'


list_num = ['3,4,5','6','7']
aclist_num = ['5,6,7','8','9','10']

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
    'phi_sym_type': 'symmetry type of based matrix'}


poly_inv={
    'inPoly': 'inner characteristic polynomial',
    'outPoly': 'outer characteristic polynomial',
    'arrowpoly': 'arrow polynomial',
    'cable_arr_poly': '2-strand cable arrow polynomial'}

concor_inv={
    'genus': 'genus of based matrix',
    'mFilling(w/Gcode)': 'Fillings of based matrix',
    'slice': 'if K is slice' }

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

@app.route('/diagram/<gcode>')
def drawer(gcode):
    return render_template(
        'diagram.html',
        text=gcodedrawer.draw_arc(gcode)
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
            dflst=[]
            for crNum in num_list:
                print(crNum)
                in_path = './csv/fk_%s.csv' % (crNum)
                df= pd.read_csv(in_path,usecols=['namelink']+val_list, dtype=str)
                dflst.append(df)
    data=pd.concat(dflst)
    morelink=data.shape[0]>200
    data=data[0*200:0*200+200]
    return render_template('table.html',
            tables=[data[['namelink']+val_list].to_html(
                index=None,
                render_links=True,
                escape=False)], 
            # titles=[],
            pagenum=0,
            num_list=num_list,
            val_list=val_list,
            morelink=morelink
            )

@app.route('/result/<int:pagenum>/<numlist>/<invlist>')
def result_i(pagenum,numlist,invlist):
    num_list=numlist.replace('[','').replace(']','').replace("'","").replace(" ","").split(',')
    if invlist=='[]':
        val_list=[]
    else:
        val_list=invlist.replace('[','').replace(']','').replace("'","").replace(" ","").split(',')
    dflst=[]
    for crNum in num_list:
        print(crNum)
        in_path = './csv/fk_%s.csv' % (crNum)
        df= pd.read_csv(in_path,usecols=['namelink']+val_list, dtype=str)
        dflst.append(df)
    data=pd.concat(dflst)
    morelink=data.shape[0]>200*pagenum
    data=data[pagenum*200:pagenum*200+200]
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
    <h>Hello World!</h>
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
    elif int( knotname[0] )<8:
        in_path = './csv/fksame_%s.csv' % knotname[0]
    df= pd.read_csv(in_path, dtype=str)
    
    df=df[df['name']==knotname]
    r3_orbit=df.iloc[0]['r3_orbit']
    content= 'Min(phi) over symmetries of the knot is: '+df.iloc[0]['phi_sym'] +\
            '\n'+'Knots with same phi are :'+df.iloc[0]['same_phi']+'\n'+\
             'Outer characteristic polynomial of the knot is: '+\
             df.iloc[0]['outPoly'] +'\n'+'Knots with same outer characteristic polynomial are :'+df.iloc[0]['same_outpoly']+'\n'
    if int( knotname[0] )<7:
        content+='2-strand cable arrow polynomial of the knot is: '+df.iloc[0]['cable_arr_poly']\
            +'\n'+'Knots with same 2-strand cable arrow polynomial are :'+df.iloc[0]['same_cable_arr_poly']+'\n'
    return render_template(
        'flatknot.html',
        knotname=knotname,
        r3_orbit=r3_orbit,
        content=content,
           )




@app.route('/calculator', methods=['POST', 'GET'])
def calculator():
    var_1 = request.form.get("vgcode", type=str, default='O1+O2+O3+U1+U3+U2+')
    var_2 = request.form.get("gcode", type=str, default='O1O2O3U1U3U2')
    operation = request.form.get("operation")
    try:
        if operation == 'Min representation':
            result = checksymmetry.checkr2r1_recursive(var_2)
        elif operation == 'Symmetries':
            result = checksymmetry.checkmirrorimg(
                checksymmetry.checkr2r1_recursive(var_2))
        elif operation == 'R3 orbit':
            result = str(checksymmetry.checkR3(
                {checksymmetry.checkr2r1_recursive(var_2)}))
        elif operation == 'Virtual knot to flat knot':
            result = checksymmetry.vk2fk(var_1)
        else:
            result = ''
    except:
        result = 'Please check your Gauss code'
    entry = result
    return render_template('calculator.html',
            gcode=var_2,
            entry=entry)





if __name__ == '__main__':
    app.run(debug=True)
