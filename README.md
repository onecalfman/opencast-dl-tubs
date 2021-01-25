# opencast-downloader
Get a csv of direct links to videos hosted on OpenCast via your organisation.
I have now added a python version with is way more stable and efficient.

## Description
This program will generate a csv file from the last 2000 Videos/Lectures uploaded to an opencast server if you can provide the link to the needed json file which should be on site-url/search/episode.json for example: https://opencast-present.rz.tu-bs.de/search/episode.json
Since the last 2000 is a changing batch, it is advised to run the scripts regulary. Both the bash and python version will merge existing csv's with new entries.

## Python Version
The python version has currently a lot of dependencies but if it works it works ¯\_(ツ)_/¯
Ther are a few comments in the code itself which hopefully help to figure out how to use it.
PS: currently it works only on *nix systems

## Bash Version
It will then generate a csv from that json file using jq.

NOTE: that the json file - at least for my university - contains 2000 entries at all times, so older lectures might be lost. To mitigate this, the program will expand your csv with the new entries and hopefully provide you with a more and more complete list of all uploaded videos. If you run it on a regular basis.

The variables for url andfile path need to be specified at the top of the script.  If an auto download file is provided this script, will download all specified lectures to the given path.  If the mail variable is set up a mail system you will get an email with your new auto-downloads, which is handy if you run it as cronjob.

### Dependencies 

* [jq - versatile json-parser](https://stedolan.github.io/jq/)
* wget

### Options
* -d   --   download json

* -c   --   generate csv from json

* -f   --   force download for all videos (for -a option)
            default behaviour: don't overwrite existing files
            which are the same size as the remote file.

* -a   --   automatically download all files whitch match the
            seriestitle string supplied in the auto_download_file
            and save them in the corresponding folder the
            seriestitle and folder need to double-quoted like:\
            "seriestitle" "folder"\
            "Rechnungswesen" "uni/rechnungswesen"\
            "Mechanik 2" "uni/tm2"
