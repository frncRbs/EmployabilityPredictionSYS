from tkinter import Y
import numpy as np
import pandas as pd
import pickle
from pandas import DataFrame
from flask import Flask, request, jsonify, render_template
from sklearn.metrics import accuracy_score

dataset = pd.read_csv("model/Institute-of-Computer-Studies-Graduate-Tracer-Study-2021-2022-Responses(ALTERED).csv")

IT_FEATURES = [
     'Sex',
     'Shiftee',
     'ComProg_1_1st',
     'ComProg_1_2nd',
     'ComProg_2_1st',
     'ComProg_2_2nd',
     'Intro_to_Computing_1st',
     'Intro_to_Computing_2nd',
     'Info_Management_1st',
     'Info_Management_2nd',
     'Operating_System_1st',
     'Operating_System_2nd',
     'Elective_1_1st',
     'Elective_1_2nd',
     'Elective_2_1st',
     'Elective_2_2nd',
     'Elective_3_1st',
     'Elective_3_2nd',
     'Data_Structures_1st',
     'Data_Structures_2nd',
     'Application_Dev_and_Emerging_Tech_1st',
     'Application_Dev_and_Emerging_Tech_2nd',
     'Human_and_Computer_Integration_1st',
     'Human_and_Computer_Integration_2nd',
     'Practicum_Industry_Immersion_1st',
     'Practicum_Industry_Immersion_2nd',
     'Integrative_Programming_and_Tech_1st',
     'Integrative_Programming_and_Tech_2nd',
     'System_Integration_and_Architecture_1st',
     'System_Integration_and_Architecture_2nd',
     'Information_Assurance_and_Security_1_1st',
     'Information_Assurance_and_Security_1_2nd',
     'Information_Assurance_and_Security_2_1st',
     'Information_Assurance_and_Security_2_2nd',
     'Software_Engineering_1st',
     'Software_Engineering_2nd',
     'Networking_1_1st',
     'Networking_1_2nd',
     'Networking_2_1st',
     'Networking_2_2nd',
     'WebProg_1st',
     'WebProg_2nd'
]
CS_FEATURES = [
     'Sex',
     'Shiftee',
     'ComProg_1_1st',
     'ComProg_1_2nd',
     'ComProg_2_1st',
     'ComProg_2_2nd',
     'Intro_to_Computing_1st',
     'Intro_to_Computing_2nd',
     'Info_Management_1st',
     'Info_Management_2nd',
     'Operating_System_1st',
     'Operating_System_2nd',
     'Elective_1_1st',
     'Elective_1_2nd',
     'Elective_2_1st',
     'Elective_2_2nd',
     'Elective_3_1st',
     'Elective_3_2nd',
     'Data_Structures_1st',
     'Data_Structures_2nd',
     'Application_Dev_and_Emerging_Tech_1st',
     'Application_Dev_and_Emerging_Tech_2nd',
     'Human_and_Computer_Integration_1st',
     'Human_and_Computer_Integration_2nd',
     'Practicum_Industry_Immersion_1st',
     'Practicum_Industry_Immersion_2nd',
     'Digital_Design_1st',
     'Digital_Design_2nd',
     'Architecture_and_Organization_1st',
     'Architecture_and_Organization_2nd',
     'Programming_Languages_1st',
     'Programming_Languages_2nd',
     'Modelling_and_Simulation_1st',
     'Modelling_and_Simulation_2nd',
     'Information_Assurance_and_Security_1st',
     'Information_Assurance_and_Security_1_2nd',
     'Software_Engineering_1_1st',
     'Software_Engineering_1_2nd',
     'Software_Engineering_2_1st',
     'Software_Engineering_2_2nd',
     'Network_Management_1st',
     'Network_Management_2nd',
     'Advance_Database_1st',
     'Advance_Database_2nd',
     'WebProg_1st',
     'WebProg_2nd'
]

TARGET = 'Suggested_job_role'

Cat_Y = dataset[TARGET]
X_IT = dataset[IT_FEATURES]
X_CS = dataset[CS_FEATURES]

X_IT = X_IT.replace(np.nan, 0)
X_CS = X_CS.replace(np.nan, 0)
percent = "%"
# Create flask app
flask_app = Flask(__name__)
model_IT = pickle.load(open("ProjectModel_IT.pkl", "rb"))
model_CS = pickle.load(open("ProjectModel_CS.pkl", "rb"))
model_CS_1 = pickle.load(open("ProjectModel_CS_1.pkl", "rb"))
model_IT_1 = pickle.load(open("ProjectModel_IT_1.pkl", "rb"))
model_IT_2 = pickle.load(open("ProjectModel_IT_2.pkl", "rb"))
model_CS_2 = pickle.load(open("ProjectModel_CS_2.pkl", "rb"))
model_IT_3 = pickle.load(open("ProjectModel_IT_3.pkl", "rb"))
model_CS_3 = pickle.load(open("ProjectModel_CS_3.pkl", "rb"))


@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/CSinputs")
def CS_view():
    return render_template("CSinputs.html")

@flask_app.route("/predictIT")
def IT_view():
    return render_template("predictIT.html")


@flask_app.route("/predict_IT", methods = ["POST"])
def predict_IT():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    new_Xdata_IT = X_IT.sample(1)
    new_Ydata_IT = Cat_Y[new_Xdata_IT.index.values]
    prediction = model_IT.predict(features)
    prediction1 = model_IT_1.predict(features)
    prediction2 = model_IT_2.predict(features)
    prediction3 = model_IT_3.predict(features)
    aScore = accuracy_score(new_Ydata_IT, prediction)
    aScore1 = accuracy_score(new_Ydata_IT, prediction1)
    aScore2 = accuracy_score(new_Ydata_IT, prediction2)
    aScore3 = accuracy_score(new_Ydata_IT, prediction3)
    return render_template("predictIT.html", prediction_text = "" if aScore == 00 else "Your 1st Job is {}{} ".format(prediction, " : {}{}".format(int(aScore), "00%")), prediction_text1 = "" if prediction == prediction1 or prediction1 == prediction2 or prediction1 == prediction3 else "{}{}".format(prediction1, " : {}".format("40%")), prediction_text2 = "" if prediction == prediction2 or prediction2 == prediction or prediction2 == prediction1 or prediction2 == prediction3 else "{}{}".format(prediction2, " : {}".format("60%")), prediction_text3 = "" if prediction == prediction3 or prediction3 == prediction or prediction3 == prediction1 or prediction3 == prediction2 else "{}{}".format(prediction3, " : {}".format("80%")), course_suggestion = "Suggest" if aScore == 00 and aScore1 == 00 and aScore2 == 00 and aScore3 == 00 or prediction1 == "Administrative Assistant" or prediction2 == "Administrative Assistant" or prediction3 == "Administrative Assistant" else "") 

@flask_app.route("/predict_CS", methods = ["POST"])
def predict_CS():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    new_Xdata_CS = X_CS.sample(1)
    new_Ydata_CS = Cat_Y[new_Xdata_CS.index.values]
    prediction = model_CS.predict(features)
    aScore = accuracy_score(new_Ydata_CS, prediction)
    return render_template("predictCS.html", prediction_text = "{}{}".format(prediction, " = {}".format(aScore, percent)) if prediction == "Software Engineer / Programmer" or prediction == "Academician" or prediction == "Technical Support Specialist" else "Sad to say your first job is not related to IT/CS.") 

if __name__ == "__main__":
    flask_app.run(debug=True)