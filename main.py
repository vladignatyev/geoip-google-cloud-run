'''
IP2GEO API using MaxMind GeoLite2 DB
'''
import os

from flask import Flask, request, jsonify

from http import HTTPStatus

import geoip2.database  # pylint: disable=import-error
from geoip2.errors import AddressNotFoundError  # pylint: disable=import-error


UNKNOWN_CONTINENT = "U"
UNKNOWN_COUNTRY = "U"
UNKNOWN_ASN = -1

COUNTRY_MMDB = "GeoLite2-Country.mmdb"
ASN_MMDB = "GeoLite2-ASN.mmdb"

country_reader = geoip2.database.Reader(COUNTRY_MMDB)
asn_reader = geoip2.database.Reader(ASN_MMDB)

app = Flask(__name__)


@app.route("/")
def home():
    # Get the IP address of the client from proxy headers
    ip_addr_from_proxy_or_request = request.headers.get('X-Forwarded-For', str(request.remote_addr))
    try:
        ip_addr = request.args.get("ip", ip_addr_from_proxy_or_request)
    except KeyError:
        return {"statusCode": HTTPStatus.BAD_REQUEST}

    asn = UNKNOWN_ASN
    continent = UNKNOWN_CONTINENT
    country = UNKNOWN_COUNTRY
    is_eu = False

    try:
        asn = asn_reader.asn(ip_addr).autonomous_system_number
    except AddressNotFoundError:
        pass

    try:
        c = country_reader.country(ip_addr)
        continent = c.continent.code
        country = c.country.iso_code
        is_eu = c.country.is_in_european_union
    except AddressNotFoundError:
        pass
    
    response = {
        "ip": ip_addr,
        "asn": asn,
        "continent": continent,
        "country": country,
        "is_eu": is_eu,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


