from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


class NoMailsWithSubjectFound:
    """Sometimes there's no e-mails found on a page"""
    pass


class HomePage(BasePage):

    MAIL_BUTTON = "//div[contains(text(),'Почта')]"

    def click_mail_button(self):
        window_before = self.driver.window_handles[0]
        element = self.driver.find_element_by_xpath(HomePage.MAIL_BUTTON)
        element.click()
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_before)
        self.driver.close()
        self.driver.switch_to.window(window_after)


class MailAuthorizationPage(BasePage):

    LOGIN_FIELD = "//input[@id='passp-field-login']"
    PASSWORD_FIELD = "//input[@id='passp-field-passwd']"

    def account_authorization(self, login, password, await_time_out=5):
        login_input = self.driver.find_element_by_xpath(MailAuthorizationPage.LOGIN_FIELD)
        login_input.send_keys(login)
        login_input.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, await_time_out).until(EC.visibility_of_element_located((By.XPATH,
                                                                                             MailAuthorizationPage.PASSWORD_FIELD)))
        password_input = self.driver.find_element_by_xpath(MailAuthorizationPage.PASSWORD_FIELD)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def close_first_window(self, window_before, window_after):
        self.driver.switch_to.window(window_before)
        self.driver.close()
        self.driver.switch_to.window(window_after)


class MailPage(BasePage):

    REFRESH_BUTTON = "//span[@title='Проверить, есть ли новые письма (F9)']"
    CREATE_MAIL_BUTTON = "//a[@title='Написать (w, c)']"
    ADDRESS_FIELD = "//div[@class='MultipleAddressesDesktop ComposeRecipients-MultipleAddressField " \
                    "ComposeRecipients-ToField tst-field-to']//div[@class='composeYabbles'] "
    SUBJECT_FIELD = "//input[@name='subject']"
    MAIL_BODY = "//div[@placeholder='Напишите что-нибудь']//div"
    SEND_BUTTON = "//button[@aria-disabled='false']"

    def mails_counter_by_subject(self, subject, await_time_out=5):
        WebDriverWait(self.driver, await_time_out).until(
            EC.visibility_of_any_elements_located((By.XPATH, MailPage.REFRESH_BUTTON)))
        try:
            mails: list = self.driver.find_elements(By.XPATH,
                                                    "//span[@title='" + subject + "']")
            return len(mails)
        except NoMailsWithSubjectFound:
            return 0

    def mails_counter_by_second_subject(self, second_subject):
        mail_page = MailPage(self.driver)
        try:
            mails_counter_by_second_subject = mail_page.mails_counter_by_subject(second_subject)
        except NoMailsWithSubjectFound:
            mails_counter_by_second_subject = 0
        return mails_counter_by_second_subject

    def sum_of_mails(self, await_time_out=5):
        self.driver.refresh()
        WebDriverWait(self.driver, await_time_out).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//span[@title='Проверить, есть ли новые письма (F9)']")))
        self.click_page_actions(MailPage.REFRESH_BUTTON)
        mails_summary: list = self.driver.find_elements(By.XPATH,
                                                        "//span[@class='mail-MessageSnippet-Item mail-MessageSnippet-Item_body js-message-snippet-body']")
        return len(mails_summary)

    def click_page_actions(self, locator):
        element = self.driver.find_element_by_xpath(locator)
        element.click()

    def send_input(self, locator, input_text):
        input_data = self.driver.find_element_by_xpath(locator)
        input_data.send_keys(input_text)
        input_data.send_keys(Keys.ENTER)

    def send_mail_action(self, count, count_sum, await_time_out=5):
        self.click_page_actions(MailPage.CREATE_MAIL_BUTTON)
        WebDriverWait(self.driver, await_time_out).until(EC.visibility_of_any_elements_located(
            (By.XPATH, "//div[@class='MultipleAddressesDesktop ComposeRecipients-MultipleAddressField " \
                       "ComposeRecipients-ToField tst-field-to']//div[@class='composeYabbles'] ")))
        self.send_input(MailPage.ADDRESS_FIELD, "sdettest@yandex.ru")
        self.send_input(MailPage.SUBJECT_FIELD, "Simbirsoft Тестовое задание. Шевадров")
        text_input = self.driver.find_element_by_xpath(MailPage.MAIL_BODY)
        text_input.send_keys(f"Писем с начальными условиями на странице: ({count})! Всего писем на "
                             f"странице: {count_sum}")
        self.click_page_actions(MailPage.SEND_BUTTON)
        self.click_page_actions(MailPage.REFRESH_BUTTON)


