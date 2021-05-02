import pandas as pd
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# Get the relevant details relate to the articles.
def obtain_details(single_result):
    field_category = single_result.find_element_by_class_name("field-category").text
    created_time = single_result.find_element_by_class_name("created-ago").text
    article_title = single_result.find_element_by_class_name("field-title").text
    article_teaser = single_result.find_element_by_class_name("article-teaser").text
    return {"Title": article_title, "Time_Created": created_time, "Category": field_category, "Teaser": article_teaser}


# Perform scrapping on every web page.
def page_scraping(driver, article_required, url, category):
    target_reached = False
    page_counter = 0
    article_counter = 0
    df = pd.DataFrame(columns=["Title", "Time_Created", "Category", "Teaser"])

    driver.get(url.format(pageNumber=page_counter, category=category))
    time.sleep(10)

    while not target_reached:

        results = driver.find_elements_by_css_selector("div.article-teaser")
        list_len_result = len(results)

        for index in range(list_len_result):
            # This checking is to skip the irrelevant html element from the results.
            if index % 2 == 0:
                details = obtain_details(results[index])
                df = df.append(details, ignore_index=True)
                article_counter += 1
                print("Article({category}) {counter} completed!".format(counter=article_counter, category=category))
                if article_counter == article_required:
                    target_reached = True
                    break

        if target_reached:
            break

        page_counter += 1
        driver.get(url.format(pageNumber=page_counter, category=category))
        time.sleep(10)

    return df


# Start of the program
driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://www.nst.com.my/news/{category}?page={pageNumber}"
categories = ["exclusive", "crime-courts", "nation", "government-public-policy", "politics"]
dataset = pd.DataFrame(columns=["Title", "Time_Created", "Category", "Teaser"])
number_of_items_per_category = 500

# Loop through all the category in the NST website for news only!
for category in categories:
    data = page_scraping(driver, number_of_items_per_category, url, category)
    print("Scrap on the " + category + " completed!\n")
    dataset = dataset.append(data, ignore_index=True)

print("Web Scrap Completed!")

# Closes the browser active window
driver.close()

# Save the data in the csv format.
dataset.to_csv("./dataset/rawdata.csv", index=False)
