import unittest


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


class Tests(unittest.TestCase):

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
        path = '../examples/flights.txt'
        with open(path) as file:
            data = file.readlines()

        data = get_locations(data)
        full_names = get_full_names(data)
        for datum in full_names: print(datum)


if __name__ == '__main__':
    unittest.main()
