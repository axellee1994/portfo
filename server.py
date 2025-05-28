import os
from flask import Flask, render_template, send_from_directory, request, redirect
import csv

app = Flask(__name__)
print(__name__)

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open('database.txt', mode="a") as database:
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{first_name}, {last_name}, {email}, {subject}, {message}\n')

def write_to_csv(data):
    file_exists = os.path.isfile('database.csv')

    with open('database.csv', mode='a', newline='') as csvfile:
        fieldnames = ['first_name', 'last_name', 'email', 'subject', 'message']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        subject = data['subject']
        message = data['message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        
        writer.writerow({'first_name': first_name,
                         'last_name': last_name,
                         'email': email,
                         'subject': subject,
                         'message': message})

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_file(data)
            write_to_csv(data)
            print(data)
            return render_template('thankyou.html',
                                first_name=data['first_name'],
                                last_name=data['last_name'])
        except:
            "Unable to save to database!"
    else:
        return 'Form submission failed!'



# # Explicit favicon route to handle both /favicon.ico and /static/favicon.ico
# @app.route("/favicon.ico")
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

# # Additional route to ensure /static/favicon.ico works if Flask's default handler fails
# @app.route("/static/favicon.ico")
# def static_favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Debug route to check file paths
@app.route("/debug/paths")
def debug_paths():
    
    static_path = os.path.join(app.root_path, 'static')
    favicon_path = os.path.join(static_path, 'favicon.ico')
    return f"""
    <pre>
    App root path: {app.root_path}
    Static folder path: {static_path}
    Favicon path: {favicon_path}
    Favicon exists: {os.path.exists(favicon_path)}
    Static folder contents: {os.listdir(static_path) if os.path.exists(static_path) else 'Directory not found'}
    </pre>
    """

if __name__ == "__main__":
        app.run(debug=True, host='127.0.0.1', port=5000)