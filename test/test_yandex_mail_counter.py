import unittest
import allure
from selenium import webdriver
from project.helpers.page import MailPage, MainPage, MailLoginPage


@allure.epic("mail.yandex.ru")
class TestMailsCount(unittest.TestCase):
    @allure.feature("Почта Яндекса")
    @allure.story("Проверка наличия писем с обозначенными темами.")
    @allure.tag("Шевадров")
    @allure.severity(allure.severity_level.CRITICAL)
    def setUp(self):
        """Локально поднял Selenium GRID"""
        self.driver = self.driver = webdriver.Remote(
            command_executor='http://192.168.0.102:5555/wd/hub',
            desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True})

    def test_yandex_mail_counter(self, login='sdettest', password='sdet3008', subject='Simbirsoft Тестовое задание',
                                 second_subject='Simbirsoft Тестовое задание. Шевадров'):
        driver = self.driver
        driver.get('https://yandex.ru')

        open_mail = MainPage(driver)
        authorization = MailLoginPage(driver)
        mail_page = MailPage(driver)

        window_before = driver.window_handles[0]
        open_mail.click_mail_button()
        window_after = driver.window_handles[1]

        authorization.close_first_window(window_before, window_after)
        authorization.account_authorization(login, password)

        mails_count_by_subject = mail_page.mails_count_by_subject(subject)  # Считает почту с темой из тестового
        try:
            mails_count_by_second_subject = mail_page.mails_count_by_subject(second_subject)  # Считает почту с второй темой из тестового
        except Exception:
            mails_count_by_second_subject = 0
        mails_sum = mails_count_by_subject + mails_count_by_second_subject
        mail_page.send_mail_action(mails_count_by_subject, mails_sum)

        driver.refresh()

        mails_final_count = mail_page.sum_of_mails()

        self.assertEqual(mails_final_count, mails_sum + 1)  # Простой ассерт на добавление письма в ящик

    def tearDown(self):
        self.driver.quit()
