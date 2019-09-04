from unittest import TestCase

from semver import SemverThing, NotSemanticVersion


semver_correct = ['1.2.3-blah+thing', '1.2.3', '1.2.3-blah', '1.2.3+thing']

semver_wrong = ['2.3-blah', '0.0', '234235-prerelease', '425']

class TestSemverThing(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_semver_parsing(self):
        for item in semver_correct:
            sv = SemverThing(item)
            assert sv.major == '1'
            assert sv.minor == '2'
            assert sv.patch == '3'
            if sv.prerelease:
                assert sv.prerelease == 'blah'
            if sv.buildmetadata:
                assert sv.buildmetadata == 'thing'

        for item in semver_wrong:
            with self.assertRaises(NotSemanticVersion):
                sv = SemverThing(item)


