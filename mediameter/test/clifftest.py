import unittest, ConfigParser, json
import mediameter.cliff

GEONAME_LONDON_UK = 2643743
GEONAME_LONDERRY_NH = 5088905

class CliffTest(unittest.TestCase):
    '''
    A basic set of test cases to make sure the API can pull from the server correctly.
    '''

    def setUp(self):
        self._config = ConfigParser.ConfigParser()
        self._config.read('settings.config')
        self._cliff = mediameter.cliff.Cliff(self._config.get('cliff', 'host'), self._config.get('cliff', 'port'))

    def testParseText(self):
        results = self._cliff.parseText("This is about Einstien at the IIT in New Delhi.")['results']
        self.assertEqual(len(results['organizations']), 1)
        self.assertEqual(len(results['places']['mentions']), 1)
        self.assertEqual(results['places']['mentions'][0]['id'], 1261481)
        self.assertEqual(len(results['people']), 1)

    def testGeonamesLookup(self):
        results = self._cliff.geonamesLookup(4943351)
        self.assertEqual(results['id'], 4943351)
        self.assertEqual(results['lon'], -71.09172)
        self.assertEqual(results['lat'], 42.35954)
        self.assertEqual(results['name'], "Massachusetts Institute of Technology")
        self.assertEqual(results['parent']['name'], "Middlesex County")
        self.assertEqual(results['parent']['parent']['name'], "Massachusetts")

    def testLocalReplacements(self):
        replacements = {
            'Londonderry': 'London',
        }
        # make sure non-replaced fetches the city in the UK
        results = self._cliff.parseText("This is about London.")['results']
        mention = results['places']['mentions'][0]
        self.assertEqual(GEONAME_LONDON_UK, mention['id'])
        # now see if it gets the city with replacements
        replacing_cliff = mediameter.cliff.Cliff(self._config.get('cliff', 'host'),
                                                 self._config.get('cliff', 'port'), replacements)
        results = replacing_cliff.parseText("This is about London.")['results']
        replaced_mention = results['places']['mentions'][0]
        self.assertEqual(GEONAME_LONDERRY_NH, replaced_mention['id'])
