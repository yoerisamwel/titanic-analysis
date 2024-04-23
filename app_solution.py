import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template_string


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///titanic.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Passenger = Base.classes.passenger

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes and provide download links."""
    html = """
    <html>
    <head>
        <title>API Home</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333366; }
            a.button {
                display: inline-block;
                padding: 10px 20px;
                margin: 10px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                text-decoration: none;
            }
            a.button:hover {
                background-color: #45a049;
            }
            .content {
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to the Titanic API</h1>
        <div class="content">
            <a href="/api/v1.0/names" class="button" download="names.json">Download Names</a>
            <a href="/api/v1.0/passengers" class="button" download="passengers.json">Download Passengers</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/api/v1.0/names")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Passenger.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/passengers")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
