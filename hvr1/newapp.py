from flask import Flask, render_template, request
import faiss
import numpy as np
import pandas as pd
import re
import requests
from sentence_transformers import SentenceTransformer
 
app = Flask(__name__)
 
# Load the sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
 
# Define the Gemini API key
api_key = "AIzaSyBkGPBmqWGU8zrKg01NiJK63XYTww7efp4"  # Replace with your actual API key
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
headers = {"Content-Type": "application/json"}
 
# Sample college data (Replace with actual dataset)
data = pd.read_csv('newcollegedata.csv')
df = pd.DataFrame(data)
 
# Combine all columns into a single text representation for embeddings
df['text'] = df.apply(lambda row: f"{row['collegename']} - Tuition: {row['tuitionfees']}, Placement: {row['placement']}, Academics: {row['academic']}, Likes: {row['likes']}, Dislikes: {row['dislikes']}", axis=1)
 
# Generate embeddings
embeddings = model.encode(df['text'].tolist(), convert_to_numpy=True)
 
# Store in FAISS
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
 
# Function to retrieve relevant college data
def retrieve_college_info(query):
    for college in df['collegename']:
        if re.search(college, query, re.IGNORECASE):
            return df[df['collegename'] == college]
 
    query_embedding = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_embedding, k=1)
    return df.iloc[I[0]]
 
# Function to query Gemini API with retrieved college data
def query_gemini(user_query):
    top_rows = retrieve_college_info(user_query)
    top_college = top_rows.iloc[0]
    college_info = "\n".join([f"{col}: {top_college[col]}" for col in top_college.index])
 
    prompt = f"User query: {user_query}\n\nBased on the following college details, answer the query in one line:\n{college_info}"
 
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=payload, headers=headers)
 
    if response.status_code == 200:
        return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")
    else:
        return "Error fetching response from Gemini API."
 
# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')
 
# Route to handle form submission
@app.route('/query', methods=['POST'])
def query():
    user_query = request.form['user_query']
    response = query_gemini(user_query)
    return render_template('index.html', query=user_query, response=response)
 
if __name__ == "__main__":
    app.run(debug=True)
    