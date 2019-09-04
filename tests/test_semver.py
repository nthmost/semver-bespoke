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
        "Testing that various formats of Semantic Version strings parse correctly."
        for item in semver_correct:
            sv = SemverThing(item)
            assert sv.major == '1'
            assert sv.minor == '2'
            assert sv.patch == '3'
            if sv.prerelease:
                assert sv.prerelease == 'blah'
            if sv.buildmetadata:
                assert sv.buildmetadata == 'thing'

    def test_semver_bad_strings(self):
        "Testing that various badly-constructed version strings raise NotSemanticVersion exception."
        for item in semver_wrong:
            with self.assertRaises(NotSemanticVersion):
                sv = SemverThing(item)

    def test_semver_cmp_operators(self):
        "Testing that operator overloading on SemverThing object work as expected (>, <, ==, !=, etc)"

        sv_lowest = SemverThing('0.0.1')
        sv_highest = SemverThing('10.10.10')
        sv_mid1 = SemverThing('2.4.6')
        sv_mid2 = SemverThing('2.6.6')
        sv_mid3 = SemverThing('2.6.7')

        # comparison on major versions
        assert sv_lowest < sv_highest
        assert sv_highest > sv_lowest
        self.assertFalse(sv_lowest > sv_highest)
        assert sv_lowest <= sv_highest 
        assert sv_lowest != sv_highest
        assert sv_highest >= sv_lowest
        self.assertFalse(sv_lowest >= sv_highest)
        self.assertFalse(sv_lowest == sv_highest)

        #comparison on minor versions
        assert sv_mid1 != sv_mid2
        assert sv_mid1 < sv_mid2
        assert sv_mid2 > sv_mid1
        assert sv_mid1 <= sv_mid2
        assert sv_mid2 >= sv_mid1
        self.assertFalse(sv_mid1 == sv_mid2)

        #comparison on patch versions
        assert sv_mid2 != sv_mid3
        assert sv_mid2 < sv_mid3
        assert sv_mid3 > sv_mid2
        assert sv_mid2 <= sv_mid3
        assert sv_mid3 >= sv_mid2
        self.assertFalse(sv_mid2 == sv_mid3)

        #TODO comparison on build and prerelease


