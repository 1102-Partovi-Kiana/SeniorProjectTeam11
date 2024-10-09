from flask import Flask, render_template

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def RenderHomepage():
    return render_template('homepage.html')

@app.route('/robotic-environment')
def RenderRoboticEnvironment():
    return render_template('robotic_environment.html')

# Debug mode allows for automatic reloading and better error messages
if __name__ == '__main__':
    app.run(debug=True)
