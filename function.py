# import module
import io
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model, Model
import pathlib
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import joblib


def load_dl_models(species):
    if (species == 1) :
        print('tomato')
        base_model = load_model('static/dl-models/tomato/resnet34.h5', compile=False)
    elif (species == 2) :
        print('sugarcane')
        base_model = load_model('static/dl-models/sugarcane/resnet34.h5', compile=False)
    else:
        print('corn')
        base_model = load_model('static/dl-models/corn/efficientNetB4.h5', compile=False)

    # base_model.summary()

    # cut prediction layer
    model = base_model
    x = model.layers[-2].output
    model = Model(inputs = base_model.input, outputs = x)
    # model.summary()

    return model

def feature_extraction(img_path, model) :
    # prepare image
    # image_file = io.BytesIO(img.read())
    image = tf.keras.utils.load_img(img_path, target_size=(224, 224))
    img_array = tf.keras.utils.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0)

    # feature extraction
    img_features= model.predict(img_array)

    # create pandas
    df_features = pd.DataFrame(img_features)
    # df_features.columns = df_features.iloc[0]

    return df_features

def feature_selection(df_features, species):
    if (int(species) == 1):
        feature_list = ['14', '26', '27', '32', '35', '40', '42', '49', '60', '66', '71', '75', '82', '86',
                        '89', '94', '97', '106', '111', '113', '122', '123', '124', '126', '129', '133',
                        '141', '157', '171', '174', '180', '191', '210', '211', '220', '224', '230', '233',
                        '242', '243', '252', '261', '278', '281', '287', '289', '294', '300', '304', '320',
                        '333', '337', '340', '341', '352', '356', '371', '382', '383', '390', '397', '401',
                        '402', '409', '415', '421', '431', '441', '443', '448', '462', '469', '479', '504',
                        '505', '509']
    elif (int(species) == 2):
        feature_list = ['4', '7', '11', '23', '33', '42', '45', '55', '59', '64', '66', '67', '71', '82', '86',
                        '88', '91', '95', '98', '104', '120', '124', '127', '132', '134', '138', '156', '162',
                        '167', '172', '187', '196', '203', '206', '207', '211', '214', '217', '218', '220',
                        '225', '236', '237', '244', '246', '249', '252', '253', '256', '270', '284', '288',
                        '292', '296', '306', '313', '315', '319', '334', '343', '344', '348', '352', '354',
                        '355', '370', '376', '381', '384', '401', '403', '404', '405', '413', '414', '415',
                        '416', '417', '421', '438', '441', '444', '445', '452', '453', '455', '456', '460',
                        '468', '470', '481', '487', '489', '492', '496', '497']

    else:
        feature_list = ['2', '13', '22', '23', '28', '36', '83', '89', '91', '105', '114', '116', '135', '144',
                        '160', '162', '169', '178', '218', '220', '228', '243', '246', '254', '271', '279',
                        '307', '321', '350', '358', '360', '363', '364', '387', '388', '429', '482', '492',
                        '494', '495', '516', '542', '543', '547', '559', '563', '579', '582', '603', '612',
                        '619', '676', '682', '684', '689', '699', '716', '727', '734', '738', '752', '763',
                        '809', '814', '817', '832', '844', '883', '893', '903', '904', '912', '930', '965',
                        '979', '996', '1022', '1047', '1054', '1056', '1071', '1076', '1085', '1092',
                        '1168', '1181', '1184', '1192', '1202', '1249', '1250', '1267', '1285', '1297',
                        '1306', '1309', '1345', '1351', '1365', '1366', '1389', '1417', '1444', '1447',
                        '1460', '1489', '1491', '1525', '1545', '1575', '1596', '1616', '1637', '1656',
                        '1665', '1667', '1670', '1693', '1698', '1704', '1710', '1760', '1766']

         
    selected_df_features = pd.DataFrame()
    # print(df_features)
    # print("bbbbbbbb", df_features[1])
    for i in feature_list:
        selected_df_features[int(i)] = df_features[int(i)]  

    return selected_df_features

def svm_prediction(selected_df_features, species):

    tomato_labels = ['Healthy', 'Early blight', 'Bacterial spot', 'Late blight', 'Leaf Mold', 'Septoria leaf spot', 'Spider mites', 'Target Spot', 'Mosaic virus', 'Yellow leaf curl virus']
    sugarcane_labels = ['Healthy', 'Mosaic', 'Red rot', 'Rust', 'Yellow']
    corn_labels = ['Healthy', 'Common rust', 'Cercospora leaf spot', 'Northern leaf blight']
    # print("aaaaaaaa", selected_df_features.shape)
    # load svm model
    if (int(species == 1)):
        svm_model = joblib.load('static/ml-models/tomato/svm-c12d2.joblib')
        result_prediction = list(svm_model.predict_proba(selected_df_features)[0])
        prob_result = {}
        for i, v in enumerate(result_prediction):
            prob_result[tomato_labels[i]] = round(v*100, 2)

    elif (int(species == 2)):
        svm_model = joblib.load('static/ml-models/sugarcane/svm-c9d3.joblib')
        result_prediction = list(svm_model.predict_proba(selected_df_features)[0])
        prob_result = {}
        for i, v in enumerate(result_prediction):
            prob_result[sugarcane_labels[i]] = round(v*100, 2)

    else:
        svm_model = joblib.load('static/ml-models/corn/svm-c27d3.joblib')
        result_prediction = list(svm_model.predict_proba(selected_df_features)[0])
        prob_result = {}
        for i, v in enumerate(result_prediction):
            prob_result[corn_labels[i]] = round(v*100, 2)
    
        # prob_result[i]
        # print("Class ", i, " -->Prob: ", round(v*100, 2))
    sorted_prob = dict(sorted(prob_result.items(), key=lambda item: item[1], reverse=True))


    return sorted_prob
