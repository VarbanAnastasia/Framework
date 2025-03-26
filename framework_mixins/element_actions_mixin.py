from venv import logger

from allure import step
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from typing import Generator, Self, Sequence
import selenium.webdriver.support.expected_conditions as EC

from web.locator import Locator


#
#
class _ElementActionsMixin:
    """Класс с базовыми методами управления элементами страницы"""


    def __init__(self, driver: WebDriver):
        """
        Args:
            driver: Инстанс WebDriver;
        """
        self._driver = driver

    # @format_locator
    @step("Ожидать присутствие элемента в DOM страницы")
    def find_element(self, locator: Locator, timeout: float = 15, **kwargs) -> WebElement:
        """
        Ожидать присутствие элемента в DOM страницы.

        Args:
            locator: Инстанс Locator;
            timeout: Количество секунд до тайм-аута ожидания;
            **kwargs: Аргументы для форматирования локатора.
        """
        try:
            logger.info(f'Ожидание присутствия {locator} в DOM странице в течение {timeout} секунд')
            element = WebDriverWait(driver=self._driver, timeout=timeout).until(
                EC.presence_of_element_located((locator.locator))
            )
            logger.info(f'{locator} найден в DOM странице!')
            return element
        except TimeoutException as ex:
            logger.error(msg := f'Не удалось найти {locator} в DOM странице в течение {timeout} секунд')
            # raise core_exceptions.NotFoundElementError(msg=msg) from ex
            raise ex
#
#     @format_locator
#     @step("Получить элемент по локатору и индексу")
#     def find_element_by_index(self, locator: Locator, index: int, **kwargs) -> WebElement:
#         """
#         Получить элемент по локатору и индексу.
#
#         Args:
#             locator: Инстанс Locator;
#             index: Индекс элемента;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#         logger.info(f'Получить {index} элемент {locator}')
#         elements = self.find_elements(locator=locator)
#         logger.debug(f'Найдено элементов: {len(elements)}')
#
#         if index >= len(elements):
#             logger.error(
#                 msg := f'Количество найденных элементов {locator}: {len(elements)} меньше, чем указанный индекс'
#             )
#             raise core_exceptions.IndexElementError(msg=msg)
#
#         logger.success(f'Найден элемент {locator} по индексу {index}')
#         return elements[index]
#
#
#     @format_locator
#     @step("Искать несколько элементов по локатору")
#     def find_elements(self, locator: Locator, **kwargs) -> List[WebElement]:
#         """Найти список элементов
#
#         Args:
#             locator: Инстанс Locator;
#             ** kwargs: Аргументы для форматирования локатора.
#         """
#
#         logger.info(f'Найти все элементы {locator}')
#         elements = self._driver.find_elements(*locator.locator)
#         logger.debug(f'Найдено элементов: {len(elements)}')
#
#         return elements
#
#
#     @format_locator
#     @step("Ожидать видимость элемента")
#     @make_screenshot
#     def find_visible_element(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> WebElement:
#         """Ожидать присутствие элемента в DOM странице и его видимость.
#
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#
#         try:
#             logger.info(f'Ожидание видимого {locator} в течение {timeout} секунд')
#             element = WebDriverWait(driver=self._driver, timeout=timeout).until(
#                 EC.visibility_of_element_located(locator.locator),
#             )
#             logger.success("Элемент найден и виден!")
#             return element
#         except TimeoutException as ex:
#             logger.error(msg := f'Не удалось найти видимый {locator} в течение {timeout} секунд')
#             raise core_exceptions.NotFoundElementError(msg=msg) from ex
#
#
#     @format_locator
#     @step("Ожидать кликабельность элемента")
#     def find_clickable_element(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> WebElement:
#         """Ожидать, что элемент виден и активен и по нему можно кликнуть.
#
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#         try:
#             logger.info(f'Ожидание кликабельного {locator} в течение {timeout} секунд')
#             element = WebDriverWait(driver=self._driver, timeout=timeout).until(
#                 EC.element_to_be_clickable(locator.locator),
#             )
#             logger.success("Элемент найден и кликабелен!")
#             return element
#         except TimeoutException as ex:
#             logger.error(msg := f'Не удалось найти кликабельный {locator} в течение {timeout} секунд')
#             raise core_exceptions.NotFoundElementError(msg=msg) from ex
#
#
    # @format_locator
    @step("Кликнуть на элемент по локатору")
    # @make_screenshot
    def click_by_locator(
        self,
        locator: Locator,
        # timeout: float = driver_config.TIMEOUT,
        timeout: float = 15,
        scroll: bool = False,
        ignoring_exceptions: Sequence[type[Exception]] = (),
        trying_counter: int = 3,
        is_clickable: bool = True,
        **kwargs,
    ) -> WebElement:
        """Найти элемент по локатору и кликнуть по нему.

        Args:
            locator: Инстанс Locator;
            timeout: Количество секунд до тайм-аута ожидания;
            scroll: Использовать прокрутку к элементу перед кликом или нет;
            ignoring_exceptions: список типов игнорируемых исключений;
            trying_counter: Количество попыток кликнуть при игнорировании исключений;
            is_clickable: дополнительная проверка на кликабельность элемента;
            **kwargs: Аргументы для форматирования локатора.
        """

        if scroll:
            self.scroll_into_view_by_locator(locator=locator)

        for counter in range(trying_counter if ignoring_exceptions else 1):
            logger.info(f'Кликаем на {locator}')
            element = self.find_visible_element(locator=locator, timeout=timeout)

            if is_clickable:
                element = self.find_clickable_element(locator=locator, timeout=timeout)
#
#     def click_by_locator(
#             self,
#             locator: Locator,
#             timeout: float = driver_config.TIMEOUT,
#             is_clickable: bool = True,
#             **kwargs,
#     ) -> WebElement:
#         """Найти элемент по локатору и кликнуть по нему."""
#
#         if is_clickable:
#             element = self.find_clickable_element(locator=locator, timeout=timeout)
#
#         element.click()
#         logger.success("Клик успешно произведен!")
#
#         return element
#
#         except Exception as ex:
#         logger.debug(f'Во время работы клика произошла ошибка:\n{ex}. Попытка {counter + 1}')
#
#         if type(ex) not in ignoring_exceptions:
#             logger.error(f'Во время попытки клика произошла ошибка:\n{ex}')
#             raise ex
#
#         logger.error(msg := f'Не удалось совершить клик на {locator}. Количество попыток: {trying_counter}')
#         raise core_exceptions.ClickElementError(msg=msg)
#
#     @step("Кликнуть на элемент")
#     @make_screenshot
#     def click_by_element(self, element: WebElement, locator: Locator, scroll: bool = False) -> WebElement:
#         """Кликнуть по элементу.
#
#         Args:
#             element: Инстанс WebElement;
#             locator: Инстанс Locator;
#             scroll: Использовать прокрутку к элементу перед кликом или нет.
#         """
#
#         if scroll:
#             self.scroll_into_view_by_element(element=element, locator=locator)
#
#         logger.info(f'Кликаем на {locator}')
#
#         try:
#             element.click()
#             logger.success("Клик успешно произведен!")
#             return element
#         except Exception as ex:
#             logger.error(msg := f'Не удалось совершить клик на {locator}')
#             raise core_exceptions.ClickElementError(msg=msg) from ex
#
#     def _click_with_hover(self, locator: Locator, element: WebElement) -> None:
#         """Навести на элемент и кликнуть
#
#         Args:
#             locator: Инстанс Locator;
#             element: Инстанс WebElement;
#         """
#
#         logger.debug(f'Кликаем по элементу {locator} с наведением')
#
#         try:
#             ActionChains(self._driver).move_to_element(element).click().perform()
#             logger.success("Клик успешно произведен!")
#         except Exception as ex:
#             logger.error(msg := f'Не удалось кликнуть с наведением на элемент {locator}')
#             raise core_exceptions.ClickElementError(msg=msg) from ex
#
#     @step("Кликнуть на элемент по локатору с наведением")
#     @make_screenshot
#     def click_with_hover_by_locator(
#             self,
#             locator: Locator,
#             timeout: float = driver_config.TIMEOUT,
#             is_clickable: bool = True,
#             **kwargs,
#     ) -> WebElement:
#         """Навести курсор на элемент по локатору и кликнуть по нему.
#
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             is_clickable: Дополнительная проверка кликабельности элемента;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#
#         if is_clickable:
#             element = self.find_clickable_element(locator=locator, timeout=timeout)
#         else:
#             element = self.find_visible_element(locator=locator, timeout=timeout)
#
#         self._click_with_hover(locator=locator, element=element)
#
#         return element
#
#     @step("Кликнуть на элемент с наведением")
#     @make_screenshot
#     def click_with_hover_by_element(self, element: WebElement, locator: Locator) -> WebElement:
#         """Навести курсор на элемент и кликнуть по нему.
#
#         Args:
#             element: Инстанс WebElement;
#             locator: Инстанс Locator;
#         """
#         self._click_with_hover(locator=locator, element=element)
#
#         return element
#
#     @step("Кликнуть на элемент по локатору с наведением")
#     @make_screenshot
#     def click_with_hover_by_locator(
#         self,
#         locator: Locator,
#         timeout: float = driver_config.TIMEOUT,
#         is_clickable: bool = True,
#         **kwargs,
#     ) -> WebElement:
#         """Навести курсор на элемент по локатору и кликнуть по нему.
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             is_clickable: Дополнительная проверка кликабельности элемента;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#
#         if is_clickable:
#             element = self.find_clickable_element(locator=locator, timeout=timeout)
#         else:
#             element = self.find_visible_element(locator=locator, timeout=timeout)
#
#         self._click_with_hover(locator=locator, element=element)
#
#         return element
#
#
#     @step("Кликнуть на элемент с наведением")
#     @make_screenshot
#     def click_with_hover_by_element(self, element: WebElement, locator: Locator) -> WebElement:
#         """Навести курсор на элемент и кликнуть по нему.
#
#         Args:
#             element: Инстанс WebElement;
#             locator: Инстанс Locator;
#         """
#
#         self._click_with_hover(locator=locator, element=element)
#
#         return element
#
#
#     @format_locator
#     @step("Кликнуть ПКМ на элемент по локатору")
#     def click_context_by_locator(
#         self,
#         locator: Locator,
#         timeout: float = driver_config.TIMEOUT,
#         scroll: bool = False,
#         is_clickable: bool = True,
#         **kwargs,
#     ) -> WebElement:
#         """Найти элемент по локатору и кликнуть ПКМ по нему
#
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             scroll: Использовать прокрутку перед кликом или нет;
#             is_clickable: Дополнительная проверка кликабельности элемента;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#
#         if scroll:
#             self.scroll_into_view_by_locator(locator=locator)
#
#         if is_clickable:
#             element = self.find_clickable_element(locator=locator, timeout=timeout)
#         else:
#             element = self.find_visible_element(locator=locator, timeout=timeout)
#
#         ActionChains(self._driver).context_click(on_element=element).perform()
#         logger.success("Клик ПКМ успешно произведен!")
#
#         return element
#
#         except Exception as ex:
#             logger.error(msg := f'Не удалось совершить клик ПКМ на {locator}')
#             raise core_exceptions.ClickElementError(msg=msg) from ex
#
#
#     @format_locator
#     @step("Кликнуть на элемент по локатору с обновлением страницы")
#     @make_screenshot
#     def click_by_locator_with_refresh(
#             self,
#             locator: Locator,
#             timeout: int = driver_config.TIMEOUT,
#             interval: int = 2,
#             scroll: bool = False,
#             is_clickable: bool = True,
#             **kwargs,
#     ) -> WebElement:
#         """Кликнуть на элемент по локатору или перезагрузить страницу в случае его отсутствия или не отображения
#
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             interval: Количество секунд между попытками клика;
#             scroll: Использовать прокрутку к элементу перед кликом или нет;
#             is_clickable: Дополнительная проверка кликабельности элемента;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#
#         if scroll:
#             self.scroll_into_view_by_locator(locator=locator)
#
#         end = time() + timeout
#
#         with step(f'Кликаем на элемент с локатором {locator}'):
#             while time() < end:
#                 try:
#                     if scroll:
#                         self.scroll_into_view_by_locator(locator=locator)
#
#                     if is_clickable:
#                         element = self.find_clickable_element(locator=locator, timeout=interval)
#                     else:
#                         element = self.find_visible_element(locator=locator, timeout=interval)
#
#                     element.click()
#                     logger.success("Клик успешно произведен!")
#                     return element
#                 except Exception:
#                     logger.error(f"Не удалось кликнуть на {locator}")
#                     logger.info("Обновление страницы")
#                     self._driver.refresh()
#
#         logger.error(msg := f'Не удалось кликнуть на "{locator}" в течение "{timeout}" секунд с обновлением страницы')
#         raise core_exceptions.ClickElementError(msg)
#
#
#     @format_locator
#     @step("Кликнуть на элемент по локатору с помощью JS")
#     def click_by_locator_with_js(
#             self,
#             locator: Locator,
#             timeout: float = driver_config.TIMEOUT,
#             scroll: bool = False,
#             **kwargs,
#     ) -> WebElement:
#         """Найти элемент по локатору и кликнуть по нему с помощью JS
#
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             scroll: Использовать прокрутку к элементу перед кликом или нет;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#
#         if scroll:
#             self.scroll_into_view_by_locator(locator=locator)
#
#         logger.info(f'Кликаем на {locator}')
#
#         element = self.find_element(locator=locator, timeout=timeout)
#
#         self._driver.execute_script("arguments[0].click();", element)
#         logger.success("Клик успешно произведен!")
#
#         return element
#
#         except Exception as ex:
#         logger.error(msg := f'Не удалось совершить клик ПКМ на {locator}')
#         raise core_exceptions.ClickElementError(msg=msg) from ex
#
#
#     @format_locator
#     @step("Ввести значение в элемент по локатору")
#     @make_screenshot
#     def send_keys_by_locator(
#             self,
#             locator: Locator,
#             keys: str | Sequence[str],
#             clear: bool = True,
#             timeout: float = driver_config.TIMEOUT,
#             **kwargs,
#     ) -> WebElement:
#         """Найти элемент по локатору и ввести в него значение.
#
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             keys: Строка для ввода;
#             clear: Очистить поле или нет;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#
#         try:
#             logger.info(f'Заполняем {locator} значением "{keys}"')
#             element = self.find_visible_element(locator=locator, timeout=timeout)
#
#             if clear:
#                 element.clear()
#
#             element.send_keys(keys)
#             logger.success("Ввод успешно произведен!")
#
#             return element
#         except Exception as ex:
#             logger.error(
#                 msg := f'Не удалось ввести в {locator}, значение "{keys}", с элементом нельзя взаимодействовать'
#             )
#             raise core_exceptions.SendKeysElementError(msg=msg) from ex
#
#
#     @staticmethod
#     @step("Ввести значение в элемент")
#     @make_screenshot
#     def send_keys_by_element(
#             element: WebElement, locator: Locator, keys: str | Sequence[str], clear: bool = True
#     ) -> WebElement:
#         """Ввести значение в элемент.
#
#         Args:
#             element: Инстанс WebElement;
#             locator: Инстанс Locator;
#             keys: Строка для ввода;
#             clear: Очистить поле или нет.
#         """
#
#         try:
#             logger.info(f'Заполняем {locator} значением "{keys}"')
#
#             if clear:
#                 element.clear()
#
#             element.send_keys(keys)
#             logger.success("Ввод успешно произведен!")
#
#             return element
#         except Exception as ex:
#             logger.error(msg := f'Не удалось ввести значение в {locator}')
#             raise core_exceptions.SendKeysElementError(msg=msg) from ex
#
#
#     @format_locator
#     @step("Очистить элемент по локатору")
#     @make_screenshot
#     def clear_by_locator(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> WebElement:
#         """Найти элемент по локатору и очистить в нем текст.
#
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#
#         try:
#             logger.info(f'Очищаем текст {locator}')
#             element = self.find_visible_element(locator=locator, timeout=timeout)
#             element.clear()
#             logger.success("Элемент успешно очищен!")
#             return element
#         except Exception as ex:
#             logger.error(msg := f'Не удалось очистить {locator}, элемент находится в недоступном состоянии')
#             raise core_exceptions.ClearElementError(msg=msg) from ex
#
#
#     @format_locator
#     @step("Очистить элемент по локатору клавишей backspace")
#     @make_screenshot
#     def clear_by_locator_with_backspace(self, locator: Locator, timeout: int = driver_config.TIMEOUT,
#                                         **kwargs) -> WebElement:
#         """Найти элемент по локатору и очистить в нем текст клавишей backspace.
#
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#
#         with step("Получить значение из элемента"):
#             element = self.find_visible_element(locator=locator, timeout=timeout)
#             value = element.get_attribute('value') if element.get_attribute('value') else ''
#
#         if value != '':
#             with step(f'Очищаем элемент {locator} нажатием backspace'):
#                 for _ in value:
#                     element.send_keys(Keys.BACKSPACE)
#
#             if value := element.get_attribute('value'):
#                 logger.warning(f'Не удалось до конца очистить поле, оставшееся значение: {value}')
#
#         return element
#
#
#     @format_locator
#     @step("Очистить элемент по локатору с помощью JS")
#     @make_screenshot
#     def clear_by_locator_with_js(self, locator: Locator, timeout: int = driver_config.TIMEOUT, **kwargs) -> WebElement:
#         """Найти элемент по локатору и очистить в нем текст с помощью JS.
#
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#         element = self.find_element(locator=locator, timeout=timeout)
#         self._driver.execute_script("arguments[0].value = '';", element)
#
#         return element
#
#
#     @format_locator
#     @step("Навести мышь на элемент по локатору")
#     def move_to_element_by_locator(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> WebElement:
#         """Переместить мышь в центральную точку элемента в поле зрения через локатор.
#
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#
#         logger.info(f'Перемещаем указатель в центр {locator}')
#         element = self.find_element(locator=locator, timeout=timeout)
#
#         try:
#             ActionChains(self._driver).move_to_element(element).perform()
#         except Exception as ex:
#             logger.error(msg := f'Не удалось переместить указатель на элемент {locator}')
#             raise core_exceptions.ActionChainsError(msg=msg) from ex
#
#         logger.success("Указатель перемещен!")
#         return element
#
#
#     def move_with_offset(self, locator: Locator, element: WebElement, x_offset: int, y_offset: int):
#         """Перемещение указателя на элемент с учетом смещения.
#
#         Args:
#             locator: Инстанс Locator;
#             element: Инстанс WebElement;
#             x_offset: Смещение по оси X;
#             y_offset: Смещение по оси Y.
#         """
#
#         try:
#             ActionChains(self._driver).move_to_element_with_offset(element, x_offset, y_offset).perform()
#         except Exception as ex:
#             logger.error(msg := f'Не удалось переместить указатель на элемент {locator} со смещением')
#             raise core_exceptions.ActionChainsError(msg=msg) from ex
#
#         logger.success("Указатель перемещен со смещением!")
#
#
#     def move_with_offset(self, locator: Locator, element: WebElement, x_offset: int, y_offset: int):
#         """Перемещение указателя на элемент с учетом смещения.
#
#         Args:
#             locator: Инстанс Locator;
#             element: Инстанс WebElement;
#             x_offset: Смещение по оси X;
#             y_offset: Смещение по оси Y.
#         """
#
#         try:
#             ActionChains(self._driver).move_to_element_with_offset(
#                 to_element=element, xoffset=x_offset, yoffset=y_offset
#             ).perform()
#         except Exception as ex:
#             logger.error(
#                 msg := f'Не удалось переместить указатель на элемент {locator} со смещением X: {x_offset}, Y: {y_offset}'
#             )
#             raise core_exceptions.ActionChainsError(msg=msg) from ex
#
#         logger.success("Указатель перемещен!")
#
#
#     @format_locator
#     @step("Навести мышь на элемент по локатору со смещением")
#     def move_to_element_by_locator_with_offset(
#             self,
#             locator: Locator,
#             x_offset: int = 0,
#             y_offset: int = 0,
#             timeout: float = driver_config.TIMEOUT,
#             **kwargs,
#     ) -> WebElement:
#         """Переместить мышь в центральную точку элемента со смещением в поле зрения через локатор.
#
#         Args:
#             locator: Инстанс Locator;
#             x_offset: Смещение по оси X;
#             y_offset: Смещение по оси Y;
#             timeout: Количество секунд до тайм-аута ожидания;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#         logger.info(f'Перемещаем указатель к элементу {locator} со смещением X: {x_offset}, Y: {y_offset}')
#         element = self.find_element(locator=locator, timeout=timeout)
#
#         self.move_with_offset(locator=locator, element=element, x_offset=x_offset, y_offset=y_offset)
#
#         return element
#
#
#     @step("Навести мышь на элемент")
#     def move_to_element_by_element(self, element: WebElement, locator: Locator) -> WebElement:
#         """Переместить мышь в центральную точку элемента в поле зрения.
#
#         Args:
#             element: Инстанс WebElement;
#             locator: Инстанс Locator.
#         """
#         logger.info(f'Перемещаем указатель в центр {locator}')
#
#         try:
#             ActionChains(self._driver).move_to_element(element).perform()
#         except Exception as ex:
#             logger.error(msg := f'Не удалось переместить указатель на элемент {locator}')
#             raise core_exceptions.ActionChainsError(msg=msg) from ex
#
#         logger.success("Указатель перемещен!")
#         return element
#
#
#     @step("Навести мышь на элемент со смещением")
#     def move_to_element_by_element_with_offset(
#             self,
#             element: WebElement,
#             locator: Locator,
#             x_offset: int = 0,
#             y_offset: int = 0,
#             **kwargs,
#     ) -> WebElement:
#         """Переместить мышь в центральную точку элемента со смещением в поле зрения.
#
#         Args:
#             element: Инстанс WebElement;
#             locator: Инстанс Locator;
#             x_offset: Смещение по оси X;
#             y_offset: Смещение по оси Y;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#         logger.info(f'Перемещаем указатель к элементу {locator} со смещением X: {x_offset}, Y: {y_offset}')
#
#         self.move_with_offset(locator=locator, element=element, x_offset=x_offset, y_offset=y_offset)
#
#         return element
#
#
#     @format_locator
#     @step("Прокрутить страницу до элемента по локатору")
#     def scroll_into_view_by_locator(
#             self,
#             locator: Locator,
#             block: JsScrollAlign = JsScrollAlign.START,
#             inline: JsScrollAlign = JsScrollAlign.NEAREST,
#             timeout: float = driver_config.TIMEOUT,
#             **kwargs,
#     ) -> WebElement:
#         """Найти элемент по локатору и прокрутить до него страницу.
#
#         Args:
#             locator: Инстанс Locator;
#             block: Определение вертикального выравнивания;
#             inline: Определение горизонтального выравнивания;
#             timeout: Количество секунд до тайм-аута ожидания;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#         logger.info(f'Прокручиваем страницу до {locator}, с режимом выравнивания: {block=}, {inline=}')
#         element = self.find_element(locator=locator, timeout=timeout)
#
#         options = {"block": block.low_value, "inline": inline.low_value}
#         self._driver.execute_script("arguments[0].scrollIntoView(arguments[1]);", element, options)
#
#         logger.success("Страница прокручена!")
#
#         return element
#
#
#     @step("Прокрутить страницу до элемента")
#     def scroll_into_view_by_element(
#             self,
#             element: WebElement,
#             block: JsScrollAlign = JsScrollAlign.START,
#             inline: JsScrollAlign = JsScrollAlign.NEAREST,
#     ) -> WebElement:
#         """Прокрутить страницу до переданного элемента.
#
#         Args:
#             element: Инстанс WebElement;
#             block: Определение вертикального выравнивания;
#             inline: Определение горизонтального выравнивания.
#         """
#         logger.info("Прокручиваем страницу до элемента")
#
#         options = {"block": block.low_value, "inline": inline.low_value}
#         self._driver.execute_script("arguments[0].scrollIntoView(arguments[1]);", element, options)
#
#         logger.success("Страница прокручена!")
#
#         return element
#
#
#     def scroll_into_view_by_element(self, element: WebElement, block, inline) -> WebElement:
#         """Прокручивает страницу до элемента.
#
#         Note:
#             Ведение части элемента к краю видимой области через локатор.
#
#         Args:
#             element: Инстанс WebElement;
#             block: определение вертикального выравнивания;
#             inline: определение горизонтального выравнивания.
#         """
#         logger.info(f'Прокручиваем страницу до {element}, с режимом выравнивания: {block=}, {inline=}')
#
#         options = {'block': block.low_value, 'inline': block.low_value}
#         self._driver.execute_script(f'arguments[0].scrollIntoView({options});', element)
#
#         logger.success(f'Страница прокручена!')
#         return element
#
#
#     @format_locator
#     @step('Прикрепить файл в поле по локатору')
#     @make_screenshot
#     def attach_file(self, attachment_name: str, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> None:
#         """
#         Прикрепить файл к веб-элементу.
#
#         Args:
#             attachment_name: Наименование прикрепляемого файла;
#             locator: Наименование элемента;
#             timeout: Количество секунд до тайм-аута ожидания;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#         logger.info(f'Прикрепление файла {attachment_name} в поле {locator}')
#         file_path = str(Config.test_data.dir) + attachment_name
#         self.find_element(locator=locator, timeout=timeout).send_keys(file_path)
#         logger.success(f'Файл {attachment_name} прикреплен!')
#
#
#     @format_locator
#     @step('Переключиться на фрейм')
#     def _switch_to_frame_with_locator(self, locator: Locator, locator_inside: Locator | None = None,
#                                       timeout: float = driver_config.TIMEOUT, **kwargs) -> None:
#         """
#         Переключение на фрейм по локатору.
#
#         Args:
#             locator: Инстанс Locator фрейма;
#             locator_inside: Locator внутри фрейма для проверки отображения;
#             timeout: Количество секунд до тайм-аута ожидания;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#         try:
#             logger.info(f'Переключаемся на iframe {locator} в течение {timeout} секунд')
#             WebDriverWait(self._driver, timeout=timeout).until(EC.frame_to_be_available_and_switch_to_it(locator.locator))
#
#             if locator_inside:
#                 wums(
#                     method=lambda loc: self.find_element(locator=loc).is_displayed(),
#                     expected=True,
#                     ignoring_exceptions=[TimeoutException],
#                     loc=locator_inside,
#                 )
#
#             logger.success(f'Фрейм найден!')
#         except Exception as ex:
#             logger.error(f'Не удалось переключиться во фрейм с локатором "{locator}"')
#             raise core_exceptions.SwitchIframeError(msg=str(ex)) from ex
#
#
#     @step('Переключиться на дефолтный фрейм')
#     def _switch_to_default_frame(self, locator_out_frame: Locator | None = None) -> None:
#         """
#         Переключение на дефолтный фрейм.
#
#         Args:
#             locator_out_frame: Locator фрейма для проверки переключения на дефолтный фрейм.
#         """
#         logger.info('Переключаемся на фрейм по умолчанию')
#         self._driver.switch_to.default_content()
#
#         if locator_out_frame:
#             wums(
#                 method=lambda loc: self.find_element(locator=loc).is_displayed(),
#                 expected=True,
#                 ignoring_exceptions=[TimeoutException],
#                 loc=locator_out_frame,
#             )
#
#         logger.success('Успешно переключены на фрейм по умолчанию')
#
#
#     @contextmanager
#     def switch_to_iframe_with_context(self, iframe: Locator, locator_in_frame: Locator | None = None,
#                                       locator_default_frame: Locator | None = None) -> Generator[Self, None, None]:
#         """
#         Переключение на iframe с помощью контекстного менеджера.
#
#         Args:
#             iframe: Локатор iframe;
#             locator_in_frame: Локатор внутри iframe для проверки;
#             locator_default_frame: Локатор на фрейме по умолчанию для проверки переключения.
#         """
#         logger.debug('Вход в iframe через контекстный менеджер')
#         self._switch_to_frame_with_locator(locator=iframe, locator_inside=locator_in_frame)
#
#         yield self
#
#         logger.debug('Выход из iframe через контекстный менеджер')
#         self._switch_to_default_frame(locator_out_frame=locator_default_frame)
#
#     @format_locator
#     @step('Получить текст из элемента по локатору')
#     def get_text_from_element_by_locator(self, locator: Locator, timeout: int = driver_config.TIMEOUT, **kwargs) -> str:
#         """
#         Получить текст из элемента.
#
#         Args:
#             locator: Инстанс Locator;
#             timeout: Количество секунд до тайм-аута ожидания;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#         logger.debug(f'Получаем текст из элемента {locator}')
#         text = self.find_element(locator=locator, timeout=timeout).text
#         logger.success(f'Полученный текст: {text}')
#         return text
#
#     @format_locator
#     @step('Получить текст из элемента')
#     def get_text_from_element_by_element(self, element: WebElement, locator: Locator, **kwargs) -> str:
#         """
#         Получить текст из элемента.
#
#         Args:
#             element: Инстанс WebElement;
#             locator: Инстанс Locator;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#         logger.debug(f'Получаем текст из элемента {locator}')
#         try:
#             result = element.text
#         except StaleElementReferenceException as ex:
#             logger.error(f'{locator} отсутствует в DOM!')
#             raise core_exceptions.NotFoundElementError(msg=str(ex)) from ex
#
#         logger.success(f'Полученный текст: {result}')
#         return result
#
#     @format_locator
#     @step('Получить css property из элемента по локатору')
#     def get_css_property_from_element_by_locator(self, locator: Locator, property_name: str, timeout: int = driver_config.TIMEOUT, **kwargs) -> str:
#         """
#         Получить css property из элемента.
#
#         Args:
#             locator: Инстанс Locator;
#             property_name: Свойство css;
#             timeout: Количество секунд до тайм-аута ожидания;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#         logger.debug(f'Получаем {property_name} из элемента {locator}')
#         result = self.find_element(locator=locator, timeout=timeout).value_of_css_property(property_name=property_name)
#
#         if not result:
#             logger.error(f'Не удалось получить {property_name} из элемента {locator}')
#             raise core_exceptions.PropertyElementError(msg=f"Не удалось получить {property_name}")
#
#         logger.success(f'Полученный {property_name}: {result}')
#         return result
#
#     @format_locator
#     @step('Получить css property из элемента')
#     def get_css_property_from_element_by_element(self, element: WebElement, locator: Locator, property_name: str, **kwargs) -> str:
#         """
#         Получить css property из элемента.
#
#         Args:
#             element: Инстанс WebElement;
#             locator: Инстанс Locator;
#             property_name: Свойство css;
#             **kwargs: Аргументы для форматирования локатора.
#         """
#         logger.debug(f'Получаем {property_name} из элемента {locator}')
#         result = element.value_of_css_property(property_name=property_name)
#
#         if not result:
#             logger.error(f'Не удалось получить {property_name} из элемента {locator}')
#             raise core_exc eptions.PropertyElementError(msg=f"Не удалось получить {property_name}")
#
#         logger.success(f'Полученный {property_name}: {result}')
#         return result
#
#
#
