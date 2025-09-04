from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import csv
import os
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "secret123"
# MongoDB connection
client = MongoClient("mongodb://localhost:27017/") 
db = client["Health"]  
login_collection = db["Login_form"]      
contact_collection = db["Contact_form"]  

# Load Health Tips CSV

def load_health_tips():
    csv_path = os.path.join(os.path.dirname(__file__), "new", "health_tips.csv")
    tips = []
    try:
        with open(csv_path, mode="r", encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tip = (row.get("Tips") or "").strip()
                if tip:
                    tips.append(tip)
    except FileNotFoundError:
        tips = []
    except Exception:
        pass
    return tips

HEALTH_TIPS = load_health_tips()

# Routes

@app.route("/")
def home():
    return render_template("index.html")  

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip().lower()
        password = (request.form.get("password") or "").strip()

        user = login_collection.find_one({"username": username, "password": password})

        if user:
            session["user"] = username
            flash("Successfully logged in", "success")
            return redirect(url_for("about"))
        else:
            flash("Invalid username or password", "error")
            return render_template("index.html")

    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password are required", "error")
            return render_template("signup.html")

        if login_collection.find_one({"username": username}):
            flash("User already exists", "error")
            return render_template("signup.html")

        # Insert into MongoDB
        login_collection.insert_one({"username": username, "password": password})

        session["user"] = username
        flash("Account created successfully", "success")
        return redirect(url_for("about"))

    return render_template("signup.html")

# ✅ ABOUT
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/details")
def details():
    return render_template("details.html", tips=HEALTH_TIPS)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        # Insert into MongoDB
        contact_collection.insert_one({
            "name": name,
            "email": email,
            "phone": phone,
            "message": message
        })

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/api/tips", methods=["GET"])
def api_tips():
    return jsonify({"tips": HEALTH_TIPS})

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have logged out!", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
