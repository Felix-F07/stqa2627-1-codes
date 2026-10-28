
"""
Test Cases TestAccountModel
"""
import json
from random import randrange
from unittest import TestCase
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}


class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """Connect to database and load test data once before all tests"""
        db.create_all()

        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnect from database after running all tests"""
        db.session.remove()

    def setUp(self):
        """Reset table and select random data sample"""
        db.session.query(Account).delete()
        self.rand = randrange(0, len(ACCOUNT_DATA))

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_repr(self):
        """Test the representation of an account"""
        account = Account()
        account.name = "Foo"
        self.assertEqual(str(account), "<Account 'Foo'>")

    def test_create_account(self):
        """Test create an account"""
        account = Account(**ACCOUNT_DATA[0])
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_create_all_accounts(self):
        """Test create all accounts"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))

    def test_to_dict(self):
        """Test account to dict"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        result = account.to_dict()

        self.assertEqual(account.name, result["name"])
        self.assertEqual(account.email, result["email"])
        self.assertEqual(account.phone_number, result["phone_number"])
        self.assertEqual(account.disabled, result["disabled"])
        self.assertEqual(account.date_joined, result["date_joined"])

    def test_from_dict(self):
        """Test account from dict"""
        data = ACCOUNT_DATA[self.rand]
        account = Account()
        account.from_dict(data)

        self.assertEqual(account.name, data["name"])
        self.assertEqual(account.email, data["email"])
        self.assertEqual(account.phone_number, data["phone_number"])
        self.assertEqual(account.disabled, data["disabled"])

    def test_update_an_account(self):
        """Test Account update using known data"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        account.create()

        self.assertIsNotNone(account.id)

        account.name = "Changed Name"
        account.update()

        found = Account.find(account.id)
        self.assertEqual(found.name, account.name)

    def test_invalid_id_on_update(self):
        """Test invalid ID update"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        account.id = None

        self.assertRaises(DataValidationError, account.update)

    def test_delete_an_account(self):
        """Test Account deletion"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        account.create()

        self.assertEqual(len(Account.all()), 1)

        account.delete()

        self.assertEqual(len(Account.all()), 0)
