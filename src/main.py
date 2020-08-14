import unittest
import pandas as pd


def get_locations(data):
    current = None

    for line in data:

        trimmed = line.strip()
        if trimmed == '': continue

        elements = trimmed.split(',')
        whitespace_removed = []
        for element in elements:
            whitespace_removed.append(element.strip())

        previous = current
        current = ','.join(whitespace_removed).upper()
        if previous is None: continue

        if previous[0] != '-' and current[0] != '-':
            yield previous

    yield current


def get_full_names(data):
    found = set()
    for line in data:
        elements = line.split(',')[:2]
        for element in elements:
            if len(element) > 3 and element not in found:
                found.add(element)
                yield element


def determine_trips(data):
    trips = {}

    for line in data:
        elements = line.split(',')
        key = elements[0] + ',' + elements[1]
        times = 1 if len(elements) == 2 else int(elements[2])

        if key not in trips:
            trips[key] = times
        else:
            trips[key] += times

    return trips


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
        path = '../data/airport-codes_csv.csv'
        all_coordinates = pd.read_csv(path)
        self.assertEqual([-0.461941, 51.4706], get_coordinates(all_coordinates, 'LHR'))
        self.assertEqual([13.2877, 52.5597], get_coordinates(all_coordinates, 'TXL'))

    def test_get_coordinates_bad_airport_code(self):
        path = '../data/airport-codes_csv.csv'
        all_coordinates = pd.read_csv(path)

        with self.assertRaises(Exception) as ex:
            self.assertEqual([0, 0], get_coordinates(all_coordinates, 'XXX'))

        self.assertEqual('Unable to find airport code XXX', str(ex.exception))

    def test_determine_trips(self):
        data = [
            'LHR,AGP,2',
            'AGP,LHR,2',
            'LGW,TXL',
            'TXL,LGW',
            'LGW,TXL',
            'TXL,LGW',
            'DOH,LHR'
        ]
        expected = {
            'LHR,AGP': 2,
            'AGP,LHR': 2,
            'LGW,TXL': 2,
            'TXL,LGW': 2,
            'DOH,LHR': 1
        }
        actual = determine_trips(data)
        self.assertEqual(expected, actual)

    def test_get_full_names(self):
        data = [
            'LONDON,MALAGA,2',
            'MALAGA,LONDON,2',
            'LHR,TXL',
            'TXL,LHR']

        expected = ['LONDON', 'MALAGA']
        actual = list(get_full_names(data))
        self.assertEqual(expected, actual)

    def test_get_locations(self):
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
            'LHR,TXL',
            'TXL,LHR']

        actual = list(get_locations(data))
        self.assertEqual(expected, actual)

    def test_display_example(self):
        self.skipTest('')
        path = '../data/flights.txt'
        with open(path) as file:
            data = file.readlines()

        data = get_locations(data)
        trips = determine_trips(data)
        for trip in trips:
            print(f'{trip}: {trips[trip]}')


if __name__ == '__main__':
    unittest.main()
