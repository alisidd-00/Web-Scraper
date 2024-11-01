from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)

# Load CSV data into memory for quick lookup
def load_csv_data(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

# Load data at the start of the application
companies_data = load_csv_data(r'C:\Users\F\Desktop\web scraper\Web-Scraper\begin\scraped_info.csv')

# Endpoint 1: Get CIK code by company name
@app.route('/get_cik', methods=['GET'])
def get_cik():
    company_name = request.args.get('company_name', '').lower()
    if not company_name:
        return jsonify({"error": "Company name is required"}), 400

    # Search for company in CSV data
    for company in companies_data:
        if company_name == company['name'].lower():
            return jsonify({"company_name": company['CompanyName'], "CIK": company['CIK']})

    return jsonify({"error": "CIK not found for the given company name"}), 404

# Endpoint 2: Get company info by CIK code
@app.route('/get_company_info', methods=['GET'])
def get_company_info():
    cik = request.args.get('cik')
    if not cik:
        return jsonify({"error": "CIK code is required"}), 400

    # Search for CIK in CSV data
    for company in companies_data:
        if cik == company['cik']:
            return jsonify(company)

    return jsonify({"error": "Company info not found for the given CIK"}), 404

if __name__ == '__main__':
    app.run(debug=True)
