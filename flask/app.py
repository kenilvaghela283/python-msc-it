from flask import Flask,render_template,request
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route("/")
def root():
    return "Mahadev Mahadev"

@app.route("/home",methods=["GET","POST"])
def home():
    print(request.method)

    if request.method == "POST":
        name = request.form.get("todo-name")
        date = request.form.get("todo-date")
        status = request.form.get("todo-status")
        print(name,date,status)
        return name
    else:
        # return "Invalid Data"

        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
