import unittest

from src import registrator


class TestRegistrator(unittest.TestCase):

    # --- Регистрация ---

    def test_empty_login_rejected(self):
        result = registrator.register_user(
            "",
            "НадёжныйПароль22!",
            "НадёжныйПароль22!"
        )

        self.assertEqual(
            result,
            (False, "Логин не может быть пустым")
        )

    def test_blacklisted_login_rejected(self):
        result = registrator.register_user(
            "root",
            "НадёжныйПароль22!",
            "НадёжныйПароль22!"
        )

        self.assertEqual(
            result,
            (False, "Логин запрещен")
        )

    def test_too_short_login_rejected(self):
        result = registrator.register_user(
            "a",
            "НадёжныйПароль22!",
            "НадёжныйПароль22!"
        )

        self.assertEqual(
            result,
            (False, "Некорректный формат логина")
        )

    def test_weak_password_rejected(self):
        result = registrator.register_user(
            "stasik",
            "qqqq",
            "qqqq"
        )

        self.assertEqual(
            result,
            (False, "Пароль не соответствует требованиям")
        )

    def test_password_mismatch_rejected(self):
        result = registrator.register_user(
            "ivan123",
            "НадёжныйПароль22!",
            "НадёжныйПароль33!"
        )

        self.assertEqual(
            result,
            (False, "Пароли не совпадают")
        )

    def test_registration_succeeds_with_valid_data(self):
        result = registrator.register_user(
            "stasik",
            "НадёжныйПароль22!",
            "НадёжныйПароль22!"
        )

        self.assertEqual(
            result,
            (True, "")
        )

    # --- Почта ---

    def test_email_standard_form_accepted(self):
        self.assertTrue(
            registrator.is_valid_email("ivan@yandex.ru")
        )

    def test_email_with_digits_accepted(self):
        self.assertTrue(
            registrator.is_valid_email("ivan2024@yandex.ru")
        )

    def test_email_without_zone_rejected(self):
        self.assertFalse(
            registrator.is_valid_email("ivan@yandex")
        )

    def test_email_without_at_sign_rejected(self):
        self.assertFalse(
            registrator.is_valid_email("ivanyandex.ru")
        )

    # --- Телефон ---

    def test_phone_international_format_accepted(self):
        self.assertTrue(
            registrator.is_valid_phone("+7-999-888-7766")
        )

    def test_phone_without_plus_rejected(self):
        self.assertFalse(
            registrator.is_valid_phone("7-999-888-7766")
        )

    def test_phone_incomplete_digits_rejected(self):
        self.assertFalse(
            registrator.is_valid_phone("+7-999-888-776")
        )

    # --- Логин ---

    def test_username_latin_accepted(self):
        self.assertTrue(
            registrator.is_valid_username("stasik")
        )

    def test_username_with_digits_accepted(self):
        self.assertTrue(
            registrator.is_valid_username("stas777")
        )

    def test_username_with_underscore_accepted(self):
        self.assertTrue(
            registrator.is_valid_username("stas_777")
        )

    def test_username_below_min_length_rejected(self):
        self.assertFalse(
            registrator.is_valid_username("abc")
        )

    def test_username_with_special_chars_rejected(self):
        self.assertFalse(
            registrator.is_valid_username("abcde!@#$@$")
        )

    def test_username_cyrillic_rejected(self):
        self.assertFalse(
            registrator.is_valid_username("котик")
        )

    # --- Пароль ---

    def test_password_strong_cyrillic_accepted(self):
        self.assertTrue(
            registrator.is_valid_password("НадёжныйПароль22!")
        )

    def test_password_too_short_rejected(self):
        self.assertFalse(
            registrator.is_valid_password("ааа")
        )

    def test_password_with_latin_rejected(self):
        self.assertFalse(
            registrator.is_valid_password("НадёжныйПароль22!qq")
        )

    def test_password_without_uppercase_rejected(self):
        self.assertFalse(
            registrator.is_valid_password("надёжныйпароль22!")
        )

    def test_password_without_lowercase_rejected(self):
        self.assertFalse(
            registrator.is_valid_password("НАДЁЖНЫЙПАРОЛЬ22!")
        )

    def test_password_without_digit_rejected(self):
        self.assertFalse(
            registrator.is_valid_password("НадёжныйПароль!")
        )

    def test_password_without_special_char_rejected(self):
        self.assertFalse(
            registrator.is_valid_password("НадёжныйПароль22")
        )


if __name__ == "__main__":
    unittest.main()