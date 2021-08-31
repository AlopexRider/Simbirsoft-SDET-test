
class MainPageLocators(object):
    MAIL_BUTTON = "//a[@class='home-link desk-notif-card__login-new-item " \
                             "desk-notif-card__login-new-item_mail home-link_black_yes']"


class MailLoginPageLocators(object):
    LOGIN_FIELD = "//input[@id='passp-field-login']"

    CONFIRM_BUTTON = "//button[@id='passp:sign-in']"

    PASSWORD_FIELD = "//input[@id='passp-field-passwd']"


class MailPageLocators(object):

    REFRESH_BUTTON = "//span[@title='Проверить, есть ли новые письма (F9)']"

    CREATE_MAIL_BUTTON = "//a[@title='Написать (w, c)']"

    ADDRESS_FIELD = "//div[@class='MultipleAddressesDesktop ComposeRecipients-MultipleAddressField " \
                    "ComposeRecipients-ToField tst-field-to']//div[@class='composeYabbles'] "

    SUBJECT_FIELD = "//input[@name='subject']"

    MAIL_BODY = "//div[@placeholder='Напишите что-нибудь']//div"

    SEND_BUTTON = "//button[@aria-disabled='false']"

    RETURN_TO_MAILS = "//span[contains(text(),'Письмо отправлено')]"
