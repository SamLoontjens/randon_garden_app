from flask import Flask, render_template, request
from random_garden_package.random_garden_generator import random_garden
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])  # Allow both GET and POST requests
def index():
    garden_art = ""
    error_message = ""
    form_data = {
        'seed': '',
        'draw_height': '26',
        'draw_width': '200',
        'weather': ''
    }  # Dictionary to hold form data
    displayed_seed = ''

    if request.method == 'POST':
        form_data['seed'] = request.form.get('seed', '')
        form_data['draw_height'] = request.form.get('draw_height', '26')
        form_data['draw_width'] = request.form.get('draw_width', '200')
        form_data['weather'] = request.form.get('weather', '')
        # Include additional fields as necessary

        try:
            # Extracting and validating inputs
            
            # Generate a random seed if not provided
            if form_data['seed']:
                seed = int(form_data['seed'])
            else:
                seed = random.randint(0, 99999)
            displayed_seed = seed

            # Validate and convert draw_height and draw_width
            draw_height = int(form_data['draw_height'])  
            draw_width = int(form_data['draw_width'])    

            if seed <= 0 or draw_height <= 0 or draw_width <= 0:
                raise ValueError("Draw height and width must be positive integers.")
            #weather = request.form.get('weather', '')

            # You can add more validation logic here if needed

            # Call the ASCII art generation function with validated inputs
            # Assuming your generate_garden function accepts these parameters
            garden_art = random_garden(
                seed = seed, 
                draw_height = draw_height, 
                draw_width = draw_width, 
                weather = form_data['weather']
            )
        except ValueError as e:
            error_message = str(e)
        except Exception as e:
            error_message = "An error occurred: " + str(e)

        # Add other exception types as needed

    # Read ASCII art from file
    with open('ascii-text-art.txt', 'r') as file:
        ascii_art_name = file.read()
    
    # Read banner from file
    with open('banner.txt', 'r') as file:
        banner = file.read()
        
    return render_template('index.html', 
                           garden_art=garden_art, 
                           error_message=error_message, 
                           form_data=form_data, 
                           displayed_seed=displayed_seed,
                           ascii_art_name=ascii_art_name,
                           banner=banner)

if __name__ == '__main__':
    app.run(debug=True)