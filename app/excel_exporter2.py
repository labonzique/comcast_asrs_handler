import pandas as pd
import os
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)


class ExcelExporter:
    def __init__(self, filename="output.xlsx", column_order=None, delete_if_exists = False):
        self.delete_if_exists = delete_if_exists
        self.filename = filename
        self.column_order = column_order
        self.executor = ThreadPoolExecutor(max_workers=2)  # Thread pool with two workers

    def save_to_excel(self, data):
        df = pd.DataFrame(data)
        
        if self.column_order:
            columns = [col for col in self.column_order if col in df.columns]
            df = df[columns]
        
        if os.path.exists(self.filename):
            logger.info(f"Excel file '{self.filename}' already exists and will be overwritten.")

        df.to_excel(self.filename, index=False, engine="openpyxl")
        logger.info(f"Excel file '{self.filename}' created or overwritten successfully.")
        return True  # Indicate success
    
    def open_excel_file(self):
        if os.path.exists(self.filename):
            if platform.system() == "Windows":
                os.startfile(self.filename)
            elif platform.system() == "Darwin":
                subprocess.call(["open", self.filename])
            else:
                subprocess.call(["xdg-open", self.filename])
            logger.info(f"Excel file '{self.filename}' opened successfully.")
        else:
            logger.info(f"File '{self.filename}' does not exist.")

    def export_and_open(self, data):
        # Submit save_to_excel task and wait for it to complete
        save_task = self.executor.submit(self.save_to_excel, data)
        if save_task.result():  # Wait for save_to_excel to complete and check success
            self.open_excel_file()  # Only open file if it was saved successfully

    def delete_excel_file(self):
        """
        Deletes the Excel file if it exists.
        """
        try:
            if self.delete_if_exists == True:
                os.remove(self.filename)
                logger.info(f"Excel file '{self.filename}' has been deleted.")
            else:
                logger.info(f"Excel file '{self.filename}' does not exist, so it cannot be deleted.")
        except FileNotFoundError: pass


    def close_executor(self):
        self.executor.shutdown(wait=True)
        logger.info("Executor closed.")
