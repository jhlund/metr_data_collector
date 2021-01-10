## Data collector CLI tool

The data collector fetches data from a server and appends the data
to an output file. A config file is used to specify data fetch interval
and server url.

### Installation
It is recommended to install the tool in a virtual environment using  
`pip install git+https://github.com/jhlund/metr_data_collector.git`  
or  
`pip install /path/to/metr_data_collector/ .`

### Config file
The config file contains a number of  entries.
1. "id": Unit identification
2. "endpoint": The url to the data server
3. "Interval": The time between each data fetch

```
{
    "id": "AC67DD",
    "endpoint": "http://numbersapi.com/random/trivia",
    "interval": 48
}
```
### CLI help output


---
>metr_data_collector --help
```
Usage: metr_data_collector [OPTIONS] COMMAND [ARGS]...

  CLI tool that reads a config file and collects data from a specified url
  at a specified interval.

Options:  
  --debug / --no-debug  
  --version             Show the version and exit.  
  --help                Show this message and exit.  

Commands:  
  collect-data  Fetches data from a location specified in a config file and...
```
---

>metr_data_collector collect-data --help 
```
Usage: metr_data_collector collect-data [OPTIONS]

  Fetches data from a location specified in a config file and outputs it in
  to a txt document at specified location.  

  :param config_path:  
  :param output_path:  
  :return:

Options:  
  -C, --config_path TEXT  path to local config file  [required]  
  -O, --output_path TEXT  path to the output file  [required]  
  --help                  Show this message and exit.
```
---
