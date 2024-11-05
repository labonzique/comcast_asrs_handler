import logging
import pandas as pd
from config import Config
from utils.logging_config import setup_logging
from app.file_management import FileManager
from app.data_processing import DataProcessor
from app.excel_exporter2 import ExcelExporter


def main():
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Directories for saving PDFs and text files
    pdf_save_directory = "./asr_pdfs"
    msg_directory = "./mail_asrs"
    txt_directory = "./tmp_txt"
    pdf_directory = "./tmp_pdf"


    # Initialize the FileManager with directories for saving files
    file_manager = FileManager(pdf_directory, txt_directory)
    processor = DataProcessor(txt_directory)
    exporter = ExcelExporter(filename="output.xlsx", column_order=Config.EXCEL_COLUMNS, delete_if_exists=True)

    exporter.delete_excel_file()

    # Process .msg files to extract PDFs
    # logger.info("------Starting .msg file processing------")
    file_manager.process_msg_directory(msg_directory, pdf_save_directory)
    logger.info("------Completed .msg files processing------")


    # Process PDF files to extract and save text content
    # logger.info("------Starting PDF files processing------")
    file_manager.process_pdf_directory()
    logger.info("------Completed PDF files processing------")


    # Parse text files in the directory
    # logger.info("------Starting text files parsing------")
    parsed_data = processor.parse_text_folder()
    logger.info("------Completed text files parsing------")


    # Process OF data with deduplication and short code extraction
    # logger.info("------Starting OF data processing------")
    processed_data = processor.process_data(parsed_data)
    logger.info(processed_data)
    logger.info("------Completed OF data processing------")


    # Process OF data with deduplication and short code extraction
    # logger.info("------Preparing final cut------")
    complete_data = processor.complete_data(processed_data)
    logger.info(complete_data)
    logger.info("------Data preparation is complete------")


    # # Excel file
    exporter.export_and_open(complete_data)
    logger.info("------Excel file created------")

    # Clear all files in the save directories after processing
    file_manager.clear_all_directories()
    logger.info("------Temporary files cleared successfully------")

    exporter.close_executor()
    logger.info("------Excel executor finished working------")

if __name__ == "__main__":
    main()
