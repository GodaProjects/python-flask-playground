from flask import Flask

# First step - init
app =Flask(__name__)

@app.route('/')
def index():
    return "Hello, Goda!"

# Why this condition is written without directly calling app.run is something i am not sure.
if __name__ == "__main__":
    app.run(debug=True)