# other
import os
from datetime import datetime
# flask 
from flask import Flask, render_template, request, redirect, flash
# my function for prediction
from function import load_dl_models, feature_extraction, feature_selection, svm_prediction

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Set up the upload folder
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/aboutUs")
def aboutUs():
    return render_template('aboutUs.html')

@app.route("/predictionSamples", methods = ['POST'])
def predictionSamples():
    if request.method == 'POST':
        print(request.form)
        
        pathSamples = request.form['pathSamples']
        speciesSamples = request.form['speciesSamples']

        if pathSamples == '':
            flash('Please select sample !!')
            return redirect('main')
        
        if speciesSamples == '' or speciesSamples == 0:
            flash('Plases select plant species !!')
            return redirect('main')
        
        # file_ext = file.filename.rsplit('.', 1)[1].lower()
        # current_date = datetime.now().strftime('%Y%m%d_%H%M%S')
        # new_filename = f"{current_date}.{file_ext}"
        # filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        # file.save(filepath)
        
        # prediction
        species = int(speciesSamples)
        model = load_dl_models(species)
        df_features = feature_extraction(f"static/{pathSamples}", model)
        selected_df_features = feature_selection(df_features, species)
        sorted_prob = svm_prediction(selected_df_features, species)
        if int(species) == 1:
            text_species = "Tomato"
        elif int(species) == 2:
            text_species = "Sugarcane"
        else: 
            text_species = "Corn"


        return render_template('result.html', species= text_species, result_prob=  sorted_prob, filepath=f"{pathSamples}")
        # else:
        #     flash('Invalid file type. Only PNG, JPG, and JPEG are allowed.')
        #     return redirect('main')
    else:
        return redirect('main')

@app.route("/prediction", methods = ['POST'])
def prediction():
    if request.method == 'POST':
        
        file = request.files['pimg']
        # img = request.files['pimg']

        # Check if the user selected a file
        if file.filename == '':
            flash('Please select file')
            return redirect('main')
        
        # Check if the file has the allowed extension
        if file and allowed_file(file.filename):
            if 'species'not in request.form:
                flash('Plases select plant species !!')
                return redirect('main')
            else:
                # save img
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                current_date = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_filename = f"{current_date}.{file_ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                file.save(filepath)
                
                # prediction
                species = int(request.form['species'])
                model = load_dl_models(species)
                df_features = feature_extraction(filepath, model)
                selected_df_features = feature_selection(df_features, species)
                sorted_prob = svm_prediction(selected_df_features, species)
                if int(species) == 1:
                    text_species = "Tomato"
                elif int(species) == 2:
                    text_species = "Sugarcane"
                else: 
                    text_species = "Corn"

                return render_template('result.html', species= text_species, result_prob=  sorted_prob, filepath=f"uploads/{filepath.split('/')[-1]}")
        else:
            flash('Invalid file type. Only PNG, JPG, and JPEG are allowed.')
            return redirect('main')
    else:
        return redirect('main')


@app.route("/main")
def main():
    return render_template('main.html')

@app.route("/result")
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)