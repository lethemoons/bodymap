from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import joblib
import numpy as np
from utils import preprocess_input, get_category_by_bodyfat_and_gender
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Memuat model
model = joblib.load("saved_model/stacked_model.pkl")

# Route halaman utama
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/home")
def home():
    return render_template("index.html")

# Route untuk halaman input data prediksi
@app.route("/check", methods=["GET"])
def check():
    return render_template("check.html")

    
# Route untuk halaman Explore
@app.route("/explore")
def explore():
    return render_template("explore.html")
    
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

# Route untuk menampilkan hasil prediksi
@app.route("/result", methods=["POST"])
def result():
    print(request.form)
    try:
        # Ambil data dari form
        data = {
            "Age": request.form.get("Age"),
            "Weight": request.form.get("Weight"),
            "Height": request.form.get("Height"),
            "Neck": request.form.get("Neck"),
            "Chest": request.form.get("Chest"),
            "Abdomen": request.form.get("Abdomen"),
            "Hip": request.form.get("Hip"),
            "Thigh": request.form.get("Thigh"),
            "Knee": request.form.get("Knee"),
            "Wrist": request.form.get("Wrist"),
            "Sex": request.form.get("Sex")
        }

        # Validasi data input
        for key, value in data.items():
            if value is None or value.strip() == "":
                return f"Error: {key} is required.", 400

        # Konversi data ke tipe yang sesuai
        data = {
            "Age": int(data["Age"]),
            "Weight": float(data["Weight"]),
            "Height": float(data["Height"]),
            "Neck": float(data["Neck"]),
            "Chest": float(data["Chest"]),
            "Abdomen": float(data["Abdomen"]),
            "Hip": float(data["Hip"]),
            "Thigh": float(data["Thigh"]),
            "Knee": float(data["Knee"]),
            "Wrist": float(data["Wrist"]),
            "Sex": data["Sex"].lower()
        }

        # Proses data untuk prediksi
        processed_data = preprocess_input(data)
        bodyfat_prediction = model.predict([processed_data])[0]
        
        # Tentukan kategori berdasarkan bodyfat_percentage dan gender
        category = get_category_by_bodyfat_and_gender(bodyfat_prediction, data["Sex"])
        bodyfat_percentage =round(bodyfat_prediction)

        session['bodyfat_percentage'] = bodyfat_percentage

        # Redirect ke halaman kategori sesuai
        return redirect(url_for(category))
        
    except Exception as e:
        return f"Error processing data: {str(e)}", 500


# Route untuk kategori Essential Fat
@app.route("/essential_fat")
def essential_fat():
    bodyfat_percentage = session.get('bodyfat_percentage', None)
    return render_template("essential_fat.html", bodyfat_percentage=bodyfat_percentage)

# Route untuk kategori Athletes
@app.route("/athletes")
def athletes():
    bodyfat_percentage = session.get('bodyfat_percentage', None)
    return render_template("athletes.html", bodyfat_percentage=bodyfat_percentage)


# Route untuk kategori Fitness Enthusiasts
@app.route("/fitness_enthusiasts")
def fitness_enthusiasts():
    bodyfat_percentage = session.get('bodyfat_percentage', None)
    return render_template("fitness_enthusiasts.html", bodyfat_percentage=bodyfat_percentage)

# Route untuk kategori Healthy Average
@app.route("/healthy_average")
def healthy_average():
    bodyfat_percentage = session.get('bodyfat_percentage', None)
    return render_template("healthy_average.html", bodyfat_percentage=bodyfat_percentage)

# Route untuk kategori Obese
@app.route("/obese")
def obese():
    bodyfat_percentage = session.get('bodyfat_percentage', None)
    return render_template("obese.html", bodyfat_percentage=bodyfat_percentage)



if __name__ == "__main__":
    app.run(debug=True)

