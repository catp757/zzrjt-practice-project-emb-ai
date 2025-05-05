''' Executing this function initiates the application of sentiment
    analysis to be executed over the Flask channel and deployed on
    localhost:5000.
'''
import json
import requests
from flask import Flask, render_template, request
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

#Initiate the flask app : TODO
app = Flask("Sentiment Analyzer")

@app.route("/sentimentAnalyzer")
def sent_analyzer():
    ''' This code receives the text from the HTML interface and
        runs sentiment analysis over it using sentiment_analysis()
        function. The output returned shows the label and its confidence
        score for the provided text.
    '''
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    # Check if text was entered
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "Please enter text to analyze."

    try:
        # Pass the text to the sentiment_analyzer function and store the response
        response = sentiment_analyzer(text_to_analyze)

        # Extract the label and score from the response
        label = response['label']
        score = response['score']

        # Check if the label is None, indicating an error or invalid input
        if not label:
            return "Invalid input! Try again."

        # Return a formatted string with the sentiment label and score
        formatted_label = label.split('_')[1] if '_' in label else label
        return f"The given text has been identified as {formatted_label} with a score of {score}."

    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        # Catch any unexpected errors and return a user-friendly message
        return f"An error occurred during sentiment analysis: {str(e)}"

@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template('index.html')

if __name__ == "__main__":
    #This functions executes the flask app and deploys it on localhost:5000
    app.run(host="0.0.0.0", port=5000)
