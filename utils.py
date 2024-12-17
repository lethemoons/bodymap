import numpy as np
import pandas as pd

def preprocess_input(data):
    # Konversi jenis kelamin ke numerik
    data["Sex"] = 1 if data["Sex"].lower() == "male" else 0
    if "Sex" not in data or data["Sex"] is None:
        raise ValueError("Sex is required")


    # Hitung BMI
    data["BMI"] = data["Weight"] / (data["Height"] ** 2)

    # Hitung fitur tambahan
    data["y_sr1"] = abs(abs(data["Neck"]) - ((data["Abdomen"] - np.exp(data["Height"])) / 1.1648)) - ((data["Wrist"] * np.sin(data["Sex"])) - (-1.7683))
    data["y_sr2"] = ((data["BMI"] - (np.sin(data["Sex"]) * (data["Hip"] - (data["Abdomen"] / 0.95054))) * np.cos(data["Sex"] / data["Height"])) - (np.sin(data["Wrist"]) + data["Sex"]))

    # Konversi ke DataFrame dengan urutan yang benar
    feature_order = ['Sex', 'Age', 'Weight', 'Height', 'Neck', 'Chest', 'Abdomen', 'Hip', 
                     'Thigh', 'Knee', 'Wrist', 'BMI', 'y_sr1', 'y_sr2']
    data_frame = pd.DataFrame([data])[feature_order]
    
    return data_frame.values[0]


# Fungsi untuk menentukan kategori berdasarkan bodyfat_percentage dan gender
def get_category_by_bodyfat_and_gender(bodyfat_percentage, gender):
    if gender == '1':
        if bodyfat_percentage <= 5:
            return "essential_fat"
        elif bodyfat_percentage <= 13:
            return "athletes"
        elif bodyfat_percentage <= 17:
            return "fitness_enthusiasts"
        elif bodyfat_percentage <= 24:
            return "healthy_average"
        else:
            return "obese"
    else:  # Female
        if bodyfat_percentage <= 13:
            return "essential_fat"
        elif bodyfat_percentage <= 20:
            return "athletes"
        elif bodyfat_percentage <= 24:
            return "fitness_enthusiasts"
        elif bodyfat_percentage <= 31:
            return "healthy_average"
        else:
            return "obese"
