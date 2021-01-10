import json
import urllib.error
import urllib.request
import click
import sys
import time

from metr_data_collector_version.version import DATA_COLLECTOR_VERSION


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.version_option(version=DATA_COLLECTOR_VERSION + ', written as programming test for metr by Johan Lund')
@click.pass_context
def cli(ctx, debug):
    """
    CLI tool that reads a config file and collects data from a specified url at a specified interval.
    """
    # ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug


def _died(msg, return_code=1):
    print('ERROR: %s' % msg)
    sys.exit(return_code)


def write_data(data_string, file_path):
    """
    Appends data in string format to a text file. Adds a date-time prefix.

    :param data_string:
    :param file_path:
    :return:
    """
    curr_time = time.asctime(time.localtime(time.time()))
    output_string = curr_time + ": " + data_string + "\n"
    with open(file_path, 'a') as file:
        file.write(output_string)


def get_data(url_path):
    """

    :param url_path:
    :return:
    """
    # https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
    data = {}
    try:
        with urllib.request.urlopen(url_path) as _url:
            _string = _url.read().decode()
            raise urllib.error.HTTPError(url=url_path, code=500, msg="generated error", hdrs=None, fp=None)
    except ValueError as errv:
        _string = "ValueError caught: %s" % errv
    except urllib.error.URLError as erru:
        _string = "URLError caught: %s" % erru

    return _string


@cli.command()
@click.option('-C', '--config_path', required=True, help='path to local config file')
@click.option('-O', '--output_path', required=True, help='path to the output file')
def collect_data(config_path, output_path):
    """
    Develop a solution to obtain configuration data for an IoT device on boot

    At metr we are running IoT devices similar to a raspberry pi with linux on it. One of the challenges we are facing is to make sure our IoT devices are downloading a set configuration settings on boot. The configuration settings are a simple set of key value pairs which are essential to a process running on the same device that needs to be started after obtaining the configuration settings. Let's call this process "data-collector". This data-collector process requires the information from the key value pairs to function correctly and it shouldn't be started without those settings.

    We provide a public endpoint mocking the configuration server. If you are sending a request to http://82.165.112.45:4710/config/AC67DD you'll receive a response containing the configuration for your fictional IoT device. One thing you might notice is that the response isn't very stable. Sometimes the configuration service will give you a 500 or incomplete information. The correct response you are looking for has a HTTP Status of 200 with a payload looking like this:
    { "id": "AC67DD", "endpoint": "http://numbersapi.com/random/trivia", "interval": 59 }
    The data-collector process will use the endpoint value as an endpoint to connect to. And it will use the interval value to know in which interval it should query the endpoint.
    Your task is to implement a solution that:

        Makes sure the configuration is fetched right after boot and saved to a file
        keeps in mind that the response from the config server might be unstable
        makes sure the second process (the data-collector) only starts after the configuration file is updated

    Remember that this should run in a headless linux system without any intervention (you can do it in a way that would run in a Raspberry Pi when you plug it into the power socket).
    """

    with open(config_path, 'r') as config_file:
        data = json.load(config_file)
        print("Config loaded: %s" % data)

    # write string to an output file
    interval = data['interval']
    while True:
        _string = get_data(data['endpoint'])
        print(_string)
        write_data(_string, output_path)
        time.sleep(interval)


if __name__ == '__main__':
    sys.exit(cli(None, False))
