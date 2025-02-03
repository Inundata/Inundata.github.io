import pandas as pd
import numpy as np

from datetime import datetime
from dateutil.relativedelta import relativedelta

from pathlib import Path
db_function = str(Path.cwd().parent.parent / "function")
file_path = str(Path.cwd().parent.parent / "files")
git_file_path = "https://raw.githubusercontent.com/Inundata/Inundata.github.io/main/files"
fetch_path = file_path + r"\function"

import sys
sys.path.append(db_function)
sys.path.append(file_path)
sys.path.append(fetch_path)

from dotenv import load_dotenv

from access_db import access_db
from get_cols import get_cols
from round_float64_columns import round_float64_columns

import os

import requests

# file fetch
from get_temperature import get_temperature

# load environment file
load_dotenv()

# db info
host = os.getenv("HOST")
user = os.getenv("USER")
pw = os.getenv("PW")
target_db = os.getenv("iMAES_DB")

# connect to db
cur, conn = access_db(host, user, pw, target_db)

# temperature cols
target_table = "temperature"
temperature_cols = get_cols(cur, target_table)

# fetch `temperature table`
get_temperature(cur, temperature_cols, round_float64_columns)