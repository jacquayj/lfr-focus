# README

## Install Python3 via Homebrew

https://docs.python-guide.org/starting/install3/osx/

## Create Virtual Environment

Open terminal into the repository folder

Create and enter the virtual environment
```
$ python3 -v venv .venv
$ source .venv/bin/activate
```

## Install dependencies

```
$ pip install requests
$ pip install python-dateutil
```

## Execute Program

```
$ cd trip-roster-report
$ python3 main.py {put your api key here}
```

Check the output file called report.csv!