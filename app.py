from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///medicine.db"
db = SQLAlchemy(app)
class Medicine(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    medicine = db.Column(db.String(100))
    time = db.Column(db.String(20))
    
medicine = []
@app.route("/", methods = ["GET","POST"])
def home():
    if request.method == "POST":
        medicine = request.form["medicine"]
        time = request.form["time"]
        new_medicine = Medicine(medicine = medicine, time = time)
        db.session.add(new_medicine)
        db.session.commit()
        return redirect("/")
    medicine_list = ""
    all_medicine = Medicine.query.all()
    current_time = datetime.now().strftime("%H:%M")
    reminder = ""
    for m in all_medicine:
        if m.time == current_time:
            reminder += f"<h3>🔔 Time to take {m.medicine}</h3>"
        status = "medicine-card"
        medicine_list += f"""<div class = '{status}'>
                             <p><strong>{m.medicine}</strong> - {m.time}</p>
                             <a href = '/edit/{m.id}'>Edit</a> |
                             <a href = '/delete/{m.id}'>Delete</a> 
                             </div>"""
        
    return f"""<link rel = "stylesheet" href = "/static/style.css">
               {reminder}
              <h1>💊 Medicine Reminder App</h1>
              <p>Built with Python, Flask, SQLite and SQLAlchemy</p>
              <form method = "POST">
              <label>Medicine Name:</label><br>
              <input type = "text" name = "medicine"><br><br>
              <label>Time</label>
 
            <input type = "time" name = "time"><br><br>
              <button type = "submit">Add Medicine</button>
             <h3>All Medicines</h3>
            {medicine_list}
              </form>"""
@app.route("/delete/<int:id>")
def delete(id):
    medicine = Medicine.query.get(id)
    if medicine:
        db.session.delete(medicine)
        db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods = ["GET", "POST"])
def edit(id):
    medicine = Medicine.query.get(id)
    if request.method == "POST":
        medicine.medicine = request.form["medicine"]
        medicine.time = request.form["time"]

        db.session.commit()
        return redirect("/")
    return f"""<link rel = "stylesheet" href = "/static/style.css">
               <h1>Edit Medicine</h1>
               <form method = "POST">
                    <label>Medicine Name</label><br>
                    <input type = "text" name = "medicine" value = "{medicine.medicine}"><br><br>
                    <label>Time</label><br>
                    <input type = "time" name = "time" value = "{medicine.time}"><br><br>
                    <button type = "submit">Update Medicine</button>
                    </form>
                    """

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)