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
        # create a fresh db
        fp, temp_file = tempfile.mkstemp()
        os.close(fp)
        cls.db_file = temp_file
        db_uri = 'sqlite:///%s' % (temp_file)
        server.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        server.db.create_all()

        # setup the server
        cls.server_ip = "127.0.0.1"
        cls.server_port = 5000
        cls.server_url = "".join(["http://", cls.server_ip, ":",
                                  str(cls.server_port)])
        kargs = {'host': cls.server_ip, 'port': cls.server_port}
        cls.server_thread = threading.Thread(target=server.app.run,
                                             kwargs=kargs)
        cls.server_thread.daemon = True
        cls.server_thread.start()

        # specify the user we will test with even though we don't
        # actually create the user here
        cls.username = "testy"
        cls.password = "testy"
        cls.auth = (cls.username, cls.password)

        # create directories to store the testing experiments,
        # results, etc.
        cls.home_dir = os.path.abspath("test")
        server.config.centinel_home = cls.home_dir
        cls.experiments_dir = os.path.join(cls.home_dir, "experiments")
        cls.client_experiments_dir = os.path.join(cls.experiments_dir,
                                                  cls.username)
        server.config.experiments_dir = cls.experiments_dir
        cls.results_dir = os.path.join(cls.home_dir, "results")
        cls.client_results_dir = os.path.join(cls.results_dir,
                                                  cls.username)
        server.config.results_dir = cls.results_dir
        cls.log_dir = os.path.join(cls.home_dir, "logs")
        cls.client_log_dir = os.path.join(cls.log_dir,
                                          cls.username)
        server.config.log_dir = cls.log_dir
        dirs = [cls.home_dir, cls.experiments_dir,
                cls.results_dir, cls.log_dir]
        for directory in dirs:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # create a user to test with 
        # Note: the fact that this username and password is crap says
        # nothing about the security of our system because the client
        # generates these as 64 character, cryptographically random
        # values
        payload = {'username': cls.username, 'password': cls.password}
        headers = {'content-type': 'application/json'}
        r = requests.post(cls.server_url + "/register",
                          data=json.dumps(payload), headers=headers)
        r.raise_for_status()

    @classmethod
    def tearDownClass(cls):
        """tear down some of the state created in setUpClass"""

        os.remove(cls.db_file)

    def get_request(self, path, payload, headers, auth):
        r = requests.get(self.server_url + path, headers=headers,
                         payload=json.dumps(payload), auth=auth)
        r.raise_for_status()
        return r.content
    
    def post_request(self, path, payload, headers):
        r = requests.post(self.server_url + path, headers=headers,
                          payload=json.dumps(payload), auth=auth)
        r.raise_for_status()

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

    def test_submit_result(self):
        fp, temp_file = tempfile.mkstemp()
        fp = os.fdopen(fp)
        testStringy = "".join(["this is a test\n",
                               json.dumps({'hello':5, 'test':6})])
        fp.write(testStringy)
        fp.close()
        files = {'result': temp_file}
        r = requests.post(self.server_url, files=files, auth=self.auth)
        r.raise_for_status()

        res_file = os.path.join(self.client_results_dir,
                                os.path.split(temp_file)[-1])
        self.assertTrue(os.path.exists(res_file))
        with open(res_file, 'r') as f:
            self.assertEqual(f.read(), testStringy)

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
