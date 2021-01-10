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


def verify_or_create_output(file_path, data):
    """
    Verifies that the output file exists or creates it.
    Writes a start-up msg in the log.

    :param file_path:
    :return:
    """
    try:
        with open(file_path, 'x') as file:
            msg = ("%s ### Session initiated ###\n"
                   " Output path: %s\n"
                   " ID: %s\n"
                   " Endpoint: %s\n"
                   " Interval: %s\n") % (time.asctime(time.localtime(time.time())),
                                         file_path,
                                         data['id'],
                                         data['endpoint'],
                                         data['interval'])
            file.write(msg)
    except FileExistsError:
        with open(file_path, 'a') as file:
            msg = ("%s ### Session continued after restart ###\n"
                   " ID: %s\n"
                   " Endpoint: %s\n"
                   " Interval: %s\n") % (time.asctime(time.localtime(time.time())),
                                         data['id'],
                                         data['endpoint'],
                                         data['interval'])
            file.write(msg)


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
    Fetches the data located at the specified url and returns it as a string

    :param url_path:
    :return:
    """
    try:
        with urllib.request.urlopen(url_path) as _url:
            _string = _url.read().decode()
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
    Fetches data from a location specified in a config file and outputs it in to a
    txt document at specified location.
    :param config_path:
    :param output_path:
    :return:
    """

    with open(config_path, 'r') as config_file:
        data = json.load(config_file)
        print("Config loaded: %s" % data)

    verify_or_create_output(output_path, data)
    # write string to an output file
    while True:
        _string = get_data(data['endpoint'])
        print(_string)
        write_data(_string, output_path)
        time.sleep(data['interval'])


if __name__ == '__main__':
    sys.exit(cli(None, False))
