import unittest
import pandas as pd

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

    return trips.values()


def get_coordinates(all_coordinates, airport):
    df = all_coordinates.loc[all_coordinates['iata_code'] == airport]
    if len(df) == 0: raise Exception(f'Unable to find airport code {airport}')

    row = df.iloc[0]
    coordinates = row['coordinates'].split(', ')
    return [
        float(coordinates[0]),
        float(coordinates[1])
    ]


class Tests(unittest.TestCase):

    def test_get_coordinates(self):
        all_coordinates = pd.read_csv(path_to_all_coordinates_csv)
        self.assertEqual([-0.461941, 51.4706], get_coordinates(all_coordinates, 'LHR'))
        self.assertEqual([13.2877, 52.5597], get_coordinates(all_coordinates, 'TXL'))

    def test_get_coordinates_bad_airport_code(self):
        all_coordinates = pd.read_csv(path_to_all_coordinates_csv)

        with self.assertRaises(Exception) as ex:
            self.assertEqual([0, 0], get_coordinates(all_coordinates, 'XXX'))

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
        self.skipTest('')

        with open(path_to_flights) as file:
            data = file.readlines()

        all_coordinates = pd.read_csv(path_to_all_coordinates_csv)

        data = get_trips(data)
        trips = combine_trips(data)
        for trip in trips:
            airports = trip.split(',')
            depart = get_coordinates(all_coordinates, airports[0])
            arrive = get_coordinates(all_coordinates, airports[1])


if __name__ == '__main__':
    unittest.main()
