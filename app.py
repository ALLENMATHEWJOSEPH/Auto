from flask import Flask, render_template, request, redirect, url_for
import gspread
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_booking', methods=['GET', 'POST'])
def submit_booking():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        date = request.form.get('date')
        time = request.form.get('time')
        service_type = request.form.get('service_type')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # IMPORTANT: Ensure 'service_account.json' is in the 'carwash_app' directory
            # For a containerized environment, the path might need to be absolute or relative to app.py's location
            # The problem description implies service_account.json is in carwash_app, so 'carwash_app/service_account.json'
            gc = gspread.service_account(filename='carwash_app/service_account.json')

            # Open the Google Sheet by its key
            sh = gc.open_by_key("1yjLWyONSZcVV2t9wdE5ETtceFK6wVLEsftphsHgAW1w")

            # Select the worksheet (tab). Using "Sheet1" as specified.
            worksheet = sh.worksheet("Sheet1") # Or sh.sheet1 if it's the first sheet

            # Prepare data for the new row
            row_data = [name, phone, email, address, date, time, service_type, timestamp]

            # Append the new row
            worksheet.append_row(row_data)

            print(f"New Booking for {name} successfully written to Google Sheet.")

        except Exception as e:
            print(f"Error writing to Google Sheet: {e}")
            # Optionally, you could add a flash message to the user here

        return redirect(url_for('index'))

    return redirect(url_for('booking'))

if __name__ == '__main__':
    app.run(debug=True)
