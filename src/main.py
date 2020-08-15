import unittest

import pandas as pd
from geopy.distance import distance

path_to_all_coordinates_csv = '../data/airport-codes_csv.csv'
path_to_flights = '../data/flights.txt'


class Location:

    def __init__(self, code: str):
        self.code = code.strip().upper()
        self.name = ''
        self.latitude = 0.0
        self.longitude = 0.0

    def __eq__(self, other):
        return self.code == other.code

    def __hash__(self):
        return hash(self.code)

    def __str__(self):
        return self.code

    def __repr__(self):
        return f'{self.code} is at {self.latitude}, {self.longitude} ({self.name})'


class Trip:

    def __init__(self, depart: Location, arrive: Location, repetitions=1):
        self.depart = depart
        self.arrive = arrive
        self.repetitions = repetitions
        self.distance = 0.0

    def __eq__(self, other):
        return self.arrive == other.arrive and self.depart == other.depart

    def __hash__(self):
        return hash((self.depart, self.arrive))

    def __str__(self):
        return f'{self.depart},{self.arrive},{self.repetitions}'

    def __repr__(self):
        return f'From {self.depart} to {self.arrive} is {self.distance} km, {self.repetitions} ' \
               f'time{"" if self.repetitions == 1 else "s"} '


def get_trips(data):
    current = None

    def create_trip(datum):
        elements = datum.split(',')
        depart = Location(elements[0])
        arrive = Location(elements[1])
        repetitions = 1 if len(elements) == 2 else int(elements[2])
        return Trip(depart, arrive, repetitions)

    for line in data:

        trimmed = line.strip()
        if trimmed == '': continue

        previous = current
        current = trimmed
        if previous is None: continue

        if previous[0] != '-' and current[0] != '-':
            yield create_trip(previous)

    yield create_trip(current)


def combine_trips(data):
    trips = {}

    for trip in data:
        if trip not in trips:
            trips[trip] = trip
        else:
            trips[trip].repetitions += trip.repetitions

    return [trip for trip in trips.values()]


def populate_location_details(all_coordinates: pd.DataFrame, location: Location):
    code = location.code
    df = all_coordinates.loc[all_coordinates['iata_code'] == code]
    if len(df) == 0: raise Exception(f'Unable to find airport code {code}')

    row = df.iloc[0]
    location.name = row['name']

    coordinates = row['coordinates'].split(', ')
    location.longitude = float(coordinates[0])
    location.latitude = float(coordinates[1])


def determine_distance(trip: Trip):
    depart = [trip.depart.latitude, trip.depart.longitude]
    arrive = [trip.arrive.latitude, trip.arrive.longitude]

    try:
        trip.distance = distance(depart, arrive).km
    except Exception:
        print(f'Error processing {trip}: {depart} to {arrive}')
        raise


def populate_trip_details(all_coordinate: pd.DataFrame, trip: Trip):
    populate_location_details(all_coordinate, trip.depart)
    populate_location_details(all_coordinate, trip.arrive)
    determine_distance(trip)


class Tests(unittest.TestCase):

    def test_get_coordinates(self):
        all_coordinates = pd.read_csv(path_to_all_coordinates_csv)

        lhr = Location('LHR')
        populate_location_details(all_coordinates, lhr)
        self.assertEqual('London Heathrow Airport', lhr.name)
        self.assertEqual(51.4706, lhr.latitude)
        self.assertEqual(-0.461941, lhr.longitude)

        txl = Location('TXL')
        populate_location_details(all_coordinates, txl)
        self.assertEqual('Berlin-Tegel Airport', txl.name)
        self.assertEqual(52.5597, txl.latitude)
        self.assertEqual(13.2877, txl.longitude)

    def test_get_coordinates_bad_airport_code(self):
        all_coordinates = pd.read_csv(path_to_all_coordinates_csv)

        with self.assertRaises(Exception) as ex:
            self.assertEqual([0, 0], populate_location_details(all_coordinates, Location('XXX')))

        self.assertEqual('Unable to find airport code XXX', str(ex.exception))

    def test_combine_trips(self):
        data = [
            'LHR,AGP,2',
            'AGP,LHR,2',
            'LGW,TXL',
            'TXL,LGW',
            'LGW,TXL',
            'TXL,LGW',
            'DOH,LHR'
        ]
        expected = [
            'LHR,AGP,2',
            'AGP,LHR,2',
            'LGW,TXL,2',
            'TXL,LGW,2',
            'DOH,LHR,1'
        ]

        all_trips = get_trips(data)
        actual = [str(trip) for trip in combine_trips(all_trips)]

        self.assertEqual(expected, actual)

    def test_get_trips(self):
        data = [
            'from,to,repetitions',
            '---',
            '',
            ' LHR , AGP , 2 ',
            'AGP,LHR,2',
            '',
            'July 2019',
            '---',
            'LHR,TXL',
            'TXL,LHR']

        expected = [
            'LHR,AGP,2',
            'AGP,LHR,2',
            'LHR,TXL,1',
            'TXL,LHR,1']

        actual = [str(trip) for trip in get_trips(data)]
        self.assertEqual(expected, actual)

    def test_display_example(self):

        with open(path_to_flights) as file:
            data = file.readlines()

        all_coordinates = pd.read_csv(path_to_all_coordinates_csv)
        trips = combine_trips(get_trips(data))

        for trip in trips:
            populate_trip_details(all_coordinates, trip)

        km = sum(trip.distance for trip in trips)
        miles = km / 1.6093
        print(f'Total distance travelled is {km:,.0f} km, or {miles:,.0f} miles')


if __name__ == '__main__':
    unittest.main()
