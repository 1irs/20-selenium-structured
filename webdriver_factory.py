from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

import os

from webdriver_manager.chrome import ChromeDriverManager


class WebDriverFactory:

    @staticmethod
    def get_driver() -> WebDriver:
        """
        :return:  WebDriver — абстрактный класс, от которого унаследованы все другие
        вебдрайверы (Хром, удаленный, Фаерфокс и т. д.)
        """

        # Здесь должен быть алгоритм по которому фабрика выбирает КОНКРЕТУЮ РЕАЛИЗАЦИЮ драйвера.
        # Есть три варианта алгоритма:
        # 1. По дням недели (разумеется шуточный вариант)
        # 2. По переменной окружения DRIVER_KIND (реализовано на BitBucket Pipelines)
        # 3. По аргументам командной строки в момент запуска тестов.

        driver_kind: str = WebDriverFactory.get_driver_kind()
        if driver_kind == "remote":
            return WebDriverFactory.get_remote_driver()
        elif driver_kind == "chrome":
            return WebDriverFactory.get_chrome_driver()
        elif driver_kind == "firefox":
            return WebDriverFactory.get_firefox_driver()
        elif driver_kind == "safari":
            return WebDriverFactory.get_safari_driver()
        else:
            raise NotImplemented('Getting driver for ' + driver_kind + ' is not implemented yet.')

    @staticmethod
    def get_driver_kind() -> str:
        driver_kind: str = os.environ['SELENIUM_DRIVER_KIND'].lower()
        return driver_kind

    @staticmethod
    def get_firefox_driver():
        driver = FirefoxDriver()
        return driver

    @staticmethod
    def get_chrome_driver():
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    @staticmethod
    def get_remote_driver():
        options = Options()
        options.add_argument('--window-size=850, 1980')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        # Этот аргумент я добавил, чтобы избежать ошибки "selenium.common.exceptions.
        # WebDriverException: Message: unknown error: session deleted because of page crash"
        # "This will force Chrome to use the /tmp directory instead.
        # This may slow down the execution though since disk will be used instead of memory."
        # https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot
        options.add_argument('--disable-dev-shm-usage')

        remote_host: str = os.getenv('REMOTE_DRIVER_HOST', 'localhost').lower()

        driver = webdriver.Remote(
            command_executor=f'http://{remote_host}:3000/webdriver',
            options=options,
        )
        driver.implicitly_wait(10)
        driver.set_window_size(850, 1980)
        return driver

    @staticmethod
    def get_safari_driver():
        raise NotImplemented('Getting Safari driver not implemented yet.')
