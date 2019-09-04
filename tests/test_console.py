from unittest import TestCase

from semver.console import compare_versions


# fixtures
EXPECT_BEFORE = [('2.3.4', '3.3.4'),
                 ('2.3.4', '2.4.4'),
                 ('0.0.0+test', '0.0.1+test'),
                 ('2.3.4-alpha', '2.3.4'),
                 ('2.3.4', '2.3.5'),
                 ('2.3.4-alpha', '2.3.4-beta'),
                ]

EXPECT_AFTER = [('3.3.4', '2.3.4'),
                ('2.4.4', '2.3.4'),
                ('0.0.1+test', '0.0.0+test'),
                ('2.3.4', '2.3.4-alpha'),
                ('2.3.5', '2.3.4'),
                ('2.3.4-beta', '2.3.4-alpha')
               ]

EXPECT_EQUAL = [('1.2.3', '1.2.3'),
                ('1.2.3+test', '1.2.3'),
                ('1.2.3+thing1', '1.2.3+thing2')
               ]

EXPECT_INVALID = [('1.1.2', '1.1'),
                  ('1.3.1', None),
                  ('0.1-alpha', '0.1.1-alpha'),
                  ('1.2+test', '1.2.3'),
                  (None, None),
                  (1.23, 10.2),
                 ]

class TestSemverConsole(TestCase):

    def test_compare_versions_expecting_before(self):
        for pair in EXPECT_BEFORE:
            assert compare_versions(*pair) == 'before'

    def test_compare_versions_expecting_after(self):
        for pair in EXPECT_AFTER:
            assert compare_versions(*pair) == 'after'

    def test_compare_versions_expecting_equal(self):
        for pair in EXPECT_EQUAL:
            assert compare_versions(*pair) == 'equal'

    def test_compare_versions_expecting_invalid(self):
        for pair in EXPECT_INVALID:
            print(pair)
            assert compare_versions(*pair) == 'invalid'


