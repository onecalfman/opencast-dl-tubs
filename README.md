# opencast-dl-tubs
Get direct links to all videos hosted on OpenCast via TU Braunschweig.

The bash script listed above downloads a json file containing direct links to all lectures uploaded to OpenCast by the Tu Braunschweig. It then parses the json file into a csv. Since i had no success with tools like jq the parsing is done with unix tools and leads to a few errors. Nevertheless i find it to be kind of usefull.

The script should run on Linux (tested) and MacOs with dmenu as an optional dependency.

It should in theorie work for all OpenCast implementation if the link to the json file is replaced.
