import unittest
import requests


""" This Test will test the code is running perfectly or not
    Send a request to the login route
    Check that the response status code is 200
    Check that the response body is correct
"""
class TestAPI(unittest.TestCase):
    def test_login(self):
      response = requests.get("http://127.0.0.1:5000/login", auth=("john", "password123"))
      try:          
          self.assertEqual(response.status_code, 200)
      except Exception as e:
           return e, 500
  
      try:            
          self.assertEqual(response.text, "You are authenticated!"), 200    
      except Exception as e:
            return e, 500



if __name__ == "__main__":
    unittest.main()
