from flask import Flask, render_template, request,session
from datetime import datetime
import joblib
import pandas as pd
from const import *
import random
import json


# Load the trained model
model = joblib.load("hotel.pkl")
flightmodel = joblib.load("flight_model.pkl")
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/ticket", methods=["POST"])
def submit_ticket():
    date_input = request.form.get("fdate")
    fdate = datetime.strptime(date_input, "%Y-%m-%d").strftime("%d %b %Y")
    print(fdate)
    tdate_input = request.form.get("tdate")
    tdate = datetime.strptime(tdate_input, "%Y-%m-%d").strftime("%d %b %Y")
    from_location = request.form.get("from")
    to_location = request.form.get("to")
    flight_class = request.form.get("flightclass")
    passengers = request.form.get("passengers")
    airline = request.form.get("airline")
    
    # Fetch available hotels in the destination city
    available_hotels = hotels.get(to_location, [])
    
    
    from_city = request.form.get("from")
    to_city = request.form.get("to")
    departure_time = random.choice(["Morning", "Afternoon", "Evening", "Night"])
    arrival_time = random.choice(["Morning", "Afternoon", "Evening", "Night"])
    flight=random.choice(flights)
    stops = random.choice(["zero", "one", "two"])
    duration = round(random.uniform(1.0, 15.0), 2)

    # Get "From Date" from form and calculate "days_left"
    fdate = request.form.get("fdate")  # format "YYYY-MM-DD"
    if fdate:
        fdate_obj = datetime.strptime(fdate, "%Y-%m-%d").date()
        today = datetime.today().date()
        days_left = (fdate_obj - today).days
    else:
        days_left = random.randint(1, 100)  # If no date is provided, fallback to random

    # Create an input array matching the features used in training
    from_code = airport_codes.get(from_city, None)[0]
    to_code = airport_codes.get(to_city, None)[0]
    from_img=airport_codes.get(from_city, None)[1]
    to_img=airport_codes.get(to_city, None)[1]

    input_features = pd.DataFrame({
        "airline": [airline],
        "flight": [flight],
        "source_city": [from_city],
        "departure_time": [departure_time],
        "stops": [stops],
        "arrival_time": [arrival_time],
        "destination_city": [to_city],
        "class": [flight_class],
        "duration": [int(duration)],
        "days_left": [int(days_left)]
    })

    print(input_features)

    price_prediction = flightmodel.predict(input_features)[0]  # Predicting for one instance
    print("price_prediction",price_prediction)
    
    if from_city ==to_city:
        price_prediction = 0.00

    ticket_details = {
        "from": from_city,
        "to": to_city,
        "date": fdate,
        "flight_class": flight_class,
        "airline": airline,
        "passengers": passengers,
        "departure_time": departure_time,
        "stops": stops,
        "days_left": days_left,
        "price": round(price_prediction, 2),
        "from_code":from_code,
        "to_code":to_code,
        "from_img":from_img,
        "to_img":to_img ,
        "flight":flight
    }
    session['ticket_details'] = ticket_details
    return render_template("hotel_selection.html", fdate=fdate,tdate=tdate, from_location=from_location,
                           to_location=to_location, flight_class=flight_class,
                           passengers=passengers, available_hotels=available_hotels,airline=airline,td=ticket_details)

@app.route("/hotel-selection", methods=["POST"])
def submit_hotel_selection():
    hotel_name = request.form.get("hotel")
    location = request.form.get("to_location")
    checkin_date = request.form.get("checkin_date")
    checkout_date = request.form.get("checkout_date")
    td = session.get('ticket_details')
  

    hotel_data = pd.DataFrame({
        "name": [hotel_name],
        "checkin_date": [checkin_date],
        "checkout_date": [checkout_date],
        "city": [location]
    })
    print(hotel_data)

    
    # Predict the price using the loaded model
    predicted_price = model.predict(hotel_data)[0]
    print("Predicted Price",predicted_price)
    
    # Retrieve selected hotel details
    selected_hotel = None
    for hotel in hotels.get(location, []):
        if hotel["name"] == hotel_name:
            selected_hotel = hotel
            break
    cd=datetime.strptime(checkin_date, "%Y-%m-%d").strftime("%d %b %Y")
    
    
    
    
    
    
    
    session['hotelticket']={
 "hotel_name": hotel_name,
  
  "hotel": selected_hotel,
  "price": round(predicted_price, 2)  ,
  "tax": round(predicted_price*0.12,2),
  'rate': round((predicted_price-0.12*predicted_price),2),  
  "location": location,
  "checkin_date": cd,
  "checkout_date": checkout_date
}
    
    ht = session.get('hotelticket')
    print(ht)
    td = session.get('ticket_details')
    if selected_hotel:
        return render_template("price_prediction.html",ht=ht,td=td)
    
    return "Hotel not found"

 
@app.route("/flightticket")
def flight_ticket():
    td = session.get('ticket_details')
    return render_template("ticket.html",td=td)   
 
@app.route("/hotelticket")
def hotel_ticket():
    ht = session.get('hotelticket')
    return render_template("hotelticket.html",ht=ht)    
@app.route("/pricepred")
def pricepred():
    ht = session.get('hotelticket')
    print(ht)
    td = session.get('ticket_details')
    return render_template("price_prediction.html",ht=ht,td=td) 

if __name__ == "__main__":
    app.secret_key = 'ruchagavade' 
    app.run(debug=True)
    

