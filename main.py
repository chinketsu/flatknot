"""test Flask with this"""
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

app.config['SECRET_KEY'] = '0000'


list_num = ['3,4,5','6','7']

list_valname = ['Gauss code',
                'based matrix from Gauss code',
                'primitive based matrix',
                'if the Based matrix from Gauss code primitive',
                'phi of primitive based matrix',
                'phi over symmetry',
                'inner characteristic polynomial',
                'outer characteristic polynomial',
                'inv_phi',
                'bar_phi',
                'invbar_phi',
                'symmetry type of based matrix',
                'Fillings of based matrix',
                'genus of based matrix',
                'arrow polynomial',
                '2-strand cable arrow polynomial']


list_val = ['gcode',
            'bsMtxNoSrt',
            'primMatrix',
            'isPrim',
            'phi',
            'phi_sym',
            'inPoly',
            'outPoly',
            'inv_phi',
            'bar_phi',
            'invbar_phi',
            'sym_type',
            'mFilling(w/Gcode)',
            'genus',
            'arrowpoly',
            'cable_arr_poly']


@app.route('/',methods=['GET','POST'])
def index():
    return render_template(
        'index.html',
        list_val=list_val,
        list_val_len=len(list_val),
        list_num=list_num,
        list_num_len=len(list_num),
        list_valname=list_valname
    )

    # if 'submit' in request.form():


@app.route('/result',methods=['POST', 'GET'])
def result():
    num_list=[]
    val_list=[]
    if request.method == 'POST':
        # result = request.form
        for i in range(len(list_num)):
            num_list.append(request.form.get('num%d' %i))
        for i in range(len(list_val)):
            val_list.append(request.form.get('val%d' %i))

        num_list=[j for j in num_list if j is not None]
        val_list=[j for j in val_list if j is not None]
        if num_list==[]:
            return '''
    <h>Please input a crossing number!</h>
    <div><a href='/flatknot/4/12'> Check the flat knot FK 4.12 </a></div>
    '''
        else:
            dflst=[]
            for crNum in num_list:
                print(crNum)
                in_path = './csv/fk_%s.csv' % (crNum)
                df= pd.read_csv(in_path,usecols=['name']+val_list, dtype=str)
                dflst.append(df)
            data=pd.concat(dflst)
    return render_template('table.html', tables=[data.to_html(index=None)], titles=[''])


@app.route('/error')
def hello():
    return '''
    <h>Hello World!</h>
    <div><a href='/flatknot/4/1'>FK 4.1 </a></div>
    '''


@app.route('/flatknot/<int:crossing_num>/<int:order_id>')
def orders(crossing_num, order_id):
    return f'<p>You are checking flat knot {crossing_num}.{order_id}.</p>'


if __name__ == '__main__':
    app.run(debug=True)
