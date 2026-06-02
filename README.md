# NEXISS – Kenya's Digital Freelance Marketplace
## Full Setup Guide for Termux (Android)

---

## 📦 1. Install Termux
Download from F-Droid (NOT Play Store):
https://f-droid.org/en/packages/com.termux/

---

## ⚙️ 2. Setup Termux

```bash
# Update packages
pkg update && pkg upgrade -y

# Install Python
pkg install python -y

# Install pip
pip install --upgrade pip
```

---

## 📁 3. Copy Project Files

Copy the nexiss/ folder to your Termux home:
```
/data/data/com.termux/files/home/nexiss/
```

Or clone/download and move it there.

---

## 🐍 4. Install Dependencies

```bash
cd ~/nexiss
pip install flask
```

---

## 🚀 5. Run the Website

```bash
cd ~/nexiss
python app.py
```

You'll see:
```
 * Running on http://0.0.0.0:5000
```

Open your phone browser and go to:
**http://localhost:5000** or **http://127.0.0.1:5000**

---

## 🌐 6. Access from Other Devices (Same WiFi)

Find your phone IP:
```bash
ifconfig | grep inet
```

Then on any device on the same WiFi:
http://YOUR_PHONE_IP:5000

---

## 🔐 Demo Login Credentials

| Role   | Email                | Password   |
|--------|----------------------|------------|
| Admin  | admin@nexiss.com     | admin123   |
| Client | brian@gmail.com      | client123  |
| Worker | john@gmail.com       | worker123  |

---

## 📂 Project Structure

```
nexiss/
├── app.py              ← Main Flask app (routes, logic)
├── data.json           ← Auto-created database (JSON)
├── requirements.txt    ← Python dependencies
└── templates/
    ├── base.html           ← Shared layout, nav, styles
    ├── index.html          ← Public homepage
    ├── services.html       ← Services catalog
    ├── login.html          ← Login page
    ├── register.html       ← Registration page
    ├── client_dashboard.html  ← Client area
    ├── worker_dashboard.html  ← Worker area
    ├── admin_dashboard.html   ← Admin panel
    ├── place_order.html       ← Order form
    └── topup.html             ← Wallet top-up
```

---

## 💰 Commission System

Every order:
- **Worker gets 70%** of order amount
- **NEXISS gets 30%** platform fee
- Payment held in **escrow** until client approves

Example: KES 12,000 order
- Worker: KES 8,400
- Platform: KES 3,600

---

## 🛠️ Features

- ✅ Public website with services catalog
- ✅ Client registration & dashboard
- ✅ Worker dashboard with job tracking
- ✅ Admin panel (users, orders, revenue)
- ✅ Escrow payment system
- ✅ Wallet top-up (M-PESA simulated)
- ✅ Order placement with live price breakdown
- ✅ User ban system
- ✅ Worker job completion flow
- ✅ JSON file-based database (no setup needed)

---

## 🔄 Keep Running in Background (Termux)

```bash
# Install tmux
pkg install tmux -y

# Create session
tmux new -s nexiss

# Run app
cd ~/nexiss && python app.py

# Detach: Ctrl+B then D
# Reattach: tmux attach -t nexiss
```

---

Built with Flask + Python · Designed for Termux on Android
