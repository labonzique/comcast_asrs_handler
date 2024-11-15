import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_TOKEN = os.getenv("API_TOKEN")
    SHEET_ID = os.getenv("SHEET_ID")

    COLUMN_IDS = {
        'fa': int(os.getenv("FA_COLUMN_ID")),
        'remarks': int(os.getenv("REMARKS_COLUMN_ID")),
        'date': int(os.getenv("DATE_COLUMN_ID")),
        'pon1': int(os.getenv("PON1_COLUMN_ID")),
        'pon2': int(os.getenv("PON2_COLUMN_ID")),
        'uni': int(os.getenv("UNI_COLUMN_ID"))
    }
    EXCEL_COLUMNS = ["of_short",  "fa", "date", "uni", "pon1", "pon2", "remarks", "all_files"]
    