import pickle
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the pickled data
with open('restaurants.pkl', 'rb') as file:
    restaurant_data = pickle.load(file)

with open('similarity.pkl', 'rb') as file:
    similarity_matrix = pickle.load(file)

# Define a function to get restaurant recommendations
def get_recommendations(restaurant_name, top_n=10):
    # Find the index of the given restaurant
    restaurant_index = restaurant_data[restaurant_data['name'] == restaurant_name].index[0]

    # Get cosine similarity scores for the given restaurant
    similarity_scores = list(enumerate(similarity_matrix[restaurant_index]))

    # Sort the restaurants by similarity score
    sorted_restaurants = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get the top N similar restaurants (excluding itself)
    top_recommendations = [restaurant_data.iloc[x[0]] for x in sorted_restaurants[1:top_n+1]]

    return top_recommendations

@app.route('/')
def index():
    return render_template('index.html', restaurant_data=restaurant_data)

@app.route('/recommend', methods=['POST'])
def recommend():
    restaurant_name = request.form['restaurant_name']
    recommendations = get_recommendations(restaurant_name)
    return render_template('index.html', restaurant_name=restaurant_name, recommendations=recommendations, restaurant_data=restaurant_data)

if __name__ == '__main__':
    app.run(debug=True)
