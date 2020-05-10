# opencast-downloader
Get direct links to all videos hosted on OpenCast via your organisation.

The bash script listed above downloads a json file containing direct links to all lectures uploaded to OpenCast by the Tu Braunschweig. It then parses the json file into a csv. Since i had no success with tools like jq the parsing is done with unix tools and leads to a few errors. Nevertheless i find it to be kind of usefull and alsmost all videos are listed without a problem.

The script should run on Linux (tested) and macOs with dmenu as optional dependency.

It should work for all OpenCast implementation if the base_url variable is set. But it's only tested for the TU Braunschweig.
