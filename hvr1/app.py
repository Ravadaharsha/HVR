from flask import Flask, render_template, request, jsonify
import faiss
import numpy as np
import pandas as pd
import re
import requests
from sentence_transformers import SentenceTransformer
import mysql.connector
Q=""

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/index")
def index():
    query_type = request.args.get("type", "last_year")  # Default to last_year if no type provided
    return render_template("index.html", type=query_type)

@app.route("/college_query")
def college_query():
    query_type = request.args.get("type", "last_year")
    return render_template("college_query.html", type=query_type)

# MySQL Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Change if necessary
        password="h@rsha1545658",  # Update with your actual MySQL password
        database="JEE"
    )

# Home Page
# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/get_branches', methods=['GET'])
def get_branches():
    try:
        # Get parameters from request
        college_name = request.args.get('college')
        seat_type = request.args.get('seat_type')
        quota = request.args.get('quota')
        gender = request.args.get('gender')
        category_rank = request.args.get('category_rank')

        query_type = request.args.get("type", "last_year")

        print("🔹 Incoming Request Params:")
        print(f"College: {college_name}, Seat Type: {seat_type}, Quota: {quota}, Gender: {gender}, Rank: {category_rank}")
        # Ensure category_rank is an integer
        category_rank = int(category_rank)

        table_name = "jee_cutoff" if query_type == "last_year" else "jee_cutoff_predicted"
        print(f"Table name: {table_name}")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Correct query using exact column names
        query = f"""
            SELECT academic_program_name 
            FROM {table_name}
            WHERE college_name = %s 
            AND seat_type = %s 
            AND quota = %s 
            AND gender = %s 
            AND closing_rank >= %s
            ORDER BY closing_rank ASC
        """
        cursor.execute(query, (college_name, seat_type, quota, gender, category_rank))
        results = cursor.fetchall()

        # Print results to console for debugging
        print("🔹 MySQL Query Results:", results)

        cursor.close()
        conn.close()

        return jsonify(results)
    
    except Exception as e:
        print("❌ Error:", str(e))  # Print error in console
        return jsonify({"error": str(e)}), 500

# API to get college name suggestions
@app.route('/getting_colleges')
def getting_colleges():
    try:
        search_query = request.args.get('query', '')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT DISTINCT college_name FROM jee_cutoff WHERE college_name LIKE %s LIMIT 10"
        cursor.execute(query, (f"%{search_query}%",))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()

        return jsonify([row["college_name"] for row in results])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# # College Query Page
# @app.route('/college_query')
# def college_query():
#     return render_template('college_query.html')

@app.route('/branch_query')
def branch_query():
    query_type = request.args.get("type", "last_year")
    return render_template("branch_query.html", type=query_type)

@app.route('/get_colleges_by_branch', methods=['GET'])
def get_colleges_by_branch():
    try:
        branch_name = request.args.get('branch')
        seat_type = request.args.get('seat_type')
        quota = request.args.get('quota')
        gender = request.args.get('gender')
        category_rank = request.args.get('category_rank')
        query_type = request.args.get("type", "last_year")

        table_name = "jee_cutoff" if query_type == "last_year" else "jee_cutoff_predicted"
        print(f"Table name: {table_name}")
        # Validate category_rank
        if category_rank is None or not category_rank.isdigit():
            return jsonify({"error": "Invalid category rank"}), 400
        category_rank = int(category_rank)

        print("Query Parameters:", branch_name, seat_type, quota, gender, category_rank)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = f"""
        SELECT college_name, MIN(closing_rank) AS min_closing_rank FROM {table_name} 
        WHERE TRIM(academic_program_name) = TRIM(%s) AND seat_type = %s 
        AND quota = %s AND gender = %s AND COALESCE(closing_rank, 0) >= %s
        GROUP BY college_name
        ORDER BY min_closing_rank ASC
        """
        cursor.execute(query, (branch_name, seat_type, quota, gender, category_rank))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        if not results:
            return jsonify({"message": "No eligible colleges found"}), 404

        return jsonify(results)
    
    except Exception as e:
        print("Error:", str(e))  # Debug the actual issue
        return jsonify({"error": str(e)}), 500


@app.route('/getting_branches', methods=['GET'])
def getting_branches():
    try:
        query = request.args.get('query', '').strip()
        if not query:
            return jsonify([])  # Return empty list if query is empty

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch distinct branch names that match the input query
        cursor.execute(
            "SELECT DISTINCT academic_program_name FROM jee_cutoff WHERE academic_program_name LIKE %s LIMIT 10",
            (query + "%",)
        )
        branches = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return jsonify(branches)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route('/category_query')
def category_query():
    query_type = request.args.get("type", "last_year")
    return render_template("category_query.html", type=query_type)

@app.route('/get_suggested_colleges', methods=['GET'])
def get_suggested_colleges():
    try:
        quota = request.args.get('quota')
        gender = request.args.get('gender')
        category_rank = request.args.get('category_rank')
        seat_type= request.args.get('seat_type')
        query_type = request.args.get("type", "last_year")

        table_name = "jee_cutoff" if query_type == "last_year" else "jee_cutoff_predicted"
        print(f"Table name: {table_name}")
        # Validate category_rank
        if category_rank is None or not category_rank.isdigit():
            return jsonify({"error": "Invalid category rank"}), 400
        category_rank = int(category_rank)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        print("harsha..........")
        print(quota)
        print(gender)
        print(category_rank)
        query = f"""
        SELECT college_name, academic_program_name,seat_type,closing_rank, quota, gender
        FROM {table_name} 
        WHERE quota = %s 
        AND seat_type = %s
        AND gender = %s 
        AND closing_rank >= %s 
        ORDER BY closing_rank ASC 
        LIMIT 10;
        """
        
        cursor.execute(query, (quota,seat_type, gender, category_rank))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        print(results)

        if not results:
            return jsonify({"message": "No eligible colleges found"}), 404
        return jsonify(results)
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500






















# Load the sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
 
# Define the Gemini API key
api_key = "AIzaSyBkGPBmqWGU8zrKg01NiJK63XYTww7efp4"  # Replace with your actual API key
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
headers = {"Content-Type": "application/json"}
 
# Sample college data (Replace with actual dataset)
data = pd.read_csv('newcollegedata.csv')
# print(data['collegename'])
with open("random3.txt", "r", encoding="utf-8", errors="ignore") as file:
    data1 = file.read()
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
    global Q
    top_rows = retrieve_college_info(user_query)
    top_college = top_rows.iloc[0]
    college_info = "\n".join([f"{col}: {top_college[col]}" for col in top_college.index])
 
    prompt = f"""
    You are an intelligent college admission assistant.

    User Query:
    {user_query}

    Use the following retrieved context to answer the user's query:
    {college_info}

    If you cannot answer from the above, refer to this additional data:
    {data1}

    If relevant information is not available in either, then use your own knowledge to give the best possible answer Don't try to explain that information is not available generate answer what you know.

    Important Instructions:
    - Provide the answer in a clear and structured format in 10-12 lines (use bullet points, tables, or steps).
    - Keep the response concise and focused on the user’s question.
    - Do not include irrelevant details.
    - Never say “as an AI language model...”

    Respond:
    """


    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=payload, headers=headers)
    temp=response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")
    plain_text = re.sub(r'(\*\*|\*|__|_)', '', temp)
    Q=Q+plain_text
    # print(Q)
    if response.status_code == 200:
        return plain_text
    else:
        return "Error fetching response from Gemini API."
    
@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_query = data.get('user_query', '')
    print(user_query)
    response = query_gemini(user_query)
    print(response)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
