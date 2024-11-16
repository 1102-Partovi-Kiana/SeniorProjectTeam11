from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder='static')

# Route for the homepage
@app.route('/')
def RenderHomepage():
    return render_template('homepage.html')

# Route for other homepage
@app.route('/home')
def RenderOtherHomepage():
    return render_template('home.html')

@app.route('/robotic-environment')
def RenderRoboticEnvironment():
    return render_template('robotic_environment.html')

@app.route('/environments')
def RenderEnvironmentList():
    environments = [
        # Example list of environment data
        {
            'id': 1,
            'name': 'FetchPickAndPlace-v1',
            'brief_description': 'Move the box to the floating goal position.',
            'preview_filename': 'fetchpickandplace.mp4'
        },
        # Add more environments as needed
    ]
    return render_template('environments-landing.html', environments=environments)

@app.route('/environment/<int:environment_id>')
def RenderEnvironment(environment_id):
    # Example logic to find the environment by id
    environments = [
        {
            'id': 1,
            'name': 'FetchPickAndPlace-v1',
            'brief_description': 'Move the box to the floating goal position.',
            'preview_filename': 'fetchpickandplace.mp4'
        },
        # Add more environments as needed
    ]
    
    # Find the environment with the given ID
    environment = next((env for env in environments if env['id'] == environment_id), None)
    
    if environment is None:
        return "Environment not found", 404

    return render_template('environment_detail.html', environment=environment)

@app.route('/signup', methods=['GET', 'POST'])
def RenderSignup():
    if request.method == 'POST':
        # Handle sign-up logic here, e.g., validate inputs and create the account
        first_name = request.form.get('inputFirstName')
        last_name = request.form.get('inputLastName')
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
        # Perform validation and account creation logic here
        # You would typically save the user information in the database here
        
        return redirect(url_for('RenderHomepage'))  # Redirect after successful sign-up

    # If the request method is GET, return the signup form
    return render_template('account/signup.html')


@app.route('/login')
def RenderLogin():
    if request.method == 'POST':
        first_name = request.form.get('inputFirstName')
        last_name = request.form.get('inputLastName')
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
    return render_template('account/login.html')

@app.route('/courses')
def RenderCourses():
    return render_template('courses.html')

@app.route('/module/introduction')
def module_intro():
    return render_template('module_intro.html') 

@app.route('/module/libraries')
def module_libraries():
    return render_template('module_libraries.html') 


# Debug mode allows for automatic reloading and better error messages
if __name__ == '__main__':
    app.run(debug=True)
