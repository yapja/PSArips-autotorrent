from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import os

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', 'E:\\')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/x-bittorrent')

# Starts headless Firefox and redirect to PSArips page
# service_log_path disables geckodriver logging
options = Options()
options.headless = True
driver = webdriver.Firefox(options = options, service_log_path='NUL', firefox_profile=profile)

# Gets current working directory
path = os.getcwd() + '\\'

# Remember to include .xpi at the end of your file names 
extensions = [
    '{529b261b-df0b-4e3b-bf42-07b462da0ee8}.xpi',
    'uBlock0@raymondhill.net.xpi'
    ]

# Installs extensions needed (uBlock Origin, Universal Bypass)
for extension in extensions:
    driver.install_addon(path + extension, temporary=True)

driver.get('https://psarips.one')

while True:
    tv_series = input("Enter TV Series: ")
    episode = input("Enter Episode(S00E00): ").lower()

    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/div[2]/form/label/input').send_keys(tv_series)
    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/div[2]/form/input').click()
    driver.find_element_by_xpath('/html/body/div/div/div/div/div/section/div[2]/div[2]/div[1]/article[1]/div/div[1]/h2').click()

    try:
        divs = driver.find_elements_by_css_selector('div[class="sp-head"]')
        for div in divs:
            title = div.text.lower()
            if (title.find(episode) > -1 and title.find('1080p') > -1):
                div.click()
                link = driver.find_element_by_link_text('TORRENT')
                driver.get(link.get_attribute('href'))
                driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/main/article/div/div/p[2]/a').click()
                driver.get('https://psarips.one')
    except Exception as e:
        print(e)

driver.quit()