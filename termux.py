from selenium import webdriver
import geckodriver_autoinstaller

geckodriver_autoinstaller.install()

driver = webdriver.Firefox()
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://ijul.my.id/")
print('\n',driver.find_element_by_tag_name('h3').text)
