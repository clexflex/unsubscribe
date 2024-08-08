from flask import Flask, request
import boto3
import sqlite3
import logging
import csv
import os
from datetime import datetime

app = Flask(__name__)
REGION = 'us-east-1'  # Your AWS region
client = boto3.client('pinpoint', region_name=REGION)

def unsubscribe_user(email):
    response = client.update_endpoint(
        ApplicationId='bf367a645f3846e39705c3c4d38799a8',  # Replace with your Application ID
        EndpointId=email,  # Use email as EndpointId for simplicity
        EndpointRequest={
            'ChannelType': 'EMAIL',
            'OptOut': 'ALL'
        }
    )
    return response

def store_unsubscribed_email(email):
    try:
        conn = sqlite3.connect('unsubscribe.db')
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO unsubscribed_emails (email, unsubscribed_at) VALUES (?, ?)',
                  (email, datetime.now()))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")

@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    email = request.args.get('email')
    if email:
        unsubscribe_user(email)
        1(email)
        return "You have been unsubscribed successfully."
    return "Invalid request.", 400

@app.route('/export', methods=['GET'])
def export_unsubscribed_emails():
    try:
        conn = sqlite3.connect('unsubscribe.db')
        c = conn.cursor()
        c.execute('SELECT email FROM unsubscribed_emails')
        rows = c.fetchall()
        conn.close()

        with open('unsubscribed_emails.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Email'])
            csvwriter.writerows(rows)
        
        return "Unsubscribed emails exported successfully to unsubscribed_emails.csv."
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
        return "Error exporting unsubscribed emails.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))