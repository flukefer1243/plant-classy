# other
import os
from datetime import datetime
# flask 
from flask import Flask, render_template, request, redirect, flash
# my function for prediction
from function import load_dl_models, feature_extraction, feature_selection, svm_prediction

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', b'_5#y2L"F4Q8z\n\xec]/')

# Set up the upload folder
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create a mapping for species
SPECIES_MAP = {
    1: "Tomato",
    2: "Sugarcane",
    3: "Corn",
}


# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_species_name(species_id):
    return SPECIES_MAP.get(species_id, "Unknown")


def get_prediction(image_path, species_id):
    model = load_dl_models(species_id)
    df_features = feature_extraction(image_path, model)
    selected_df_features = feature_selection(df_features, species_id)
    sorted_prob = svm_prediction(selected_df_features, species_id)
    return sorted_prob


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/aboutUs")
def aboutUs():
    return render_template('aboutUs.html')


@app.route("/predictionSamples", methods=['POST'])
def predictionSamples():
    if request.method == 'POST':
        path_samples = request.form.get('pathSamples')
        species_samples = request.form.get('speciesSamples')

        if not path_samples:
            flash('Please select a sample image.')
            return redirect(request.url)

        if not species_samples or int(species_samples) == 0:
            flash('Please select a plant species.')
            return redirect(request.url)

        species_id = int(species_samples)
        sorted_prob = get_prediction(f"static/{path_samples}", species_id)
        species_name = get_species_name(species_id)

        return render_template(
            'result.html',
            species=species_name,
            result_prob=sorted_prob,
            filepath=path_samples
        )
    return redirect(url_for('main'))


@app.route("/prediction", methods=['POST'])
def prediction():
    if request.method == 'POST':
        if 'pimg' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['pimg']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            if 'species' not in request.form:
                flash('Please select a plant species.')
                return redirect(request.url)

            species_id = int(request.form['species'])
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            current_date = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_filename = f"{current_date}.{file_ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(filepath)

            sorted_prob = get_prediction(filepath, species_id)
            species_name = get_species_name(species_id)

            return render_template(
                'result.html',
                species=species_name,
                result_prob=sorted_prob,
                filepath=f"uploads/{new_filename}"
            )

        flash('Invalid file type. Only PNG, JPG, and JPEG are allowed.')
        return redirect(request.url)
    return redirect(url_for('main'))


@app.route("/main")
def main():
    return render_template('main.html')


@app.route("/result")
def result():
    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)