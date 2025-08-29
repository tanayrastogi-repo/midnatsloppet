import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def scrape_website(url: str, gekodriver: str="./geckodriver", headless: bool = True, wait_seconds: int = 20) -> str:
    """Function to scrape the url provied. It returns the HTML DOM for the url recieved.

    Args:
        url (str): Link for which the DOM is scraped.
        gekodriver (str, optional): Path to the Firefox driver. Defaults to "./geckodriver".
        headless (bool, optional): To run the scarping without opening the browser. Defaults to True.
        wait_seconds (int, optional): Time to wait for the page to load. Defaults to 20.

    Returns:
        str: HTML DOM for the provided URL.
    """

    # Firefox driver
    options = webdriver.FirefoxOptions()
    if headless:
            options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service(gekodriver), options=options)

    # Fetch HTML from the webpage
    try:
        driver.get(url)
        print("Page opened:", url)

        # Wait until the results table rows are present (adjust selector if needed)
        wait = WebDriverWait(driver, wait_seconds)
        # Wait for at least one `.results-table .row` to appear
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".results-table .row")))
        ### Optionally wait until pagination is visible, or until a timestamp element has text
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pagination")))

        # 2) Optionally scroll to bottom to trigger lazy-load
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(0.5)

        # HTLM DOM
        html = driver.page_source
        return html

    except Exception as e:
        print("Fetch failed:", e)
        return ""

    finally:
        driver.quit()


def extract_table(html_content: str) -> list:
    """Extract the result from the HTML content

    Args:
        html_content (str): DOM from the Midnattsloppet result page.

    Returns:
        list: Each row of table as dict with keys: [place, bib, name, class, team, time]
    """

    soup = BeautifulSoup(html_content, "html.parser")

    # Varible to create a table
    table = []

    # Enumerate on each row of the table
    for itr, row in enumerate(soup.select(".results-table .row")):
        place = row.select_one(".pair .row-content") and row.select_one(".pair .row-content").get_text(strip=True)
        time_text = row.select_one(".pair.right .row-content") and row.select_one(".pair.right .row-content").get_text(strip=True)
        team = row.select_one(".team.row-content") and row.select_one(".team.row-content").get_text(strip=True)

        # Extracting the class, as there are multiple <html class> named "pair"
        classcat = None
        for pair in row.select(".pair"):
            header = pair.select_one(".table-header")
            if header and header.get_text(strip=True) == "Class":
                classcat = pair.select_one(".row-content").get_text(strip=True)

        # Bib and Name are together.
        # Seperate the bib and name from each other and save seperately.
        bib = None
        name_el = row.select_one(".name.row-content a") and row.select_one(".name.row-content a").get_text(strip=True)
        name = name_el
        if name_el is not None:
            parts = name_el.split(" ", 1)
            if len(parts) == 2 and parts[0].isdigit():
                bib =  parts[0]
                name = parts[1]

        # Adding to a table
        table.append({"place": place, "bib": bib, "name": name, "class": classcat, "team": team, "time": time_text})

    return table



def extract_tables_from_all_pages(total_pages: int = 1208,
                                  base_url: str    = "https://results.midnattsloppet.com/stockholm/results"
                        ) -> pd.DataFrame:
    """Function to extract result from all the number of pages in the midnattsloppet website

    Args:
        total_pages (int, optional): The number of pages from until the results is extracted (1 to n). Defaults to 1208.
        base_url (_type_, optional): URL for the result. Defaults to "https://results.midnattsloppet.com/stockholm/results".

    Returns:
        pd.DataFrame: Result with headers: [place, bib, name, class, team, time]
    """
    # Create an empty dataframe
    result_table = pd.DataFrame()

    # Loop Across the pages for results
    for number in (pbar:= tqdm(range(1, total_pages+1))):
        pbar.set_description(f"Processing page {number}")
        url = base_url + f"?page={number}"
        html_content = scrape_website(url)

        # Extract table from the page
        table = extract_table(html_content)

        # Convert the dict to dataframe
        result_table = pd.concat([result_table,
                                  pd.DataFrame.from_dict(table).iloc[1:]
                                ],
                            ignore_index=True)

    return result_table


if __name__ == "__main__":
    ## Save the table as feather
    res = extract_tables_from_all_pages()

    print("\n Saving data to disk as feather file... ", end=" ")
    res.to_feather("midnattsloppet_result_Stockholm_2025_Individual_10k.feather")
    print("Done!")