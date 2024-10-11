# Google Cloud Run Example
## MaxMind GeoLite2 geoip (ip2geo) database
This ip2geo API retrieves a geolocation information 
by IP address of the client and responds with JSON 
that contains the country code, the flag that tells 
if it is within EU or not, the continent where the country 
located and the ASN number that the IP address belong to.

This is a containerized version of the API https://github.com/vladignatyev/geoip-digitalocean-functions
Initilal

# How to deploy to Google Cloud Run
Assume that you have created the Project and the Artifacts Registry repository already. 
If not, please walk through the documentation: https://cloud.google.com/run/docs/building/containers

1. Clone repo.
2. Build the image locally using Docker: `docker build . --tag <REGISTRY_REGION>-docker.pkg.dev/<PROJECT_ID>/<REPOSITORY_NAME>/geoip-image:latest`
3. Push the image to the Google Cloud Run Artifacts Repository: `docker push <REGISTRY_REGION>-docker.pkg.dev/<PROJECT_ID>/<REPOSITORY_NAME>/geoip-image:latest`
4. Run `gcloud run deploy geoip --image <SERVICE_REGION>.pkg.dev/<PROJECT_ID>/<REPOSITORY_NAME>/geoip-image:latest`

# Invoke/Demo
After the successful deployment you will see the Service URL for the newly created service located in SERVICE_REGION, billed at PROJECT_ID.

# Notice on implementation
I used Flask and intentionally put all `requirements.txt` dependencies into the `Dockerfile` itself.
This approach enables Docker to keep pip dependencies as a separate layer and reduce time required to build the image.

# Development
For development run the container locally: `docker build . -t geoip && docker run -e PORT=8080 -p 8080:8080 geoip`

`curl localhost:8080?ip=8.8.8.8` should print: `{"asn":15169,"continent":"NA","country":"US","ip":"8.8.8.8","is_eu":false}`.

# MaxMind database updates
MaxMind databases are downloaded during the build of the Docker image using curl. In case you need to replace them, 
change the corresponding URLs in `Dockerfile`. 