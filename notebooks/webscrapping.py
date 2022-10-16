# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: 'Python 3.10.0 (''ambiente_virtual'': venv)'
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup

import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# %%
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")

# Set path to chromedriver as per your configuration
# homedir = os.path.expanduser("~")
webdriver_service = Service("/chromedriver/stable/chromedriver")

# Choose Chrome Browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Get page

# %% [markdown]
# # WBNA Salaries

# %%
df = pd.read_html(
    "https://www.spotrac.com/wnba/rankings/2022/cap-hit/"
)  # The year 2022 were select in the web page
df = df[0]
df = df.iloc[:, 1:]
df

# %%
df["Player"] = df["Player"].astype("string")
df["Team"] = df["Player"].str.split(" ")
df["Team"] = [text[-1] for text in df["Team"]]
df["Team"] = df["Team"].astype("string")
df["Player"] = [
    player.replace("  " + team, "") for player, team in zip(df["Player"], df["Team"])
]
df


# %%
df["cap hit"] = df["cap hit"].astype("string")
df["cap hit"] = df["cap hit"].str.replace("$", "")
df["cap hit"] = df["cap hit"].str.replace(",", "")
df["cap hit"] = df["cap hit"].astype("int64")
df.info()
df

# %% [markdown]
# # WNBA avarage attendance


# %%
url = "https://www.acrossthetimeline.com/wnba/attendance.html"
browser.get(url)

# %%
soup = BeautifulSoup(browser.page_source)
table = soup.find_all("table")
table = pd.read_html(str(table))
table = table[0]
table
