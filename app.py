from flask import Flask, flash, redirect, render_template, request, session, abort
from werkzeug import secure_filename
#from flask import send_file
import pandas as pd
import pickle

# load the model from disk
loaded_model=pickle.load(open('Flight_pred.pkl', 'rb'))

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['xlsx','xls','csv'])
special_list=['-','@','#']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/')
def upload_file_renderer():
    return render_template('index.html', output_tables='')

@app.route('/', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(type(filename))
            new_filename=""
            for _ in filename:
                if _ not in special_list:
                    new_filename=new_filename+_
            file.save("excels/"+new_filename)
            df= pd.read_excel("excels/" + new_filename)
            big_df = df.copy()
            big_df['Date'] = big_df['Date_of_Journey'].str.split('/').str[0]
            big_df['Month'] = big_df['Date_of_Journey'].str.split('/').str[1]
            big_df['Year'] = big_df['Date_of_Journey'].str.split('/').str[2]
            big_df['Date'] = big_df['Date'].astype(int)
            big_df['Month'] = big_df['Month'].astype(int)
            big_df['Year'] = big_df['Year'].astype(int)
            big_df = big_df.drop(['Date_of_Journey'], axis=1)
            big_df['Arrival_Time'] = big_df['Arrival_Time'].str.split(' ').str[0]
            big_df[big_df['Total_Stops'].isnull()]
            big_df['Total_Stops'] = big_df['Total_Stops'].fillna('1 stop')
            big_df['Total_Stops'] = big_df['Total_Stops'].replace('non-stop', '0 stop')
            big_df['Stop'] = big_df['Total_Stops'].str.split(' ').str[0]
            big_df['Stop'] = big_df['Stop'].astype(int)
            big_df = big_df.drop(['Total_Stops'], axis=1)
            big_df['Arrival_Hour'] = big_df['Arrival_Time'].str.split(':').str[0]
            big_df['Arrival_Minute'] = big_df['Arrival_Time'].str.split(':').str[1]
            big_df['Arrival_Hour'] = big_df['Arrival_Hour'].astype(int)
            big_df['Arrival_Minute'] = big_df['Arrival_Minute'].astype(int)
            big_df = big_df.drop(['Arrival_Time'], axis=1)
            big_df['Departure_Hour'] = big_df['Dep_Time'].str.split(':').str[0]
            big_df['Departure_Minute'] = big_df['Dep_Time'].str.split(':').str[1]
            big_df['Departure_Hour'] = big_df['Departure_Hour'].astype(int)
            big_df['Departure_Minute'] = big_df['Departure_Minute'].astype(int)
            big_df = big_df.drop(['Dep_Time'], axis=1)
            big_df['Route_1'] = big_df['Route'].str.split('→ ').str[0]
            big_df['Route_2'] = big_df['Route'].str.split('→ ').str[1]
            big_df['Route_3'] = big_df['Route'].str.split('→ ').str[2]
            big_df['Route_4'] = big_df['Route'].str.split('→ ').str[3]
            big_df['Route_5'] = big_df['Route'].str.split('→ ').str[4]
            big_df['Route_1'].fillna("None", inplace=True)
            big_df['Route_2'].fillna("None", inplace=True)
            big_df['Route_3'].fillna("None", inplace=True)
            big_df['Route_4'].fillna("None", inplace=True)
            big_df['Route_5'].fillna("None", inplace=True)
            big_df = big_df.drop(['Route'], axis=1)
            big_df = big_df.drop(['Duration'], axis=1)
            from sklearn.preprocessing import LabelEncoder
            encoder = LabelEncoder()
            big_df["Airline"] = encoder.fit_transform(big_df['Airline'])
            big_df["Source"] = encoder.fit_transform(big_df['Source'])
            big_df["Destination"] = encoder.fit_transform(big_df['Destination'])
            big_df["Additional_Info"] = encoder.fit_transform(big_df['Additional_Info'])
            big_df["Route_1"] = encoder.fit_transform(big_df['Route_1'])
            big_df["Route_2"] = encoder.fit_transform(big_df['Route_2'])
            big_df["Route_3"] = encoder.fit_transform(big_df['Route_3'])
            big_df["Route_4"] = encoder.fit_transform(big_df['Route_4'])
            big_df["Route_5"] = encoder.fit_transform(big_df['Route_5'])
            big_df = big_df.drop(['Year'], axis=1)



            my_prediction = loaded_model.predict(big_df.iloc[:, :].values)
            df['Pred'] = my_prediction
            if len(df.index) > 0:
                return render_template('index.html', output_tables=[df.to_html(classes='data')])
            else:
                return render_template('index.html', output_tables='')

        else:
            flash("Select excel file")
            return redirect('/')
    else:
        print("Here----")
        return redirect('/')
        

if __name__ == "__main__":
    app.run(debug=True)
    

