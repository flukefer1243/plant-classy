# Live Demo

https://huggingface.co/spaces/madlabnu1/PlantClassy

# Plant Classy

Plant Classy is a web application that uses machine learning to predict diseases in plants from images of their leaves. It currently supports three types of plants: Tomato, Sugarcane, and Corn.

## Features

*   **Disease Prediction:** Predicts the disease of a plant from an image of its leaf.
*   **Multiple Plant Types:** Supports prediction for Tomato, Sugarcane, and Corn.
*   **Image Upload:** Users can upload their own images of plant leaves to get a prediction.
*   **Sample Images:** A gallery of sample images is provided for users to try out the prediction functionality.
*   **Probability Scores:** The application displays the probability of each possible disease, allowing users to see the confidence of the prediction.

## How to Run the Project

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/plant-classy.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd plant-classy
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Flask application:**
    ```bash
    python app.py
    ```
5.  **Open your web browser and navigate to:**
    ```
    http://127.0.0.1:5000
    ```

## How It Works

The prediction process consists of two main steps:

1.  **Feature Extraction:** A pre-trained deep learning model is used to extract features from the input image. The model is either ResNet34 or EfficientNetB4, depending on the plant species.
2.  **Prediction:** A pre-trained Support Vector Machine (SVM) model is used to classify the disease based on the extracted features. The SVM model predicts the probability of each possible disease.

## User Interface

The web interface is built with Flask and Bootstrap. It consists of the following pages:

*   **Home Page:** The landing page of the application.
*   **Main Page:** The page where users can upload an image or select a sample image for prediction.
*   **Result Page:** The page that displays the prediction results.
*   **About Us Page:** A page with information about the project and its creators.

## Models

The following models are used in this project:

| Plant Species | Model Type      | Model Name      | Model Path                                       |
| ------------- | --------------- | --------------- | ------------------------------------------------ |
| Tomato        | Deep Learning   | ResNet34        | `static/dl-models/tomato/resnet34.h5`            |
| Tomato        | Machine Learning | SVM             | `static/ml-models/tomato/svm-c12d2.joblib`       |
| Sugarcane     | Deep Learning   | ResNet34        | `static/dl-models/sugarcane/resnet34.h5`         |
| Sugarcane     | Machine Learning | SVM             | `static/ml-models/sugarcane/svm-c9d3.joblib`     |
| Corn          | Deep Learning   | EfficientNetB4  | `static/dl-models/corn/efficientNetB4.h5`        |
| Corn          | Machine Learning | SVM             | `static/ml-models/corn/svm-c27d3.joblib`         |

## Project Structure

```
├── app.py                  # Flask application
├── function.py             # Core functions for prediction
├── requirements.txt        # Project dependencies
├── static                  # Static assets (CSS, JS, images, models)
│   ├── bootstrap-5.3.3-dist
│   ├── dl-models           # Deep learning models
│   ├── font
│   ├── img
│   ├── ml-models           # Machine learning models
│   └── uploads
└── templates               # HTML templates
    ├── aboutUs.html
    ├── header.html
    ├── index.html
    ├── layout.html
    ├── main.html
    └── result.html
```

## Contributing

Contributions are welcome! If you would like to contribute to the project, please follow these guidelines:

### Reporting Bugs

If you find a bug, please open an issue on the GitHub repository. Please include the following information in your bug report:

*   A clear and concise description of the bug.
*   Steps to reproduce the bug.
*   The expected behavior.
*   The actual behavior.
*   Screenshots or screen recordings, if applicable.

### Suggesting Enhancements

If you have an idea for an enhancement, please open an issue on the GitHub repository. Please include the following information in your enhancement suggestion:

*   A clear and concise description of the enhancement.
*   The problem that the enhancement solves.
*   Any alternative solutions or features you have considered.

### Pull Requests

If you would like to submit a pull request, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your changes.
3.  Make your changes and commit them to your branch.
4.  Push your changes to your forked repository.
5.  Open a pull request on the original repository.

Please ensure that your pull request follows these guidelines:

*   Your code should adhere to the coding standards of the project.
*   Your pull request should include a clear and concise description of the changes you have made.
*   Your pull request should be based on the `main` branch of the repository.

## Dependencies

The main dependencies of the project are:

*   Flask
*   TensorFlow
*   scikit-learn
*   Pandas
*   Numpy
*   Pillow
*   Joblib

A complete list of dependencies is available in the `requirements.txt` file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
