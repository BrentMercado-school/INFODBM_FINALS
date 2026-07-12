import os
import uuid

from flask import Flask, render_template, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from db import get_connection

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
app = Flask (__name__)
app.secret_key = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"

@app.route("/")
def open_register_page():
    return render_template("register.html")

@app.route("/api/auth/register", methods=["POST"])
def register_user():
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'])

    messages = {
        "NO USERNAME": ("Please enter a username.", 400),
        "NO PASSWORD": ("Please enter a password.", 400),
        "USERNAME ALREADY TAKEN": ("Username already taken.", 400),
    }

    try:
        cursor.execute("EXEC uspRegisterUser @username = ?, @password = ?",
                       (data['username'], hashed_password))

        result = cursor.fetchone()[0]
        if result != "SUCCESS":
            text, code = messages.get(result, ("Something went wrong.", 400))
            return jsonify({"error": text}), code
        conn.commit()
        return jsonify({"message": "Registered successfully."}), 201
    except Exception as e:
        conn.rollback()
        print("REGISTER ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/auth/login", methods=["POST"])
def login_user():
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()

    password = data['password']
    username = data['username']

    try:
        cursor.execute("EXEC uspLoginUser @username = ?", username)
        result = cursor.fetchone()

        if result is None:
            return jsonify({"error": "Invalid username or password."}), 400

        if not result[6]:
            return jsonify({"error": "This account is deactivated."}), 400

        if check_password_hash(result[2], password):
            session["username"] = result[1]
            session["user_id"] = result[0]
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid username or password."}), 400
    except Exception as e:
        conn.rollback()
        print("LOGIN ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/home")
def open_home_page():
    return render_template("home.html")

@app.route("/api/logout", methods=["POST"])
def logout_user():
    session.clear()
    return jsonify({"message": "Logout successful."}), 200

@app.route("/api/items/add", methods=["POST"])
def add_item():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401

    conn = get_connection()
    cursor = conn.cursor()

    data = request.form
    image = request.files.get("image")

    messages = {
        "NO NAME": ("Please enter an item name.", 400),
        "NO CATEGORY": ("Please select a category.", 400),
        "NO CONDITION": ("Please state item condition.", 400),
    }

    try:
        image_url = None
        if image and image.filename and allowed_file(image.filename):
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            image_url = f"/static/uploads/{filename}"

        cursor.execute(
            "EXEC uspAddItem @name = ?, @category = ?, @condition = ?, "
            "@description = ?, @note = ?, @owner = ?, @image = ?, @securityDeposit = ?",
            data['item_name'], data['category'], data['condition'], data['description'],
            data['note'], session["user_id"], image_url, data['security_deposit'] or 0
        )

        result  = cursor.fetchone()[0]

        if result in messages:
            text, code = messages[result]
            return jsonify({"error": text}), code

        conn.commit()
        return jsonify({"message": "Item added successfully."}), 200

    except Exception as e:
        conn.rollback()
        print("ADD ITEM ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/categories", methods=["GET"])
def load_categories():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    conn = get_connection()
    cursor = conn.cursor()
    categories = []

    try:
        cursor.execute("EXEC uspLoadCategories")
        rows = cursor.fetchall()
        for row in rows:
            categories.append({
                "id": row[0],
                "name": row[1],
            })
        return jsonify(categories)
    except Exception as e:
        print("LOAD CATEGORIES ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/items/community_items", methods=["GET"])
def load_community_items():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401

    conn = get_connection()
    cursor = conn.cursor()
    items = []

    try:
        cursor.execute("EXEC uspLoadCommunityItems @user_id = ?", session["user_id"])
        rows = cursor.fetchall()

        for row in rows:
            items.append({
                "id": row[0],
                "image": row[1],
                "name": row[2],
                "category": row[3],
                "condition": row[4],
                "owner": row[5],
                "security_deposit": row[6],
                "status": row[7],
            })
        return jsonify(items)
    except Exception as e:
        print("LOAD COMMUNITY ITEMS ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()
if __name__ == '__main__':
   app.run(debug=True)