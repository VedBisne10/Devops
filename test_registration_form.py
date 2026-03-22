"""
Selenium Test Cases — Symbiosis Admission Registration Form
Run: python test_registration_form.py

Requirements:
  pip install selenium
  Chrome + matching ChromeDriver in PATH
"""

import unittest, os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select


def get_driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opts)


HTML_PATH = "file://" + os.path.abspath("index.html")


class TestRegistrationForm(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()
        self.driver.get(HTML_PATH)
        time.sleep(0.5)

    def tearDown(self):
        self.driver.quit()

    # -------------------------------------------------------
    # TC-01: Page title check
    # -------------------------------------------------------
    def test_01_page_title(self):
        self.assertIn("Symbiosis", self.driver.title)

    # -------------------------------------------------------
    # TC-02: All required fields are present in the DOM
    # -------------------------------------------------------
    def test_02_fields_present(self):
        d = self.driver
        self.assertTrue(d.find_element(By.ID, "fullName").is_displayed())
        self.assertTrue(d.find_element(By.ID, "emailId").is_displayed())
        self.assertTrue(d.find_element(By.ID, "password").is_displayed())
        self.assertTrue(d.find_element(By.ID, "confirmPassword").is_displayed())
        self.assertTrue(d.find_element(By.ID, "course").is_displayed())
        genders = d.find_elements(By.CSS_SELECTOR, "input[name='gender']")
        self.assertEqual(len(genders), 3)

    # -------------------------------------------------------
    # TC-03: Submit with all fields empty → errors visible
    # -------------------------------------------------------
    def test_03_empty_form_shows_errors(self):
        self.driver.find_element(By.CSS_SELECTOR, ".submit-btn").click()
        time.sleep(0.2)
        name_err = self.driver.find_element(By.ID, "nameError")
        self.assertIn("visible", name_err.get_attribute("class"))
        email_err = self.driver.find_element(By.ID, "emailError")
        self.assertIn("visible", email_err.get_attribute("class"))

    # -------------------------------------------------------
    # TC-04: Name too short (< 3 chars) triggers error
    # -------------------------------------------------------
    def test_04_name_too_short(self):
        d = self.driver
        d.find_element(By.ID, "fullName").send_keys("AB")
        d.find_element(By.CSS_SELECTOR, ".submit-btn").click()
        time.sleep(0.2)
        err = d.find_element(By.ID, "nameError")
        self.assertIn("visible", err.get_attribute("class"))

    # -------------------------------------------------------
    # TC-05: Valid name clears error
    # -------------------------------------------------------
    def test_05_valid_name_clears_error(self):
        d = self.driver
        d.find_element(By.ID, "fullName").send_keys("Priya Sharma")
        # trigger other errors first, then check name field
        d.find_element(By.CSS_SELECTOR, ".submit-btn").click()
        time.sleep(0.2)
        name_field = d.find_element(By.ID, "fullName")
        self.assertIn("success", name_field.get_attribute("class"))

    # -------------------------------------------------------
    # TC-06: Invalid email → error visible
    # -------------------------------------------------------
    def test_06_invalid_email(self):
        d = self.driver
        d.find_element(By.ID, "emailId").send_keys("notanemail")
        d.find_element(By.CSS_SELECTOR, ".submit-btn").click()
        time.sleep(0.2)
        err = d.find_element(By.ID, "emailError")
        self.assertIn("visible", err.get_attribute("class"))

    # -------------------------------------------------------
    # TC-07: Valid email clears error
    # -------------------------------------------------------
    def test_07_valid_email(self):
        d = self.driver
        d.find_element(By.ID, "emailId").send_keys("priya@example.com")
        d.find_element(By.CSS_SELECTOR, ".submit-btn").click()
        time.sleep(0.2)
        email_field = d.find_element(By.ID, "emailId")
        self.assertIn("success", email_field.get_attribute("class"))

    # -------------------------------------------------------
    # TC-08: No gender selected → error visible
    # -------------------------------------------------------
    def test_08_gender_not_selected(self):
        d = self.driver
        d.find_element(By.CSS_SELECTOR, ".submit-btn").click()
        time.sleep(0.2)
        err = d.find_element(By.ID, "genderError")
        self.assertIn("visible", err.get_attribute("class"))

    # -------------------------------------------------------
    # TC-09: Gender checkbox selection
    # -------------------------------------------------------
    def test_09_gender_checkbox(self):
        d = self.driver
        male_cb = d.find_element(By.ID, "genderMale")
        male_cb.click()
        self.assertTrue(male_cb.is_selected())
        # Check that female is NOT selected (single-select behavior)
        female_cb = d.find_element(By.ID, "genderFemale")
        self.assertFalse(female_cb.is_selected())

    # -------------------------------------------------------
    # TC-10: Only one gender can be selected at a time
    # -------------------------------------------------------
    def test_10_gender_single_select(self):
        d = self.driver
        d.find_element(By.ID, "genderMale").click()
        d.find_element(By.ID, "genderFemale").click()
        time.sleep(0.1)
        self.assertFalse(d.find_element(By.ID, "genderMale").is_selected())
        self.assertTrue(d.find_element(By.ID, "genderFemale").is_selected())

    # -------------------------------------------------------
    # TC-11: Course dropdown has options
    # -------------------------------------------------------
    def test_11_course_dropdown_options(self):
        d = self.driver
        sel = Select(d.find_element(By.ID, "course"))
        options = [o.get_attribute("value") for o in sel.options if o.get_attribute("value")]
        self.assertGreater(len(options), 3)

    # -------------------------------------------------------
    # TC-12: No course selected → error visible
    # -------------------------------------------------------
    def test_12_course_not_selected(self):
        d = self.driver
        d.find_element(By.CSS_SELECTOR, ".submit-btn").click()
        time.sleep(0.2)
        err = d.find_element(By.ID, "courseError")
        self.assertIn("visible", err.get_attribute("class"))

    # -------------------------------------------------------
    # TC-13: Password < 8 chars → error
    # -------------------------------------------------------
    def test_13_short_password(self):
        d = self.driver
        d.find_element(By.ID, "password").send_keys("abc12")
        d.find_element(By.CSS_SELECTOR, ".submit-btn").click()
        time.sleep(0.2)
        err = d.find_element(By.ID, "passwordError")
        self.assertIn("visible", err.get_attribute("class"))

    # -------------------------------------------------------
    # TC-14: Passwords do not match → error
    # -------------------------------------------------------
    def test_14_passwords_mismatch(self):
        d = self.driver
        d.find_element(By.ID, "password").send_keys("SecurePass1!")
        d.find_element(By.ID, "confirmPassword").send_keys("WrongPass99")
        d.find_element(By.CSS_SELECTOR, ".submit-btn").click()
        time.sleep(0.2)
        err = d.find_element(By.ID, "confirmPasswordError")
        self.assertIn("visible", err.get_attribute("class"))

    # -------------------------------------------------------
    # TC-15: Full valid form → success banner shown
    # -------------------------------------------------------
    def test_15_valid_form_submission(self):
        d = self.driver
        d.find_element(By.ID, "fullName").send_keys("Priya Sharma")
        d.find_element(By.ID, "emailId").send_keys("priya@example.com")
        d.find_element(By.ID, "genderFemale").click()
        Select(d.find_element(By.ID, "course")).select_by_value("mba")
        d.find_element(By.ID, "password").send_keys("SecurePass1!")
        d.find_element(By.ID, "confirmPassword").send_keys("SecurePass1!")
        d.find_element(By.CSS_SELECTOR, ".submit-btn").click()
        time.sleep(0.3)
        banner = d.find_element(By.ID, "successBanner")
        self.assertIn("visible", banner.get_attribute("class"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
