import pandas as pd
import numpy as np

from datetime import datetime
from dateutil.relativedelta import relativedelta

from pathlib import Path
db_function = str(Path.cwd().parent.parent / "function")
file_path = str(Path.cwd().parent.parent / "files")
fetch_path = file_path + r"\function"

import sys
sys.path.append(db_function)
sys.path.append(file_path)
sys.path.append(fetch_path)

from dotenv import load_dotenv

from access_db import access_db
from get_cols import get_cols
from round_float64_columns import round_float64_columns
from adjust_day_for_temp import adjust_day_based_on_tm_and_hour

import os

import requests

# file fetch
from get_temperature import get_temperature
from wide_temperature import wide_temperature

# github url
from github_upload_url import main

# create md
from create_md import create_md

# telegram
from Telegrambot import TelegramBot

import glob

# load environment file
try:
    load_dotenv()

    # 🔹 특정 경로의 모든 .md 파일 삭제
    md_files = list(Path(os.getcwd()).glob("*.md"))

    for md_file in md_files:
        try:
            os.remove(md_file)
            print(f"🗑️ 삭제 완료: {md_file}")
        except Exception as e:
            print(f"❌ 삭제 실패: {md_file}, 오류: {e}")

    # # connect to db
    # host = os.getenv("HOST")
    # user = os.getenv("USER")
    # pw = os.getenv("PW")
    # target_db = os.getenv("iMAES_DB")

    # cur, conn = access_db(host, user, pw, target_db)

    # # temperature cols
    # target_table = "temperature"
    # temperature_cols = get_cols(cur, target_table)

    # # fetch `temperature table`
    # get_temperature(cur, temperature_cols, round_float64_columns)

    # # temperature file
    # temp_fname = [v for v in os.listdir(file_path) if v.startswith("temperature")][0]
    # wide_temp_fname = [v for v in os.listdir(file_path) if v.startswith("temperature_wide")][0]

    # # create wide temp.xlsx file
    # wide_temperature(file_path, temp_fname)

    # temperature file
    temp_fname = [v for v in os.listdir(file_path) if v.startswith("temperature")][0]
    temp_wide_fname = [v for v in os.listdir(file_path) if v.startswith("temperature_wide")][0]

    file_list = [temp_fname, temp_wide_fname]
    download_links = main(temp_fname, file_path, file_list)

    title = f"{datetime.today().strftime('%Y-%m-%d')}기준 기온 데이터"
    content = f"""

    {datetime.today().strftime('%Y-%m-%d')}기준 기온 데이터입니다.

    1. [Long version]({download_links[0]})
    2. [Wide version]({download_links[1]})
    """
    create_md(title, content, os.getcwd())

except Exception as e:
    # telegram bot 생성
    iMAES_TELEGRAM_TOKEN = "iMAES_TELEGRAM_TOKEN"
    iMAES_TELEGRAM_CHANNEL_ID = "iMAES_TELEGRAM_CHANNEL_ID"
    bot = TelegramBot(iMAES_TELEGRAM_TOKEN, iMAES_TELEGRAM_CHANNEL_ID)

    text = f"{datetime.today().strftime('%Y-%m-%d')} github page업로드가 실패했습니다 : {e}"
    bot.send_message(text)