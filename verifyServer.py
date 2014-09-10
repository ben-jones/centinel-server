#!/usr/bin/python
# Ben Jones bjones99@gatech.edu
# Georgia Tech Fall 2014 
# Centinel project
#
# verifyServer.py: unit tests for the centinel server API

import json
import os
import requests
import socket
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
        os.close(fp)
        cls.db_file = temp_file
        db_uri = 'sqlite:///%s' % (temp_file)
        server.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        server.db.create_all()

        cls.server_ip = "127.0.0.1"
        cls.server_port = 5000
        cls.server_url = "".join(["http://", cls.server_ip, ":",
                                  str(cls.server_port)])
        kargs = {'host': cls.server_ip, 'port': cls.server_port}
        cls.server_thread = threading.Thread(target=server.app.run,
                                             kwargs=kargs)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        """tear down some of the state created in setUpClass"""

        os.remove(cls.db_file)

    def test_not_found(self):
        r = requests.get(self.server_url + "/this-is-not/a-real-url")
        self.assertEqual(r.status_code, 404)

    def test_bad_request(self):
        pass
        # TODO: figure out why we can't connect to the socket
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.connect((self.server_ip, self.server_port))
        # sock.send("asdlfkjas;dlfjas;dlfjsa;dlfj;ladskfj\r\n\r\n")
        # received = sock.recv(2048)

    def test_unauthorized(self):
        r = requests.get(self.server_url + "/results")
        self.assertEqual(r.status_code, 401)

    def test_recommended_version(self):
        version = "1.2.3.4.5.6.7.8.9"
        server.config.recommended_version = version
        r = requests.get(self.server_url + "/version")
        content = json.loads(r.text)
        self.assertEqual(content['version'], version)

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
