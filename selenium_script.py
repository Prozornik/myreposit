# webdriver — основной интерфейс для управления браузером.
from selenium import webdriver
# By — позволяет выбирать элементы по типу селектора (CSS, XPath и др.).
from selenium.webdriver.common.by import By
# WebDriverWait и expected_conditions — нужны для ожидания событий (например, загрузки элементов или URL).
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Настройка драйвера (предположим, используем Chrome)
# ChromeOptions позволяет конфигурировать поведение браузера.
options = webdriver.ChromeOptions()
# Используется headless-режим, чтобы тест запускался без отображения окна браузера.
options.add_argument('--headless')  # если не нужен GUI
# Используем webdriver.Chrome() — самый популярный браузер в автоматизации.
driver = webdriver.Chrome(options=options)

try:
    # 1. Открываем веб-страницу
    # get() — стандартный метод для загрузки нужного URL.
    driver.get("https://example.com")
    # print нужен для вывода результата теста в терминале.
    print("Страница открыта")

    # 2. Проверяем, что заголовок содержит "Example"
    # driver.title возвращает текущий заголовок страницы.
    # assert используется для валидации — если условие ложно, тест падает с ошибкой.
    assert "Example" in driver.title, f"Заголовок не содержит 'Example': {driver.title}"
    print("Заголовок найден")

    # 3. Находим элемент с текстом "More information" и кликаем по нему
    # WebDriverWait(...).until(...) — явное ожидание (лучше, чем time.sleep()), чтобы избежать проблем с недогруженными элементами.
    # Селектор 'a[href*="iana.org"]' подбирается так, чтобы сработал даже при возможных изменениях в тексте ссылки.
    link = WebDriverWait(driver, 5).until(
        # element_to_be_clickable — гарантирует, что элемент доступен для клика.
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="iana.org"]'))
        # By.CSS_SELECTOR + 'a[href*="iana.org"]' — универсальный селектор, ищет ссылку по фрагменту href, устойчив к изменениям текста.
    )
    # Проверяем, что текст в элементе соответствует ожиданиям, затем кликаем по ссылке.
    assert "More information" in link.text, f"Ожидался текст 'More information', найдено: {link.text}"
    link.click()
    print("Элемент найден, перенаправление...")

    # 4. Проверяем, что произошел переход на нужный URL
    # После клика может потребоваться время, чтобы загрузить новую страницу. Используем явное ожидание, чтобы не делать sleep.
    WebDriverWait(driver, 5).until(
        EC.url_to_be("https://www.iana.org/help/example-domains")
    )
    # Финальная проверка, что редирект действительно сработал, и мы оказались на нужной странице.
    assert driver.current_url == "https://www.iana.org/help/example-domains", f"Переход не выполнен: {driver.current_url}"

    print("Тест пройден успешно!")

# try/except — чтобы тест не упал «тихо» при ошибке.
except Exception as e:
    print(f"Ошибка в тесте: {e}")

# finally: driver.quit() — гарантирует, что браузер будет закрыт даже при исключении (важно в автоматических сборках, чтобы не накапливались процессы).
finally:
    driver.quit()