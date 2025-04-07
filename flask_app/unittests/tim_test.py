import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from app import app, db, User

class TestSignup(unittest.TestCase):

    def setUp(self):
        """Set up the test client and application context"""
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

    @patch('app.User.query.filter_by')
    @patch('app.db.session.add')
    @patch('app.db.session.commit')
    @patch('app.hash_password', return_value='hashed_password')
    @patch('app.is_valid_email', return_value=True)
    @patch('app.check_password_requirements', return_value=True)
    @patch('app.check_default_values', return_value=False)
    def test_successful_signup(
        self, mock_check_defaults, mock_check_password, mock_valid_email,
        mock_hash_password, mock_db_commit, mock_db_add, mock_user_query
    ):
        mock_user_query.return_value.first.return_value = None

        data = {
            'username': 'anotheruser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@gmail.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'account_type': 'student'
        }

        response = self.app.post('/signup', data=data, follow_redirects=True)

        self.assertIn(response.status_code, [200, 302])
        mock_db_add.assert_called_once()
        mock_db_commit.assert_called_once()

    @patch('app.is_valid_email', return_value=False)
    @patch('app.render_template')
    def test_invalid_email(self, mock_render_template, mock_valid_email):
        """Test signup fails due to an invalid email"""
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'account_type': 'student'
        }

        response = self.app.post('/signup', data=data)
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_with('account/signup.html', is_homepage=True)

    @patch('app.render_template')
    def test_password_mismatch(self, mock_render_template):
        """Test signup fails when passwords do not match"""
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'DifferentPass!',
            'account_type': 'student'
        }

        response = self.app.post('/signup', data=data)
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_with('account/signup.html')

if __name__ == '__main__':
    unittest.main()
