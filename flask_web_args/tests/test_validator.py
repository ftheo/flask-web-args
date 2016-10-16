from unittest import TestCase

import flask_web_args.validate_wrapper as validate_wrapper
import flask_web_args.validator as validator


class TestValidator(TestCase):

    def test_fails_on_invalid_init(self):
        validate_wrapper.error_handler_func = lambda name, value, error_msg: None
        self.assertRaises(AssertionError, lambda: validator.Validator())
        self.assertRaises(AssertionError, lambda: validator.Validator(valid="foo"))
        self.assertRaises(AssertionError, lambda: validator.Validator(arg_type="foo"))  # Has to be of VALID_TYPES

    def test_valid_init(self):
        validate_wrapper.error_handler_func = lambda name, value, error_msg: None
        self.assertTrue(validator.Validator(arg_type=int))
        self.assertTrue(validator.Validator(default=5))
        self.assertTrue(validator.Validator(default=["foo"]))
        self.assertTrue(validator.Validator(valid_value=lambda x: None))
