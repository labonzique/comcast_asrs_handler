import pandas as pd
import os
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)

class ExcelExporter:
    def __init__(self, filename="output.xlsx", column_order=None, delete_if_exists = False):
        """
        Initializes the ExcelExporter with an optional column order.
        
        :param filename: Name of the Excel file to save
        :param column_order: List specifying the order of columns in Excel
        """
        self.delete_if_exists = delete_if_exists
        self.filename = filename
        self.column_order = column_order
        self.executor = ThreadPoolExecutor(max_workers=2)  # Thread pool with two workers

    def save_to_excel(self, data):
        """
        Saves data to an Excel file, arranging columns based on the specified order.
        
        :param data: List of dictionaries with data to be saved
        """
        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(data)
        
        # Rearrange columns if column order is specified
        if self.column_order:
            # Filter out columns not present in the data to avoid KeyErrors
            columns = [col for col in self.column_order if col in df.columns]
            df = df[columns]
        
        # Check if file exists and log that it will be overwritten
        if os.path.exists(self.filename):
            logger.info(f"Excel file '{self.filename}' already exists and will be overwritten.")

        # Save DataFrame to Excel file
        df.to_excel(self.filename, index=False, engine="openpyxl")
        logger.info(f"Excel file '{self.filename}' created or overwritten successfully.")
    
    def open_excel_file(self):
        """
        Opens the Excel file in the associated application.
        """
        if os.path.exists(self.filename):
            if platform.system() == "Windows":
                os.startfile(self.filename)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", self.filename])
            else:  # Linux and other systems
                subprocess.call(["xdg-open", self.filename])
            logger.info(f"Excel file '{self.filename}' opened successfully.")
        else:
            logger.info(f"File '{self.filename}' does not exist.")

    def export_and_open(self, data):
        """
        Exports data to an Excel file and opens it in parallel.
        
        :param data: List of dictionaries with data to be saved
        """
        # Run file saving and opening tasks in parallel
        save_task = self.executor.submit(self.save_to_excel, data)
        save_task.add_done_callback(lambda x: self.executor.submit(self.open_excel_file))

    def close_executor(self):
        """
        Shuts down the ThreadPoolExecutor.
        """
        self.executor.shutdown(wait=True)
        logger.info("Executor closed.")


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
