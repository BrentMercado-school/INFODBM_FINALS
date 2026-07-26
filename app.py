import os
import uuid

from flask import Flask, render_template, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename, redirect

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
        print("LOGIN ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/home")
def open_home_page():
    if session.get("user_id") is None:
        return redirect("/")
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

@app.route("/api/items/latest_items", methods=["GET"])
def load_latest_items():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401

    conn = get_connection()
    cursor = conn.cursor()
    items = []

    try:
        cursor.execute("EXEC uspGetLatestItems @user_id = ?", session["user_id"])
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
        print("LOAD LATEST ITEMS ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/items/<int:id>", methods=["GET"])
def get_item_by_id(id):
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("EXEC uspGetItemByID @item_id = ?", id)
        item = cursor.fetchone()

        if item is None:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({
            "id": item[0],
            "name": item[1],
            "category": item[2],
            "condition": item[3],
            "owner": item[4],
            "image": item[5],
            "security_deposit": item[6],
            "status": item[7],
            "note": item[8],
        })
    except Exception as e:
        print("GET ITEM ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/borrowItem/<int:item_id>", methods=["POST"])
def borrow_item(item_id):
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401

    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()

    messages = {
        "NOT_FOUND": ("Item not found.", 404),
        "OWN_ITEM": ("You cannot borrow your own item.", 400),
        "NOT_AVAILABLE": ("This item is not available for borrowing.", 400),
        "START_IN_PAST": ("Start date cannot be in the past.", 400),
        "INVALID_DATES": ("Return date must be on or after the start date.", 400),
    }

    try:
        cursor.execute(
            "EXEC uspBorrowItem @borrower_id = ?, @item_id = ?, @start = ?, @return = ?",
            session["user_id"], item_id, data["startDate"], data["returnDate"])

        result = cursor.fetchone()[0]
        if result != "SUCCESS":
            text, code = messages.get(result, ("Something went wrong.", 400))
            return jsonify({"error": text}), code

        conn.commit()
        return jsonify({"message": "Borrow request sent."}), 201
    except Exception as e:
        conn.rollback()
        print("BORROW ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 400
    finally:
        conn.close()

@app.route("/api/community_items")
def open_community_items_page():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    return render_template("community_items.html")

@app.route("/api/items/community_items/all", methods=["GET"])
def get_community_items_all():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    conn = get_connection()
    cursor = conn.cursor()
    items = []

    try:
        cursor.execute("EXEC uspGetAllCommunityItems @user_id = ?", session["user_id"])
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
        print("LOAD ALL ITEMS ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/items/community_items/appliance", methods=["GET"])
def get_community_items_appliance():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    conn = get_connection()
    cursor = conn.cursor()
    items = []

    try:
        cursor.execute("EXEC uspGetApplianceCommunityItems @user_id = ?", session["user_id"])
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
        print("LOAD APPLIANCE ITEMS ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/items/community_items/technology", methods=["GET"])
def get_community_items_technology():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    conn = get_connection()
    cursor = conn.cursor()
    items = []

    try:
        cursor.execute("EXEC uspGetTechnologyCommunityItems @user_id = ?", session["user_id"])
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
        print("LOAD TECHNOLOGY ITEMS ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/items/community_items/sports", methods=["GET"])
def get_community_items_sports():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    conn = get_connection()
    cursor = conn.cursor()
    items = []

    try:
        cursor.execute("EXEC uspGetSportsCommunityItems @user_id = ?", session["user_id"])
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
        print("LOAD SPORTS ITEMS ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/items/community_items/search/<string:search>", methods=["GET"])
def get_community_items_search(search):
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    conn = get_connection()
    cursor = conn.cursor()

    items = []

    try:
        cursor.execute("EXEC uspGetSearchItems @search = ?, @user_id = ?", search, session["user_id"])
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
        print("LOAD SEARCH ITEMS ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/request")
def open_request_page():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    return render_template("request.html")

@app.route("/api/borrow_request/all", methods=["GET"])
def get_borrow_request_all():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401

    conn = get_connection()
    cursor = conn.cursor()
    data = []

    try:
        cursor.execute("EXEC uspGetBorrowRequest @user_id = ?", session["user_id"])

        rows = cursor.fetchall()
        for row in rows:
            data.append({
                "borrow_form_id": row[0],
                "item_id": row[1],
                "image": row[2],
                "name": row[3],
                "category": row[4],
                "start_date": row[5],
                "return_date": row[6],
                "security_deposit": row[7],
                "owner": row[8],
            })
        return jsonify(data)
    except Exception as e:
        print("LOAD ALL BORROW REQUEST ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/borrow_request/accept", methods=["PUT"])
def accept_borrow_request():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401

    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()

    messages = {
        "NOT_FOUND": ("Request not found.", 404),
        "NOT_PENDING": ("This request has already been handled.", 400),
        "ITEM_UNAVAILABLE": ("This item is no longer available.", 400),
    }

    try:
        cursor.execute("EXEC uspAcceptBorrowRequest @borrow_id = ?, @item_id = ?",
                       data["borrow_form_id"], data["item_id"])
        result = cursor.fetchone()[0]

        if result != "SUCCESS":
            text, code = messages.get(result, ("Something went wrong.", 400))
            return jsonify({"error": text}), code

        conn.commit()
        return jsonify({"message": "Borrow request accepted."}), 200

    except Exception as e:
        conn.rollback()
        print("ACCEPT ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 400
    finally:
        conn.close()

@app.route("/api/borrow_request/decline", methods=["PUT"])
def decline_borrow_request():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401

    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()

    messages = {
        "NOT_FOUND": ("Request not found.", 404),
        "NOT_PENDING": ("This request has already been handled.", 400),
    }

    try:
        cursor.execute("EXEC uspDeclineBorrowRequest @borrow_id = ?, @owner_id = ?, @decline_reason = ?",
                       data["borrow_form_id"], session["user_id"], data["decline_reason"])
        result = cursor.fetchone()[0]

        if result != "SUCCESS":
            text, code = messages.get(result, ("Something went wrong.", 400))
            return jsonify({"error": text}), code

        conn.commit()
        return jsonify({"message": "Borrow request declined."}), 200

    except Exception as e:
        conn.rollback()
        print("DECLINE ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 400
    finally:
        conn.close()

@app.route("/api/my_borrow_request", methods=["GET"])
def load_my_borrow_request():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401

    conn = get_connection()
    cursor = conn.cursor()
    data = []
    try:
        cursor.execute("EXEC uspGetMyBorrowRequest @user_id = ?", session["user_id"])
        rows = cursor.fetchall()

        for row in rows:
            data.append({
                "borrow_form_id": row[0],
                "image": row[1],
                "name": row[2],
                "category": row[3],
                "condition": row[4],
                "start_date": row[5].strftime("%B %d, %Y"),
                "return_date": row[6].strftime("%B %d, %Y"),
                "security_deposit": row[7],
                "status": row[8],
            })

        return jsonify(data)
    except Exception as e:
        print("MY BORROW REQUEST ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 400
    finally:
        conn.close()

@app.route("/api/my_borrow_request/cancel/<int:id>", methods=["PUT"])
def cancel_borrow_request(id):
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401

    conn = get_connection()
    cursor = conn.cursor()

    messages = {
        "NOT_FOUND": ("Request not found.", 404),
        "NOT_PENDING": ("This request has already been handled.", 400),
    }

    try:
        cursor.execute("EXEC uspCancelBorrowRequest @id= ?", id)
        result = cursor.fetchone()[0]
        if result != "SUCCESS":
            text, code = messages.get(result, ("Something went wrong.", 400))
            return jsonify({"error": text}), code

        conn.commit()
        return jsonify({"message": "Borrow request cancelled."}), 200
    except Exception as e:
        conn.rollback()
        print("CANCEL ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 400
    finally:
        conn.close()

@app.route("/api/ongoing_borrow_request", methods=["GET"])
def get_ongoing_borrow_request():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    conn = get_connection()
    cursor = conn.cursor()

    data = []

    try:
        cursor.execute("EXEC uspGetOnGoingBorrowedItems @user_id = ?", session["user_id"])
        rows = cursor.fetchall()
        for row in rows:
            data.append({
                "image": row[0],
                "name": row[1],
                "category": row[2],
                "condition": row[3],
                "return_date": row[4].strftime("%B %d, %Y"),
                "start_date": row[5].strftime("%B %d, %Y"),
                "security_deposit": row[6],
                "status": row[7],
            })

        return jsonify(data)
    except Exception as e:
        print("ONGOING BORROW REQUEST ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 400
    finally:
        conn.close()

@app.route("/api/history_borrow_request", methods=["GET"])
def get_history_borrow_request():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    conn = get_connection()
    cursor = conn.cursor()
    data = []

    try:
        cursor.execute("EXEC uspGetHistory @user_id = ?", session["user_id"])
        rows = cursor.fetchall()
        for row in rows:
            data.append({
                "image": row[0],
                "name": row[1],
                "category": row[2],
                "condition": row[3],
                "start_date": row[4].strftime("%B %d, %Y") if row[4] else None,
                "return_date": row[5].strftime("%B %d, %Y") if row[5] else None,
                "security_deposit": row[6],
            })
        return jsonify(data)
    except Exception as e:
        print("HISTORY ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 400
    finally:
        conn.close()

@app.route("/profile")
def open_profile_page():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    return render_template("profile.html")

@app.route("/api/profile", methods=["GET"])
def get_profile():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC uspGetUserById @user_id = ?", session["user_id"])
        row = cursor.fetchone()
        if row is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify({
            "id": row[0],
            "username": row[1],
            "address": row[2],
            "contact": row[3],
            "image": row[4],
            "is_active": row[5],
        })
    except Exception as e:
        print("GET PROFILE ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/profile/update", methods=["PUT"])
def update_profile():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401

    conn = get_connection()
    cursor = conn.cursor()

    data = request.form
    image = request.files.get("image")

    try:
        # handle the image the same way as add-item
        image_url = None
        if image and image.filename and allowed_file(image.filename):
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            image_url = f"/static/uploads/{filename}"

        cursor.execute(
            "EXEC uspUpdateUser @user_id = ?, @username = ?, @address = ?, @contact = ?, @image = ?",
            session["user_id"], data["username"], data["address"], data["contact"], image_url
        )
        conn.commit()
        return jsonify({"message": "Profile updated successfully."}), 200

    except Exception as e:
        conn.rollback()
        print("UPDATE PROFILE ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 400
    finally:
        conn.close()

@app.route("/api/profile/stats", methods=["GET"])
def get_user_stats():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC uspGetUserStats @user_id = ?", session["user_id"])
        row = cursor.fetchone()
        return jsonify({
            "items_shared": row[0],
            "items_lent_out": row[1],
            "items_borrowing": row[2],
            "borrows_completed": row[3],
        })
    except Exception as e:
        print("USER STATS ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()

@app.route("/api/myitems")
def open_my_items_page():
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401
    return render_template("my_items.html")

@app.route("/api/items/my-items", methods=["GET"])
def get_my_items():
   if session.get("user_id") is None:
       return jsonify({"error": "You need to login first."}), 401


   selected_filter = request.args.get(
       "filter",
       "all"
   ).strip().lower()


   search_text = request.args.get(
       "search",
       ""
   ).strip()


   allowed_filters = {
       "all",
       "available",
       "borrowed",
       "latest"
   }


   if selected_filter not in allowed_filters:
       selected_filter = "all"


   conn = get_connection()
   cursor = conn.cursor()
   items = []


   try:
       if search_text:
           cursor.execute(
               "EXEC dbo.uspSearchItems "
               "@ownerID = ?, "
               "@search = ?, "
               "@filter = ?",
               session["user_id"],
               search_text,
               selected_filter
           )
       else:
           cursor.execute(
               "EXEC dbo.uspGetOwnerItems "
               "@ownerID = ?, "
               "@filter = ?",
               session["user_id"],
               selected_filter
           )


       rows = cursor.fetchall()


       for row in rows:
           items.append({
               "id": row[0],
               "image": row[1],
               "name": row[2],
               "category": row[3],
               "condition": row[4],
               "description": row[5],
               "note": row[6],
               "security_deposit": float(row[7] or 0),
               "status": row[8],
               "created_at": row[9].strftime("%B %d, %Y") if row[9] else "",
               "borrow_form_id": row[10],
           })


       return jsonify(items), 200


   except Exception as e:
       print("GET MY ITEMS ERROR:", e)


       return jsonify({
           "error": "Something went wrong."
       }), 500


   finally:
       conn.close()

@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def soft_delete_item(item_id):
   if session.get("user_id") is None:
       return jsonify({"error": "You need to login first."}), 401


   conn = get_connection()
   cursor = conn.cursor()


   messages = {
       "ITEM NOT FOUND": ("Item not found or you do not own this item.", 404),
       "ITEM BORROWED": ("A borrowed item cannot be deleted.", 400),
       "ALREADY UNAVAILABLE": ("This item is already unavailable.", 400),
   }


   try:
       cursor.execute(
           "EXEC dbo.uspUpdateItemStatus "
           "@itemID = ?, @ownerID = ?, @status = ?",
           (
               item_id,
               session["user_id"],
               "Unavailable"
           )
       )


       result = cursor.fetchone()[0]


       if result != "SUCCESS":
           text, code = messages.get(
               result,
               ("Unable to delete item.", 400)
           )
           return jsonify({"error": text}), code


       conn.commit()


       return jsonify({
           "message": "Item deleted successfully."
       }), 200


   except Exception as e:
       conn.rollback()
       print("SOFT DELETE ITEM ERROR:", e)


       return jsonify({
           "error": "Something went wrong."
       }), 500


   finally:
       conn.close()

@app.route("/api/my-items/<int:item_id>", methods=["GET"])
def get_my_item_by_id(item_id):
   if session.get("user_id") is None:
       return jsonify({"error": "You need to login first."}), 401


   conn = get_connection()
   cursor = conn.cursor()


   try:
       cursor.execute(
           "EXEC dbo.uspGetItemByIdMyItems @itemID = ?, @ownerID = ?",
           item_id,
           session["user_id"]
       )


       row = cursor.fetchone()


       if row is None:
           return jsonify({
               "error": "Item not found or you do not own this item."
           }), 404


       item = {
           "id": row[0],
           "name": row[1],
           "category_id": row[2],
           "condition": row[3],
           "description": row[4],
           "note": row[5],
           "image": row[6],
           "security_deposit": float(row[7] or 0),
           "status": row[8]
       }


       return jsonify(item), 200


   except Exception as e:
       print("GET ITEM BY ID ERROR:", e)
       return jsonify({"error": "Something went wrong."}), 500


   finally:
       conn.close()

@app.route("/api/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
   if session.get("user_id") is None:
       return jsonify({"error": "You need to login first."}), 401


   conn = get_connection()
   cursor = conn.cursor()


   data = request.form
   image = request.files.get("image")


   messages = {
       "ITEM NOT FOUND": (
           "Item not found or you do not own this item.",
           404
       ),
       "ITEM BORROWED": (
           "A borrowed item cannot be edited.",
           400
       ),
       "NO NAME": (
           "Please enter an item name.",
           400
       ),
       "NO CATEGORY": (
           "Please select a category.",
           400
       ),
       "INVALID CATEGORY": (
           "Please select a valid category.",
           400
       ),
       "NO CONDITION": (
           "Please enter the item condition.",
           400
       ),
       "INVALID DEPOSIT": (
           "Security deposit cannot be negative.",
           400
       )
   }


   try:
       image_url = None


       if image and image.filename:
           if not allowed_file(image.filename):
               return jsonify({
                   "error": "Please upload a valid image file."
               }), 400


           os.makedirs(UPLOAD_FOLDER, exist_ok=True)


           filename = (
               f"{uuid.uuid4().hex}_"
               f"{secure_filename(image.filename)}"
           )


           image.save(os.path.join(UPLOAD_FOLDER, filename))
           image_url = f"/static/uploads/{filename}"


       cursor.execute(
           "EXEC dbo.uspUpdateItem "
           "@itemID = ?, "
           "@ownerID = ?, "
           "@name = ?, "
           "@category = ?, "
           "@condition = ?, "
           "@description = ?, "
           "@note = ?, "
           "@image = ?, "
           "@securityDeposit = ?",
           item_id,
           session["user_id"],
           data.get("item_name"),
           data.get("category"),
           data.get("condition"),
           data.get("description"),
           data.get("note"),
           image_url,
           data.get("security_deposit") or 0
       )


       result = cursor.fetchone()[0]


       if result != "SUCCESS":
           text, code = messages.get(
               result,
               ("Unable to update item.", 400)
           )


           return jsonify({"error": text}), code


       conn.commit()


       return jsonify({
           "message": "Item updated successfully."
       }), 200


   except Exception as e:
       conn.rollback()
       print("UPDATE ITEM ERROR:", e)


       return jsonify({
           "error": "Something went wrong."
       }), 500

   finally:
       conn.close()

@app.route("/api/return_details/<int:borrow_form_id>", methods=["GET"])
def get_return_details(borrow_form_id):
    if session.get("user_id") is None:
        return jsonify({"error": "You need to login first."}), 401

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC uspGetReturnDetails @user_id = ?, @borrow_form = ?",
                       session["user_id"], borrow_form_id)
        row = cursor.fetchone()

        if row is None:
            return jsonify({"error": "Return details not found."}), 404

        return jsonify({
            "borrower_image": row[0],
            "borrower_name": row[1],
            "borrower_address": row[2],
            "item_image": row[3],
            "item_name": row[4],
            "item_category": row[5],
            "item_condition": row[6],
            "start_date": row[7].strftime("%B %d, %Y") if row[7] else "",
            "expected_return": row[8].strftime("%B %d, %Y") if row[8] else "",
            "security_deposit": float(row[9] or 0),
        })
    except Exception as e:
        print("RETURN DETAILS ERROR:", e)
        return jsonify({"error": "Something went wrong."}), 500
    finally:
        conn.close()


if __name__ == '__main__':
  app.run(debug=True)


