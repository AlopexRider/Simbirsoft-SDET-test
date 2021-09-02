import unittest
import allure
from selenium import webdriver
from project.helpers.page import MailPage, HomePage, MailAuthorizationPage


@allure.epic("mail.yandex.ru")
class TestMailsCount(unittest.TestCase):
    @allure.feature("Почта Яндекса")
    @allure.story("Проверка наличия писем с обозначенными темами.")
    @allure.tag("Шевадров")
    @allure.severity(allure.severity_level.CRITICAL)
    def setUp(self):
        self.driver = webdriver.Chrome('D:/WebDriver/chromedriver.exe')

    def test_yandex_mail_counter(self, login="sdettest", password="sdet3008", subject="Simbirsoft Тестовое задание",
                                 second_subject="Simbirsoft Тестовое задание. Шевадров"):
        driver = self.driver
        driver.get("https://yandex.ru")

        open_homepage = HomePage(driver)
        authorization_page = MailAuthorizationPage(driver)
        mail_page = MailPage(driver)

        open_homepage.click_mail_button()
        authorization_page.account_authorization(login, password)
        mails_count_by_subject = mail_page.mails_counter_by_subject(subject)
        mails_count_by_second_subject = mail_page.mails_counter_by_second_subject(second_subject)
        mails_sum = mails_count_by_subject + mails_count_by_second_subject
        mail_page.send_mail_action(mails_count_by_subject, mails_sum)
        mails_final_count = mail_page.sum_of_mails()

        self.assertEqual(mails_final_count, mails_sum + 1)

    def tearDown(self):
        self.driver.quit()
