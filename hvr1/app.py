from flask import Flask, render_template, request, jsonify
import mysql.connector

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
        print(" Error:", str(e))  # Print error in console
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


if __name__ == '__main__':
    app.run(debug=True)
