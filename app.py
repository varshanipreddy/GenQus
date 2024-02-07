from flask import Flask, render_template, request, redirect, url_for
from Questgen.main import BoolQGen, QGen, AnswerPredictor
import nltk
import json
import random

app = Flask(__name__)



def add_answer_to_options(question):
    # Add the answer to options at a random index
    options_with_answer = question['options'][:]
    random_index = random.randint(0, len(options_with_answer))
    options_with_answer.insert(random_index, question['answer'])
    
    # Update the options in the question
    question['options'] = options_with_answer

def modify_processed_text(processed_text):
    # Iterate through each question and add answer to options
    for question in processed_text['questions']:
        add_answer_to_options(question)
    
    return processed_text

# Initialize BoolQGen instance
qe = BoolQGen()
qg = QGen()

# Replace this with your actual logic to get site data
def get_site_data():
    # This is a placeholder, replace with your logic to get site data
    return {"id": 1, "name": "Example Site"}  # Replace with your actual data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get selected option from the form
        selected_option = request.form['options']

        # Get text from the submitted form
        input_text = request.form['input_text']

        # Create payload with the entered text
        payload = {"input_text": input_text}
        payload2 = {"input_text": input_text}

        # Call the appropriate function based on the selected option
        if selected_option == 'option1':
            result = qe.predict_boolq(payload)
        elif selected_option == 'option2':
            result = qg.predict_mcq(payload)
        elif selected_option == 'option3':
            result = qg.predict_shortq(payload)
        elif selected_option == 'option4':
            result = qg.paraphrase(payload)
        else:
            # Default to predict_boolq if an invalid option is selected
            result = qe.predict_boolq(payload)

        # Render the result on a new page
        return render_template('result.html', result=result)

    # Render the main page with the form
    return render_template('index.html')

@app.route('/base/<option>', methods=['GET', 'POST'])
def base(option='home'):
    site = get_site_data()  # Call your function to get site data
    # selected = "bool"  # Assuming you have a 'selected' variable defined

    processed_text = ""

    if request.method == 'POST':
        # Get selected option from the form
        selected_option = request.form.get('selected_option')

        # Get text from the submitted form
        input_text = request.form.get('input_text', '')

        # Create payload with the entered text
        payload = {"input_text": input_text}

                # Call the appropriate function based on the selected option
        if selected_option == 'bool':
            result = qe.predict_boolq(payload)

        elif selected_option == 'mcq':
            result_1 = qg.predict_mcq(payload)
            # result_1 = processed_text['Boolean Questions']
            result = modify_processed_text(result_1)
        elif selected_option == 'faq':
            result = qg.predict_shortq(payload)
        elif selected_option == 'para':
            result = qg.paraphrase(payload)
        else:
            # Default to predict_boolq if an invalid option is selected
            result = qe.predict_boolq(payload)

        # Process the input based on the selected option
        processed_text = result



    return render_template('base.html', site=site, selected=option, processed_text=processed_text)



if __name__ == '__main__':
    app.run(debug=True)
