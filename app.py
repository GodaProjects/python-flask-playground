from flask import Flask, render_template

# First step - init
app =Flask(__name__)

@app.route('/')
def index():
    # You dont have to mention the templates folder here as the name is predefined name.
    return render_template('index.html')

# Why this condition is written without directly calling app.run is something i am not sure.
if __name__ == "__main__":
    app.run(debug=True)