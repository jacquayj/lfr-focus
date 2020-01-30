# README

## Install Python3 via Homebrew

https://docs.python-guide.org/starting/install3/osx/

## Create Virtual Environment

Open terminal into the repository folder

Create the virtual environment
```
$ python3 -m venv .venv
```
Enter the virtual environment (to pull fresh report start here if starting new session in terminal) 
```
$ source .venv/bin/activate
```

## Install dependencies - initial set up only

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