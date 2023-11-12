from flask import Flask, jsonify
from unidecode import unidecode
import numpy as np

import json

app = Flask(__name__)

data_file_path = "data/world.geojson.json"
data = json.load(open(data_file_path, "r"))


# get random country
def get_random_country(countries):
    index = np.random.randint(0, len(countries))
    return countries[index]


def get_country_names(countries):
    def mapper(country):
        return country["properties"]["name_long"]

    return list(map(mapper, countries))


@app.route("/random_country", methods=["GET"])
def random_country():
    country = get_random_country(data)

    return jsonify(country)


@app.route("/country_names", methods=["GET"])
def country_names():
    names = get_country_names(data)

    return jsonify(names)


@app.route("/info/<country>")
def get_country_info(country):
    targetCountry = None

    for c in data:
        if (
            unidecode(c["properties"]["name_long"].replace(" ", "").replace("'", ""))
            == country
        ):
            targetCountry = c
            break

    response = targetCountry["properties"]

    return jsonify(response)


if __name__ == "__main__":
    app.run(port=8000)
