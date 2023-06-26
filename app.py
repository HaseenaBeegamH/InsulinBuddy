import json
import pickle

from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd

app=Flask(__name__)
## Load the model
regmodel=pickle.load(open('regmodel.pkl','rb'))
scalar=pickle.load(open('scaling.pkl','rb'))
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    cbg = request.form.get('cbg')
    daily_dose = request.form.get('dailydose')
    carbohydrate = request.form.get('carbohydrate')
    isf=request.form.get('isf')
    new_data=scalar.transform([[cbg,carbohydrate,daily_dose,isf]])
    output=regmodel.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict',methods=['POST'])
def predict():
    cbg = request.form.get('cbg')
    daily_dose = request.form.get('dailydose')
    carbohydrate = request.form.get('carbohydrate')
    isf=request.form.get('isf')
    final_input=scalar.transform([[cbg,carbohydrate,daily_dose,isf]])
    print(final_input)
    output=regmodel.predict(final_input)[0]
    return render_template("home.html",prediction_text="The insulin dosage prediction is {}".format(output))




if __name__=="__main__":
    app.run(debug=True)