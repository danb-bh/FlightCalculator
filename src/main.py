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


def find_full_names(data):
    found = set()
    for line in data:
        elements = line.split(',')[:2]
        for element in elements:
            if len(element) > 3 and element not in found:
                found.add(element)
                yield element


class Tests(unittest.TestCase):

    def test_find_full_names(self):
        data = [
            'LONDON,MALAGA,2',
            'MALAGA,LONDON,2',
            'LHR,TXL',
            'TXL,LHR']

        expected = ['LONDON', 'MALAGA']
        actual = list(find_full_names(data))
        self.assertEqual(expected, actual)

    def test_get_locations(self):
        data = [
            'from,to,repetitions',
            '---',
            '',
            'london , malaga , 2 ',
            'malaga,london,2',
            '',
            'July 2019',
            '---',
            'LHR,TXL',
            'TXL,LHR']

        expected = [
            'LONDON,MALAGA,2',
            'MALAGA,LONDON,2',
            'LHR,TXL',
            'TXL,LHR']

        actual = list(get_locations(data))
        self.assertEqual(expected, actual)

    def test_display_example(self):
        # self.skipTest('')
        path = '../examples/flights.txt'
        with open(path) as file:
            data = file.readlines()

        data = get_locations(data)
        full_names = find_full_names(data)
        for datum in full_names: print(datum)


if __name__ == '__main__':
    unittest.main()
