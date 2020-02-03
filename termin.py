from selenium.webdriver import Chrome, ChromeOptions
from time import sleep
import os


appointment_count = "1"
termin_id = os.environ['termin_id']
url = os.environ['url'] + termin_id
count_drp_dwn = '//select'
submit_count = '//input[@type="submit"]'
bookable_date = '//a[contains(@class, "nat_calendar_weekday_bookable")]'
bookable_time = '//input[@class="WEB_APPOINT_TIMELIST_BUTTON"]'
next_button = '//a[contains(@class, "navButton") and contains(@href, "NEXT")]'
month_text = '//span[@class="navMonthText"]'


browser_options = ChromeOptions()
browser_options.add_argument('--headless')
driver = Chrome(options=browser_options)
dates = {}
try:
    driver.get(url)
    frames = len(driver.find_elements_by_xpath("//iframe"))
    driver.switch_to.frame(0)
    driver.find_element_by_xpath(count_drp_dwn).send_keys(appointment_count)
    driver.find_element_by_xpath(submit_count).click()
    i = 0
    for avail_date in driver.find_elements_by_xpath(bookable_date):
        date_text = avail_date.get_attribute("href").split("'")[-2]
        appointments = []
        month_count = len(driver.find_elements_by_xpath(next_button))
        while not avail_date.is_displayed() and i < month_count:
            driver.find_elements_by_xpath(next_button)[i].click()
            i += 1
            sleep(1)
        avail_date.click()
        for avail_time in driver.find_elements_by_xpath(bookable_time):
            appointments.append(avail_time.get_attribute("value"))
        # print("{} :: {}".format(date_text, appointmentsera))
        dates[date_text] = appointments
    print(dates)

    # Make HTML for upload
    hmtl_data = "<html><body><table border=1><tr><th>Date</th><th>Time Slots</th></tr>"
    for date in dates:
        hmtl_data += "<tr><td><b>{}</b></td><td>{}</td></tr>".format(date, ", ".join(dates[date]))
    hmtl_data += "</table></body></html>"
    with open("results/index.html", "w") as fp:
        fp.write(hmtl_data)

finally:
    driver.quit()
