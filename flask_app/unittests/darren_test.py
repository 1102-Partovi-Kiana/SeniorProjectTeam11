import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from app import app

class TestRunCode(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.env', MagicMock())
    @patch('app.analyze_robotics_code', return_value=[])
    def test_valid_code_submission(self, mock_analyze_robotics_code):
        data = {
            'code': 'print("Hello, World!")',
            'context': 'Fetch Pick and Place'
        }
        response = self.app.post('/run-code', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Code executed successfully.')
        self.assertIsNone(response_data['error'])
        self.assertEqual(response_data['static_issues'], [])
        self.assertEqual(response_data['context'], 'Fetch Pick and Place')

if __name__ == '__main__':
    unittest.main()