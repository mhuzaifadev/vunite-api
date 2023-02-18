import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
import os
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api

# Load the data from the Excel file
# Add current directory path


class NLP(Resource):
    def get(self):
        subject = request.args.get('subject')
        question = request.args.get('question')
        if subject == 'None':
            return make_response(
                jsonify(
                    {
                        'message': 'Please enter a valid subject'
                        }), 
                    400)
        elif question == 'None':
            return make_response(
                jsonify(
                    {
                        'message': 'Please enter a valid question'
                        }), 
                    400)
        else:
            if subject == 'sirsyed':
                answer = self.answer(question, subject)
                
                return make_response(
                    jsonify(
                        {
                            'message': answer
                            }), 
                        200)
            elif subject == 'liquat':
                answer = self.answer(question, subject)
                
                return make_response(
                    jsonify(
                        {
                            'message': answer
                            }), 
                        200)
            elif subject == 'quaid':
                answer = self.answer(question, subject)
                
                return make_response(
                    jsonify(
                        {
                            'message': answer
                            }), 
                        200)
            elif subject == 'fatima':
                answer = self.answer(question, subject)
                
                return make_response(
                    jsonify(
                        {
                            'message': answer
                            }), 
                        200)
            else:
                return make_response(
                    jsonify(
                        {
                            'message': 'Please enter a valid subject'
                            }), 
                        400)

    def answer(self, question, subject):
 
        path = os.path.dirname(__file__).replace("\\","/")
        if subject == 'sirsyed':
            filename = 'SirSyedAhmedKhan.csv'
        elif subject == 'liquat':
            filename = 'LiaquatAliKhan.csv'
        elif subject == 'quaid':
            filename = 'QuaideAzam.csv'
        elif subject == 'fatima':
            filename = 'FatimahJinnah.csv'


        data = pd.read_excel(path+"/"+filename)
        # print(data)

        # Preprocess the data
        data['questions'] = data['questions'].apply(lambda x: x.lower())
        data['questions'] = data['questions'].apply(word_tokenize)
        stop_words = set(stopwords.words('english'))
        data['questions'] = data['questions'].apply(lambda x: [item for item in x if item not in stop_words])
        data['questions'] = data['questions'].apply(lambda x: ' '.join(x))

        # Initialize the TF-IDF vectorizer
        vectorizer = TfidfVectorizer()

        # Fit the vectorizer on the data
        vectorizer.fit(data['questions'])

        # Convert the user's input into a vector
        user_input = question.lower()
        user_input = word_tokenize(user_input)
        user_input = [item for item in user_input if item not in stop_words]
        user_input = ' '.join(user_input)
        user_input_vector = vectorizer.transform([user_input])

        # Compute the cosine similarities between the user's input and the questions in the data
        similarities = cosine_similarity(user_input_vector, vectorizer.transform(data['questions']))

        # Find the index of the most similar question
        most_similar_index = np.argmax(similarities)

        # Get the answer corresponding to the most similar question
        answer = data.loc[most_similar_index, 'answers']

        return answer