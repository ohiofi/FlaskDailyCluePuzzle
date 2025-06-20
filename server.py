from flask import Flask, render_template, request
from datetime import datetime
import model

def time_to_int(dateobj):
    #total = int(dateobj.strftime('%S'))........
    # total = int(dateobj.strftime('%M')) * 60
    # total += int(dateobj.strftime('%H')) * 60 * 60
    total = (int(dateobj.strftime('%j')) - 1) * 60 * 60 * 24
    total += (int(dateobj.strftime('%Y')) - 1970) * 60 * 60 * 24 * 365
    return total

app = Flask(__name__)
solution = model.generate_solution(time_to_int(datetime.now()))
hints = 0

@app.route("/", methods=["GET", "POST"])
def index():
    global hints
    if request.method == 'POST':
        clues = "suspects"
        hints = hints + 1
        return render_template("index.html", now=hints, clues=model.generate_hint(solution,hints)["text"])
    return render_template("index.html", now=hints)

  
@app.route("/result", methods=["GET", "POST"])
def result():
  if request.method == "POST":
    userdata = dict(request.form)
    print(userdata)
    if "button1" in userdata:
      return render_template("index.html", clues="yo")
    if "button2" in userdata:
      return render_template("result.html", book=userdata["suspect"][0])
  else:
    return "Sorry, there was an error."
  
def home():
    return "HelloWorld"
  


if __name__ == "__main__":
    app.run()