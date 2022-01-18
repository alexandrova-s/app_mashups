from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/")
def start():
   return render_template('index.html')

@app.route("/action")
def action():
   return "action"

if __name__ == "__main__":
   app.run(port=5005, debug=True)

