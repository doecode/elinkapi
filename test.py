import unittest
from elinkapi.organization import Organization
from elinkapi.record import Record, ProductType
from elinkapi.person import Person
from elinkapi.contribution import Contribution
from datetime import date

class TestOrganizations(unittest.TestCase):
    """
    Ensure pydantic functions work properly for checking ROR IDs, other requirements, etc.
    """
    def test_ror_ids(self):
        example_rors = ["https://ror.org/024mw5h28", "015w2mp89", "http://ror.org/05h992307"]
        bad_rors = [ "nope", "0bAdone!", "https://rororg/024mw5h28" ]

        # ensure good ones work
        for ror in example_rors:
            o = Organization(type='SPONSOR', ror_id=ror)
            self.assertEqual(o.ror_id, ror, "ROR values did not match up.")

        # ensure bad ones fail
        for ror in bad_rors:
            with self.assertRaises(ValueError, msg=f"Value {ror} should fail"):
                o = Organization(type="SPONSOR", ror_id=ror)
                
class TestPerson(unittest.TestCase):
    """
    Test various conditions are validated for Persons.
    """
    def test_person_validation(self):
        # try a few good values
        types = [t.value for t in Person.Type]
        bad_types = ["NOPE", "WRONG", "not-this-either"]
        
        for type in types:
            # make sure construction works
            p = Person(type=type, last_name = "Example")

        for type in bad_types:
            # ensure these don't make it
            with self.assertRaises(ValueError, msg=f"{type} is not a valid type"):
                p = Person(type = type, last_name = "Wrong")

        # ensure only contributors may have contributing types
        contribution_types = [t.value for t in Contribution]

        # ensure all the contributor types work properly with CONTRIBUTING
        p = Person(type=Person.Type.CONTRIBUTING, last_name ="Mann")
        for type in contribution_types:
            p.contributor_type = type

class TestRecord(unittest.TestCase):
    """
    Test basic field requirements exist.
    """
    def test_record(self):
        # records REQUIRE: product type and title at least
        with self.assertRaises(ValueError, msg="Missing required fields."):
            r = Record()

        with self.assertRaises(ValueError, msg="Missing required fields."):
            r = Record(title="Not enough")

        with self.assertRaises(ValueError, msg="Missing required fields."):
            r = Record(product_type = "TR")

        # make sure at least these work
        r = Record(title="Good record", product_type=ProductType.Conference)

        # test all these work
        for type in [t.value for t in ProductType]:
            r = Record(title="Good one", product_type = type)

        bad_types = ["X", "NO", "BOGUS"]

        for type in bad_types:
            with self.assertRaises(ValueError, msg=f"Type {type} is not a valid value."):
                r = Record(title="Title is ok", product_type=type)

    """
    Test some record functionality ("publication_date")
    """
    def test_date_setting(self):
        # construct a basic Record
        r = Record(title="Example", product_type = "TR")

        # try setting a str
        r.publication_date = '2011-08-12'
        self.assertEqual(r.publication_date, date(2011, 8, 12), "Date didn't set properly")

        # try a date
        r.publication_date = date(1999, 4, 14)
        self.assertEqual(r.publication_date, date(1999, 4, 14), "date type not setting.")

        # try some failures
        bad_dates = ['9', '199', 'monday, Feb 7, 1920', "Spring"]

        for value in bad_dates:
            with self.assertRaises(ValueError, msg=f"Value {value} should fail"):
                r.publication_date = value

# Run all the unit tests above
if __name__ == '__main__':
    unittest.main()