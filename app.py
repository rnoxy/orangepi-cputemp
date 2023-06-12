"""
This script runs a Flask web server on the Raspberry or Orange Pi
and returns the CPU temperature in JSON format when
you browse to http://<IP address of RPi>:80/cpu_temp

To run the script:
$ python app.py

Example curl command
$ curl http://<IP address of RPi>:80/cpu_temp?n_zones=6
"""

from flask import Flask, jsonify, request
import subprocess


app = Flask(__name__)


@app.route("/cpu_temp")
def cpu_temp():
    n_zones = request.args.get("n_zones", default=6, type=int)
    result = dict()
    total_temp = 0
    for zone in range(0, n_zones):
        temp = (
            float(
                subprocess.check_output(
                    ["cat", f"/sys/class/thermal/thermal_zone{zone}/temp"]
                )
            )
            / 1000.0
        )
        # round to 2 decimal places
        temp = round(temp, 2)
        result[f"temp_zone{zone}"] = temp
        total_temp += temp

    result["temp_average"] = total_temp / n_zones
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=80)
