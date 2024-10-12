"""
IP2GEO API using MaxMind GeoLite2 DB
"""

import os

from flask import Flask, request, jsonify

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
    ip_addr_from_proxy_or_request = request.headers.get(
        "X-Forwarded-For", str(request.remote_addr)
    )

    # Get the IP address from the query string or use
    # one from the proxy headers
    ip_addr = request.args.get("ip", ip_addr_from_proxy_or_request)

    # Provide defaults for the response
    asn = UNKNOWN_ASN
    continent = UNKNOWN_CONTINENT
    country = UNKNOWN_COUNTRY
    is_eu = False

    try:
        # Get the ASN for the IP address
        asn = asn_reader.asn(ip_addr).autonomous_system_number
    except AddressNotFoundError:
        # Didn't find ASN for the IP address
        pass

    try:
        # Get the country for the IP address
        c = country_reader.country(ip_addr)
        continent = c.continent.code
        country = c.country.iso_code
        is_eu = c.country.is_in_european_union
    except AddressNotFoundError:
        # Didn't find country for the IP address
        pass

    # Prepare the response
    response = {
        "ip": ip_addr,
        "asn": asn,
        "continent": continent,
        "country": country,
        "is_eu": is_eu,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("DEBUG", False),
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
    )
