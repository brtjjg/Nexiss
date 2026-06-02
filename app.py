from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json, os, hashlib, uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = "nexiss_secret_2024"

DATA_FILE = "data.json"

# ── seed data ──────────────────────────────────────────────────
def load_data():
    if not os.path.exists(DATA_FILE):
        default = {
            "users": {
                "admin": {
                    "id": "admin",
                    "name": "Admin",
                    "email": "admin@nexiss.com",
                    "password": hashlib.sha256("admin123".encode()).hexdigest(),
                    "role": "admin",
                    "wallet": 0,
                    "joined": "2024-01-01"
                },
                "brian": {
                    "id": "brian",
                    "name": "Brian Kamau",
                    "email": "brian@gmail.com",
                    "password": hashlib.sha256("client123".encode()).hexdigest(),
                    "role": "client",
                    "wallet": 25000,
                    "joined": "2024-05-01"
                },
                "john": {
                    "id": "john",
                    "name": "John Doe",
                    "email": "john@gmail.com",
                    "password": hashlib.sha256("worker123".encode()).hexdigest(),
                    "role": "worker",
                    "wallet": 8400,
                    "pending": 3600,
                    "rating": 4.8,
                    "completed": 15,
                    "joined": "2024-03-01",
                    "skills": ["Web Design", "Logo Design", "SEO"],
                    "verified": True
                }
            },
            "orders": [
                {
                    "id": "ORD-1001",
                    "client_id": "brian",
                    "worker_id": "john",
                    "service": "Business Website",
                    "amount": 12000,
                    "worker_cut": 8400,
                    "platform_cut": 3600,
                    "status": "In Progress",
                    "date": "2024-05-10"
                },
                {
                    "id": "ORD-1002",
                    "client_id": "brian",
                    "worker_id": "john",
                    "service": "Logo Design",
                    "amount": 1000,
                    "worker_cut": 700,
                    "platform_cut": 300,
                    "status": "Completed",
                    "date": "2024-05-09"
                },
                {
                    "id": "ORD-1003",
                    "client_id": "brian",
                    "worker_id": "john",
                    "service": "SEO Setup",
                    "amount": 8000,
                    "worker_cut": 5600,
                    "platform_cut": 2400,
                    "status": "Pending",
                    "date": "2024-05-08"
                }
            ],
            "services": [
                {"category": "Web Development", "name": "Landing Page", "price": 3500},
                {"category": "Web Development", "name": "Business Website", "price": 12000},
                {"category": "Web Development", "name": "E-commerce Website", "price": 25000},
                {"category": "Web Development", "name": "School Website", "price": 18000},
                {"category": "Web Development", "name": "Portfolio Website", "price": 6000},
                {"category": "Web Development", "name": "Web Application", "price": 40000},
                {"category": "Mobile Apps", "name": "Basic Android App", "price": 20000},
                {"category": "Mobile Apps", "name": "Business App", "price": 35000},
                {"category": "Mobile Apps", "name": "E-commerce App", "price": 50000},
                {"category": "Mobile Apps", "name": "Delivery App", "price": 70000},
                {"category": "Design", "name": "Logo Design", "price": 1000},
                {"category": "Design", "name": "Poster Design", "price": 500},
                {"category": "Design", "name": "Flyer Design", "price": 300},
                {"category": "Design", "name": "Brand Kit", "price": 5000},
                {"category": "Video", "name": "TikTok Editing", "price": 300},
                {"category": "Video", "name": "YouTube Shorts", "price": 400},
                {"category": "Video", "name": "YouTube Video", "price": 1500},
                {"category": "Video", "name": "Promo Video", "price": 3000},
                {"category": "AI Services", "name": "AI Chatbot Setup", "price": 8000},
                {"category": "AI Services", "name": "AI Automation", "price": 20000},
                {"category": "AI Services", "name": "AI Content Tools", "price": 500},
                {"category": "Marketing", "name": "Facebook Ads Setup", "price": 2000},
                {"category": "Marketing", "name": "TikTok Ads", "price": 2500},
                {"category": "Marketing", "name": "SEO Setup", "price": 8000},
                {"category": "Writing", "name": "CV Writing", "price": 500},
                {"category": "Writing", "name": "Business Plan", "price": 5000},
                {"category": "Writing", "name": "E-book Writing", "price": 10000},
                {"category": "Education", "name": "Assignment Help", "price": 300},
                {"category": "Education", "name": "Tutoring", "price": 500},
                {"category": "Business", "name": "Data Entry", "price": 500},
                {"category": "Business", "name": "Virtual Assistant", "price": 5000},
                {"category": "Business", "name": "Market Research", "price": 3000},
            ],
            "platform_revenue": 25430,
            "escrow": []
        }
        save_data(default)
        return default
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user():
    if "user_id" in session:
        data = load_data()
        return data["users"].get(session["user_id"])
    return None

# ── public pages ───────────────────────────────────────────────
@app.route("/")
def index():
    data = load_data()
    categories = list({s["category"] for s in data["services"]})
    return render_template("index.html", services=data["services"], categories=categories, user=get_user())

@app.route("/services")
def services():
    data = load_data()
    categories = list({s["category"] for s in data["services"]})
    return render_template("services.html", services=data["services"], categories=categories, user=get_user())

# ── auth ───────────────────────────────────────────────────────
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        data = load_data()
        email = request.form["email"]
        pw = hashlib.sha256(request.form["password"].encode()).hexdigest()
        for uid, u in data["users"].items():
            if u["email"] == email and u["password"] == pw:
                session["user_id"] = uid
                if u["role"] == "admin":
                    return redirect(url_for("admin_dashboard"))
                elif u["role"] == "worker":
                    return redirect(url_for("worker_dashboard"))
                else:
                    return redirect(url_for("client_dashboard"))
        flash("Invalid credentials", "error")
    return render_template("login.html", user=get_user())

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        data = load_data()
        name = request.form["name"]
        email = request.form["email"]
        role = request.form["role"]
        pw = hashlib.sha256(request.form["password"].encode()).hexdigest()
        uid = name.lower().replace(" ", "_") + "_" + str(uuid.uuid4())[:4]
        data["users"][uid] = {
            "id": uid, "name": name, "email": email,
            "password": pw, "role": role,
            "wallet": 0, "joined": datetime.now().strftime("%Y-%m-%d"),
            "pending": 0, "rating": 0, "completed": 0,
            "skills": [], "verified": False
        }
        save_data(data)
        session["user_id"] = uid
        flash("Account created! Welcome to NEXISS.", "success")
        return redirect(url_for("client_dashboard" if role=="client" else "worker_dashboard"))
    return render_template("register.html", user=get_user())

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ── client area ────────────────────────────────────────────────
@app.route("/client")
def client_dashboard():
    u = get_user()
    if not u or u["role"] not in ("client","admin"):
        return redirect(url_for("login"))
    data = load_data()
    my_orders = [o for o in data["orders"] if o["client_id"] == u["id"]]
    return render_template("client_dashboard.html", user=u, orders=my_orders)

@app.route("/client/order", methods=["GET","POST"])
def place_order():
    u = get_user()
    if not u:
        return redirect(url_for("login"))
    data = load_data()
    if request.method == "POST":
        service_name = request.form["service"]
        svc = next((s for s in data["services"] if s["name"]==service_name), None)
        if svc:
            amount = svc["price"]
            if u["wallet"] < amount:
                flash("Insufficient wallet balance. Please top up.", "error")
            else:
                oid = "ORD-" + str(uuid.uuid4())[:6].upper()
                data["users"][u["id"]]["wallet"] -= amount
                data["escrow"].append({"order_id": oid, "amount": amount})
                data["orders"].append({
                    "id": oid, "client_id": u["id"], "worker_id": None,
                    "service": service_name, "amount": amount,
                    "worker_cut": int(amount*0.7), "platform_cut": int(amount*0.3),
                    "status": "Pending", "date": datetime.now().strftime("%Y-%m-%d")
                })
                save_data(data)
                flash(f"Order placed! KES {amount:,} held in escrow.", "success")
                return redirect(url_for("client_dashboard"))
    return render_template("place_order.html", user=u, services=data["services"])

# ── worker area ────────────────────────────────────────────────
@app.route("/worker")
def worker_dashboard():
    u = get_user()
    if not u or u["role"] not in ("worker","admin"):
        return redirect(url_for("login"))
    data = load_data()
    my_jobs = [o for o in data["orders"] if o.get("worker_id") == u["id"]]
    return render_template("worker_dashboard.html", user=u, jobs=my_jobs)

@app.route("/worker/complete/<order_id>")
def complete_job(order_id):
    u = get_user()
    if not u:
        return redirect(url_for("login"))
    data = load_data()
    for o in data["orders"]:
        if o["id"] == order_id and o.get("worker_id") == u["id"]:
            o["status"] = "Completed"
            data["users"][u["id"]]["wallet"] = data["users"][u["id"]].get("wallet",0) + o["worker_cut"]
            data["users"][u["id"]]["completed"] = data["users"][u["id"]].get("completed",0) + 1
            data["platform_revenue"] = data.get("platform_revenue",0) + o["platform_cut"]
            save_data(data)
            flash(f"Job completed! KES {o['worker_cut']:,} added to your wallet.", "success")
            break
    return redirect(url_for("worker_dashboard"))

# ── admin area ─────────────────────────────────────────────────
@app.route("/admin")
def admin_dashboard():
    u = get_user()
    if not u or u["role"] != "admin":
        return redirect(url_for("login"))
    data = load_data()
    total_users = len(data["users"])
    total_workers = sum(1 for x in data["users"].values() if x["role"]=="worker")
    total_orders = len(data["orders"])
    pending = sum(1 for o in data["orders"] if o["status"]=="Pending")
    return render_template("admin_dashboard.html",
        user=u, data=data,
        total_users=total_users, total_workers=total_workers,
        total_orders=total_orders, pending=pending,
        revenue=data.get("platform_revenue",0)
    )

@app.route("/admin/assign/<order_id>/<worker_id>")
def assign_order(order_id, worker_id):
    u = get_user()
    if not u or u["role"] != "admin":
        return redirect(url_for("login"))
    data = load_data()
    for o in data["orders"]:
        if o["id"] == order_id:
            o["worker_id"] = worker_id
            o["status"] = "In Progress"
    save_data(data)
    flash("Worker assigned!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/ban/<user_id>")
def ban_user(user_id):
    u = get_user()
    if not u or u["role"] != "admin":
        return redirect(url_for("login"))
    data = load_data()
    if user_id in data["users"] and user_id != "admin":
        data["users"][user_id]["banned"] = True
        save_data(data)
        flash(f"User {user_id} banned.", "success")
    return redirect(url_for("admin_dashboard"))

# ── wallet top-up (simulated) ──────────────────────────────────
@app.route("/topup", methods=["GET","POST"])
def topup():
    u = get_user()
    if not u:
        return redirect(url_for("login"))
    if request.method == "POST":
        amount = int(request.form.get("amount", 0))
        if amount > 0:
            data = load_data()
            data["users"][u["id"]]["wallet"] = data["users"][u["id"]].get("wallet",0) + amount
            save_data(data)
            flash(f"KES {amount:,} added to your wallet (M-PESA simulated).", "success")
            return redirect(url_for("client_dashboard"))
    return render_template("topup.html", user=u)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
