import os
import logging
import smartsheet
from config import Config

logger = logging.getLogger(__name__)

class SmartsheetClient:
    def __init__(self, sheet_id: int, column_ids: dict, api_token: str = Config.API_TOKEN):
        """
        Initializes the Smartsheet client with necessary configuration.
        
        :param sheet_id: ID of the Smartsheet sheet
        :param column_ids: Dictionary mapping column names to Smartsheet column IDs
        :param api_token: API token for authenticating with Smartsheet
        """
        self.client = smartsheet.Smartsheet(api_token)
        self.sheet_id = sheet_id
        self.column_ids = column_ids

    def add_row_to_smartsheet(self, data: dict, pdf_directory: str):
        """
        Adds a row to the Smartsheet and attaches PDFs if provided.
        
        :param data: Dictionary containing row data and optionally 'all_files' for attachments
        :param pdf_directory: Directory where PDF files are stored
        """
        row = smartsheet.models.Row()
        row.to_bottom = True  # Add the row at the bottom of the sheet

        # Populate row cells with data
        for key, value in data.items():
            if key in self.column_ids:
                if isinstance(value, list):
                    value = ', '.join(value)
                row.cells.append({
                    'column_id': self.column_ids[key],
                    'value': value
                })

        try:
            # Add the row to Smartsheet
            response = self.client.Sheets.add_rows(self.sheet_id, [row])
            new_row_id = response.result[0].id
            logger.info("Row successfully added to Smartsheet.")

            # Attach PDFs if 'all_files' is present in data
            if 'all_files' in data:
                self._attach_files(new_row_id, data['all_files'], pdf_directory)

        except smartsheet.exceptions.ApiError as e:
            logger.error(f"Error adding row to Smartsheet: {e}")

    def _attach_files(self, row_id: int, files: list, pdf_directory: str):
        """
        Attaches PDF files to a Smartsheet row.

        :param row_id: The ID of the Smartsheet row to attach files to
        :param files: List of file names to attach (expected to have .txt extension)
        :param pdf_directory: Directory where PDF files are stored
        """
        for file_name in files:
            pdf_file_path = os.path.join(pdf_directory, file_name.replace('.txt', '.pdf'))

            if os.path.exists(pdf_file_path):
                try:
                    with open(pdf_file_path, 'rb') as pdf_file:
                        self.client.Attachments.attach_file_to_row(
                            self.sheet_id, 
                            row_id, 
                            (pdf_file_path, pdf_file, 'application/pdf')
                        )
                    logger.info(f"File {pdf_file_path} successfully attached.")
                except Exception as e:
                    logger.error(f"Error attaching file {pdf_file_path}: {e}")
            else:
                logger.warning(f"File {pdf_file_path} not found.")
