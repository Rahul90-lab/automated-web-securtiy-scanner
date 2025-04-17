from flask import Flask, request, jsonify, render_template, send_file
import os
import csv
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Store scan results in memory
scan_results = []

# OWASP Top 10 Tests: Mock Scanner
def scan_website(url):
    vulnerabilities = {
        "SQL Injection": ["Detected on parameter 'id'"] if "id=" in url else [],
        "XSS": ["Detected on input field"] if "search=" in url else [],
        "CSRF": ["Potential CSRF vulnerability detected"] if "csrf=" in url else [],
        "Open Redirect": ["Unvalidated redirect detected"] if "redirect=" in url else [],
    }

    result = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "url": url,
        "SQL Injection": vulnerabilities["SQL Injection"],
        "XSS": vulnerabilities["XSS"],
        "CSRF": vulnerabilities["CSRF"],
        "Open Redirect": vulnerabilities["Open Redirect"],
    }

    scan_results.append(result)
    return result

@app.route("/")
def index():
    return render_template("index2.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    url = data.get("url")
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = scan_website(url)
    return jsonify(result)

@app.route("/results")
def get_results():
    return jsonify(scan_results)

@app.route("/download/pdf")
def download_pdf():
    file_path = "scan_report.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(100, 750, "Web Security Scan Report")
    c.drawString(100, 730, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = 700
    for scan in scan_results:
        c.drawString(100, y, f"URL: {scan['url']}")
        c.drawString(100, y-20, f"SQL Injection: {', '.join(scan['SQL Injection']) or 'None'}")
        c.drawString(100, y-40, f"XSS: {', '.join(scan['XSS']) or 'None'}")
        c.drawString(100, y-60, f"CSRF: {', '.join(scan['CSRF']) or 'None'}")
        c.drawString(100, y-80, f"Open Redirect: {', '.join(scan['Open Redirect']) or 'None'}")
        c.drawString(100, y-100, "-" * 50)
        y -= 120

    c.save()
    return send_file(file_path, as_attachment=True)

@app.route("/download/csv")
def download_csv():
    file_path = "scan_report.csv"
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "URL", "SQL Injection", "XSS", "CSRF", "Open Redirect"])
        for scan in scan_results:
            writer.writerow([
                scan["timestamp"], scan["url"],
                ", ".join(scan["SQL Injection"]) or "None",
                ", ".join(scan["XSS"]) or "None",
                ", ".join(scan["CSRF"]) or "None",
                ", ".join(scan["Open Redirect"]) or "None"
            ])
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
