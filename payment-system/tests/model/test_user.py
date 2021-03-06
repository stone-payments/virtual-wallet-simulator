import hashlib
from unittest import TestCase

from base.connect_db import ConnectDB
from exceptions.user_exceptions import UsernameInUse
from exceptions.user_exceptions import UserInactive
from exceptions.user_exceptions import UserPasswordNotGiven
from exceptions.user_exceptions import UsernameNotGiven
from exceptions.user_exceptions import UserPasswordIncorrect
from exceptions.user_exceptions import UsernameNotFound
from model.user import User, factors


class TestUser(TestCase):

    def setUp(self):
        ConnectDB.connect_database()

        self.passwd = 'v3ry_h@rd_p@$$w0rd'
        self.user = User(name="Testing User",
                         username="test01",
                         adress="0, Dummy Street, 219875-456",
                         phone_number='+55 21 99999-999',
                         mail_address='test@test_users.com',
                         password=self.passwd)
        self.user.save()

    def test_hashed_password(self):
        """
        Password should be hashed when set
        """
        suid = str(self.user.uid)
        a, b = factors(suid, self.passwd)
        s = zip(suid * a, self.passwd * b)
        p = ''.join([''.join(_) for _ in s]).encode('utf8')
        h = hashlib.sha384(p).hexdigest()

        self.assertEqual(h, self.user.password)

    def test_creating_user_with_used_username(self):
        """
        Should raise an UsernameInUse
        exception
        """

        user2 = User(name="Testing User 02",
                     username="test01",
                     adress="0, Dummy Street, 219875-456",
                     phone_number='+55 21 99999-999',
                     mail_address='test@test_users.com',
                     password='weak password')

        with self.assertRaises(UsernameInUse):
            user2.save()

    def test_creating_user_without_password(self):
        """
        When creating user without password,
        it should block and return 'no_password_given'
        """
        user = User(name="Testing User",
                    username="test02",
                    adress="0, Dummy Street, 219875-456",
                    phone_number='+55 21 99999-999',
                    mail_address='test@test_users.com')

        with self.assertRaises(UserPasswordNotGiven):
            user.save()

    def test_creating_user_without_username(self):
        """
        When creating user without username,
        it should block and return 'no_username_given'
        """
        user = User(name="Testing User",
                    adress="0, Dummy Street, 219875-456",
                    phone_number='+55 21 99999-999',
                    mail_address='test@test_users.com',
                    password='a simple password')

        with self.assertRaises(UsernameNotGiven):
            user.save()

    def test_update_user(self):
        """
        Update user means save an user with same username,
        but once is an uptade, not a register, should proceed
        """
        # Load the already created user
        user1 = User.nodes.get_or_none(username='test01')

        # update mail address:
        user1.mail_address = 'user1@mail_adress.com'

        # Try saving:
        result = user1.save()

        # Test if result is None (it is, if saving failed)
        self.assertIsNotNone(result)
        # Load again and test if e-mail was changed
        user2 = User.nodes.get_or_none(username='test01')
        self.assertEqual(user2.mail_address, 'user1@mail_adress.com')

    def test_login_with_correct_password(self):
        """
        If user can access should return the
        user object
        """
        result = User.login('test01', self.passwd)
        self.assertEqual('test01', result.username)

    def test_login_incorrect_password(self):
        """
        If user can't access should return false
        """
        with self.assertRaises(UserPasswordIncorrect):
            User.login('test01', 'incorrect password')

    def test_login_inactive_user(self):
        """
        Should raise exception during login
        if user is inactive and password correct
        """
        # Turn user to inactive for testing purposes
        self.user.active = False
        self.user.save()

        with self.assertRaises(UserInactive):
            User.login('test01', self.passwd)

        # Turn user active again
        self.user.active = True
        self.user.save()

    def test_login_inexistent_user(self):
        """
        Should return 'inexistent' if username not found
        """
        with self.assertRaises(UsernameNotFound):
            User.login('not_found_username', self.passwd)

    def tearDown(self):
        if self.user.save() is not None:
            self.user.delete()

