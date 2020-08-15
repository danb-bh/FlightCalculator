# FlightCalculator

Work out how far you've flown


## Get the app running on your location machine

From the repo root, run the following commands:

```bash
cd src

python3 -m venv venv
. ./venv/bin/activate

python3 -m pip install --upgrade pip
pip install -r requirements.txt
```


## Using the app

From the repo root, run the following commands:

```bash
cd src
python3 main.py
```

The method `Tests.test_display_example(..)` reads the file `data/flights.txt` and calculates the total distance travelled


## Data file location and format

The source file for flight data is `data/flights.txt`. The format is CSV-ish. The columns are `from,to,repititions`, with locations specified using three-character IATA airport codes. `repetitions` is a shorthand notation to indicate multiple trips between the locations specified.

You can have sub-headings throughout the file, which are denoted by the following line starting with a `-`. Blank lines are ignored.

An example is as follows:

```csv
from,to,repetitions
-------------------
LHR,BUD
BUD,LHR
LHR,GIG
GIG,LHR
LHR,AGP,2
AGP,LHR,2

July 2018
---------
LHR,CPH
CPH,LHR
```