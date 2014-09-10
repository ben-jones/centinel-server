#!/usr/bin/python
# Ben Jones bjones99@gatech.edu
# Georgia Tech Fall 2014 
# Centinel project
#
# verifyServer.py: unit tests for the centinel server API

import requests
import tempfile
import threading
import unittest

import server


class TestRESTAPI(unittest.TestCase):
    """Class to test our REST API"""

    @classmethod
    def setUpClass(cls):
        """Setup a fresh copy of the server for testing

        This class method will perform the following functionality
        1) create a fresh db to use (in a new file)
        2) start the server in a different thread
        3) create a user to test with
        4) create experiments to sync to the client

        """
        fp, temp_file = tempfile.mkstemp()
        fp.close()
        cls.db_file = temp_file
        db_uri = 'sqlite:///%s' % (tempFile)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        db.create_all()
        cls.server_thread = threading.Thread(target=app.run)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        """tear down some of the state created in setUpClass"""

        os.remove(cls.db_file)

    def test_recommended_version(self):
        pass

    def test_experiments(self):
        pass

    def test_results(self):
        pass

    def test_clients(self):
        pass

    def test_submit_results(self):
        pass


if __name__ == "__main__":
    unittest.main()
