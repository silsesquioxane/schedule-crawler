import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright

from env import password, user_id

columns = ["Subject", "Start Date", "Start Time", "End Time", "Description"]


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://learning.bcgrise.com/bcgrise/Login/Login.aspx")
    page.get_by_placeholder("User ID").fill(user_id)
    page.get_by_placeholder("Password").fill(password)
    page.get_by_placeholder("Password").press("Enter")
    page.get_by_role("link", name="2 Class").click()
    page.wait_for_load_state("networkidle")

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    venues = soup.find_all("td", {"data-th": "Venue"})
    urls = [td.find("a")["href"] for td in venues if td.find("a")]

    df = pd.read_html(html)[0]

    df["Description"] = urls
    df["Start Date"] = df["Class Date"]
    df["Start Time"] = df["Class Time"].str[:5]
    df["End Time"] = df["Class Time"].str[-5:]
    df["Subject"] = df["Topic"].str.replace("–", "-")

    df = df.replace(to_replace="\u200b", value="", regex=True)
    df = df.reindex(columns=columns)

    df.to_csv("TFIP BCG AI 2023 Calender.csv", index=False, encoding="utf-8")
    print(f"Job's done!\n{df}")

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
