import os
import json
from datetime import datetime
from pprint import pprint
from flask import Flask, render_template, Response, request
import dweepy


APP = Flask(__name__, static_url_path="/pi-dash/static", static_folder="static",)
APP.debug = False

DWEET_THING = os.environ.get("DWEET_THING")


def get_results():
    """
    :return:
    """
    try:
        dweet = dweepy.get_latest_dweet_for(DWEET_THING)
        results = json.loads(dweet[0]['content']['results'])
    except Exception as err:
        results = [
            {"name": "UNKOWN", "last_start_time": "", "last_end_time": "",
             "status": 0, "status_message": err, "alert_level": "UNKNOWN",
             "latency": 0.0, "label": "error", "sort": 10}]
    return results

@APP.route('/')
def get_jobs():
    """
    :return:
    """
    logo_url = '/pi-dash/static/images/pi.png'
    print(DWEET_THING)
    jobs = get_results()
    jobs.sort(key=lambda i: i['sort'])
    return render_template("jobs.html",
                           title='pi-dash',
                           asof="Last Updated: {0}".format(datetime.now().strftime("%I:%M %p")),
                           logo=logo_url,
                           status_path='',
                           jobs=jobs)


if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=False)
