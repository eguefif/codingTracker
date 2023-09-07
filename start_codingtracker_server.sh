#/bin/bash

docker run -d --name codingtracker --network codingtrackernet --mount source=codingtracker,target=/data -p 10000:10000 eguefif/codingtracker:v0.0.2
