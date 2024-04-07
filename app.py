from flask import Flask,render_template,request
import joblib
import numpy as np
import pandas as pd

model = joblib.load('model_save')
train_df=joblib.load('train_df_save')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result',methods=['post'])
def recommend():
    precipitation = request.form.get('precipitation')
    temp_max = request.form.get('temp_max')
    temp_min = request.form.get('temp_min')
    wind = request.form.get('wind')
    date = request.form.get('date')
    columns=train_df.columns
    np_arr=np.array([[0,0,0,0,0,0,0,0]])
    prediction=pd.DataFrame(np_arr,columns=columns)
    try:
        if precipitation:
            precipitation=float(precipitation)
        else:
            precipitation=0.00

        if temp_max:
            temp_max=float(temp_max)
        else:
            temp_max=0.00

        if temp_min:
            temp_min=float(temp_min)
        else:
            temp_min=0.00

        if wind:
            wind=float(wind)
        else:
            wind=0.00
        
        # print(type(precipitation))
        # print(type(temp_max))
        # print(type(temp_min))
        # print(type(wind))
        print(date)
        prediction['precipitation']=precipitation
        prediction['temp_max']=temp_max
        prediction['temp_min']=temp_min
        prediction['wind']=wind

        month=date[5:7]
        month=int(month)
        print(month)
        print(type(month))
        seasons={1:'Winter',
            2:'Winter',
            3:'Spring',
            4:'Spring',
            5:'Spring',
            6:'Summer',
            7:'Summer',
            8:'Summer',
            9:'Autumn',
            10:'Autumn',
            11:'Autumn',
            12:'Winter'}
        prediction['season_'+seasons[month]]=1
        answer=model.predict(prediction)[0]
        weather_keys={0: 'drizzle', 2: 'rain', 4: 'sun', 3: 'snow', 1: 'fog'}
        image=weather_keys[answer]
        return render_template('result.html',image=image)
    except:
        return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)