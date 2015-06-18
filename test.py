"""Some very basic unit tests for app."""

from unittest import TestCase, main
import os


class SwitchesTestCase(TestCase):

    """A base class for all app tests."""

    def setUp(self):
        """Set up the testing database etc."""
        switches.db.create_all()
        self.db = switches.db
        self.app = switches.app.test_client()

    def tearDown(self):
        """Remove the database."""
        self.db.session.remove()
        self.db.drop_all()

    def add_switch(self, *args, **kwargs):
        """Add a Switch to self.db. Pass all args to Switch."""
        s = switches.Switch(*args, **kwargs)
        self.db.session.add(s)
        self.db.session.commit()
        return s


class TestSwitchModel(SwitchesTestCase):

    """Testing the database model."""

    def setUp(self):
        """Add a swtich to use for testing."""
        super(TestSwitchModel, self).setUp()
        self.switch = self.add_switch(slug='Bob')

    def test_Switch_to_dict(self):
        """Test the Switch.to_dict method."""
        expected = {
            'id_': 1,
            'slug': 'Bob',
            'value': False,
        }
        self.assertDictContainsSubset(expected, self.switch.to_dict())

    def test_Switch_flip(self):
        """Test the Switch.to_dict method."""
        self.assertFalse(self.switch.value)
        self.switch.flip()
        self.assertTrue(self.switch.value)

    def test_Switch_on_changed_value(self):
        """Test the Switch.on_changed_value."""
        updated = self.switch.updated
        self.switch.flip()
        self.assertGreater(self.switch.updated, updated)


class TestSwitchesApp(SwitchesTestCase):

    """Testing the flask app and the routes."""

    def test_homepage(self):
        """Go the home page with an empty database."""
        res = self.app.get('/')
        self.assertIn('No Switches', res.data)

    def test_homepage_with_switch(self):
        """Add a switch and then see if it is there."""
        self.switch = self.add_switch(slug='Bob')
        res = self.app.get('/')
        self.assertIn('Bob', res.data)

    def test_api_flip(self):
        """Test the flip api endpoint."""
        s = self.add_switch(slug='Bob')
        self.assertFalse(s.value)
        self.app.post('/api/flip/1')
        s = switches.Switch.query.get(1)
        self.assertTrue(s.value)

    def test_api_add(self):
        """Test the add api endpoint."""
        self.assertListEqual([], switches.Switch.query.all())
        self.app.post('/api/add', data={'slug': 'Jane'})
        self.assertEqual(1, len(switches.Switch.query.all()))
        s = switches.Switch.query.get(1)
        self.assertIsNotNone(s)
        self.assertEqual('Jane', s.slug)


if __name__ == '__main__':
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    os.environ['TESTING'] = 'True'
    import switches
    main()
