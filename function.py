import json
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
import pandas as pd
import joblib

# Load the configuration file
with open('config.json') as f:
    config = json.load(f)


def load_dl_models(species_id):
    """
    Loads a pre-trained deep learning model based on the plant species.
    """
    try:
        species_name = list(config['models'].keys())[species_id - 1]
        model_path = config['models'][species_name]['dl_model']
        base_model = load_model(model_path, compile=False)
        model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)
        return model
    except (FileNotFoundError, IndexError):
        return None


def feature_extraction(img_path, model):
    """
    Extracts features from an image using a pre-trained deep learning model.
    """
    image = tf.keras.utils.load_img(img_path, target_size=(224, 224))
    img_array = tf.keras.utils.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0)
    img_features = model.predict(img_array)
    df_features = pd.DataFrame(img_features)
    return df_features


def feature_selection(df_features, species_id):
    """
    Selects a subset of features from the extracted features.
    """
    species_name = list(config['models'].keys())[species_id - 1]
    feature_list = config['models'][species_name]['features']
    selected_df_features = pd.DataFrame()
    for i in feature_list:
        selected_df_features[i] = df_features[i]
    return selected_df_features


def svm_prediction(selected_df_features, species_id):
    """
    Predicts the disease of a plant using a pre-trained SVM model.
    """
    species_name = list(config['models'].keys())[species_id - 1]
    svm_model_path = config['models'][species_name]['svm_model']
    labels = config['models'][species_name]['labels']

    svm_model = joblib.load(svm_model_path)
    result_prediction = list(svm_model.predict_proba(selected_df_features)[0])

    prob_result = {}
    for i, v in enumerate(result_prediction):
        prob_result[labels[i]] = round(v * 100, 2)

    sorted_prob = dict(sorted(prob_result.items(), key=lambda item: item[1], reverse=True))
    return sorted_prob
