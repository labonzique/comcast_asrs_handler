import os
import logging
import extract_msg as msg
import pdfplumber

logger = logging.getLogger(__name__)

class FileManager:
    def __init__(self, pdf_save_directory: str, txt_save_directory: str):
        """
        Initializes the FileManager with directories for saving PDF and text files.
        
        :param pdf_save_directory: Directory to save extracted PDF files from .msg files
        :param txt_save_directory: Directory to save extracted text content from PDFs
        """
        self.pdf_save_directory = pdf_save_directory
        self.txt_save_directory = txt_save_directory

        # Ensure the directories exist
        os.makedirs(self.pdf_save_directory, exist_ok=True)
        os.makedirs(self.txt_save_directory, exist_ok=True)
        
    def extract_pdfs_from_msg(self, msg_path: str, pdf_save = None):
        """
        Extracts PDF attachments from a .msg file and saves them to the designated directory.
        
        :param msg_path: Path to the .msg file
        """
        try:
            msg_file = msg.Message(msg_path)
            for attachment in msg_file.attachments:
                if attachment.longFilename.endswith('.pdf'):
                    save_path = os.path.join(self.pdf_save_directory, attachment.longFilename)
                    
                    with open(save_path, 'wb') as pdf_file:
                        pdf_file.write(attachment.data)
                    logger.info(f"PDF saved: {attachment.longFilename}")

                    if pdf_save:
                        os.makedirs(pdf_save, exist_ok=True)
                        save_path2 = os.path.join(pdf_save, attachment.longFilename)
                        with open(save_path2, 'wb') as pdf_file:
                            pdf_file.write(attachment.data)
                        logger.info(f"PDF saved to directory 2: {attachment.longFilename}")

        except Exception as e:
            logger.error(f"Error occurred while processing {msg_path}: {e}")

    def process_msg_directory(self, directory: str, pdf_save_directory =None):
        """
        Processes all .msg files in the specified directory and extracts PDF attachments.
        
        :param directory: Directory containing .msg files
        """
        logger.info("Starting processing of .msg files in directory: %s", directory)
        for filename in os.listdir(directory):
            if filename.endswith('.msg'):
                msg_path = os.path.join(directory, filename)
                logger.info("Processing file: %s", filename)
                self.extract_pdfs_from_msg(msg_path, pdf_save_directory)
                logger.info("Finished processing file: %s", filename)
            else:
                logger.info("Skipped file (not .msg): %s", filename)


    def parse_pdf(self, pdf_path) -> str:
        """
        Parses the text content of the first page of a PDF file and saves it as a .txt file.
        
        :param pdf_path: Path to the PDF file
        :return: Extracted text from the PDF file
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                first_page_text = pdf.pages[0].extract_text() if pdf.pages else None
                
                if not first_page_text:
                    logger.warning(f"No text found on the first page of {os.path.basename(pdf_path)}")
                    return None

                logger.info(f"Text extracted from first page of {os.path.basename(pdf_path)}")

                txt_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
                txt_path = os.path.join(self.txt_save_directory, txt_filename)

                if not os.path.exists(txt_path):
                    with open(txt_path, "w", encoding="utf-8") as txt_file:
                        txt_file.write(first_page_text)
                    logger.info(f"Text file saved: {txt_filename}")
                else:
                    logger.info(f"Text file already exists: {txt_filename}")
                
                return first_page_text
        except Exception as e:
            logger.error(f"Error occurred while processing {pdf_path}: {e}")
            return None

    def process_pdf_directory(self):
        """
        Processes all PDF files in the specified directory and saves their text content as .txt files.
        """
        logger.info("Starting processing of PDF files in directory: %s", self.pdf_save_directory)
        
        for filename in os.listdir(self.pdf_save_directory):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_save_directory, filename)
                logger.info("Processing PDF file: %s", filename)
                self.parse_pdf(pdf_path)
            else:
                logger.info("Skipped file (not PDF): %s", filename)


    def clear_directory(self, directory: str):
        """
        Clears all files in the specified directory.
        
        :param directory: Directory to clear files from
        """
        try:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logger.info(f"Deleted file: {file_path}")
            logger.info(f"All files cleared from directory: {directory}")
        except Exception as e:
            logger.error(f"Error clearing directory {directory}: {e}")

    def clear_all_directories(self):
        """
        Clears all files in both pdf_save_directory and txt_save_directory.
        """
        logger.info("Clearing all files in PDF and text save directories")
        self.clear_directory(self.pdf_save_directory)
        self.clear_directory(self.txt_save_directory)

        





# import os
# import logging
# import extract_msg as msg
# import pdfplumber

# logger = logging.getLogger(__name__)


# # def create_temp_dir():
# #     """
# #     Создает временную директорию, возвращает путь к ней.
# #     """
# #     return tempfile.TemporaryDirectory()

# # def save_to_temp_file(content, file_name, temp_dir):
# #     """
# #     Сохраняет контент во временный файл в указанной временной директории.
# #     """
# #     file_path = os.path.join(temp_dir, file_name)
# #     with open(file_path, 'w') as file:
# #         file.write(content)
# #     return file_path


# def extract_pdfs_from_msg(msg_path, save_directory):
#     try:
#         msg_file = msg.Message(msg_path)
#         for attachment in msg_file.attachments:
#             if attachment.longFilename.endswith('.pdf'):
#                 save_path = os.path.join(save_directory, attachment.longFilename)
#                 with open(save_path, 'wb') as pdf_file:
#                     pdf_file.write(attachment.data)
#                 logging.info(f"PDF Saved: {attachment.longFilename}")
#     except Exception as e:
#         logging.error(f"Error occured while processing {msg_path}: {e}")



# def process_directory(directory, save_directory):
#     # Создаем директорию для сохранения вложений, если ее нет
#     os.makedirs(save_directory, exist_ok=True)
    
#     # Проходим по всем .msg файлам в директории
#     for filename in os.listdir(directory):
#         if filename.endswith('.msg'):
#             msg_path = os.path.join(directory, filename)
#             logging.info(f"File processing started: {filename}")
#             extract_pdfs_from_msg(msg_path, save_directory)
#             logging.info(f"File processing ended: {filename}")
#         else:
#             logging.info(f"Missed file (not PDF) (not .msg): {filename}")



# def parse_pdf(file_path, save_directory):
#     """
#     Function for parsing the contents of a PDF file.

#     """
#     try:
#         with pdfplumber.open(file_path) as pdf:
#             text_content = []
#             for i, page in enumerate(pdf.pages):
#                 if i == 0: 
#                     text = page.extract_text()
#                     if text:
#                         text_content.append(text)
#                         logging.info(f"Text extracted from page {i+1} из {os.path.basename(file_path)}")
#                     else:
#                         logging.warning(f"On the page {i+1} no text was found")
#                 else: logging.info(f"The first page has been read")
            
#             full_text = "\n".join(text_content)
#             logging.info(f"The text was successfully extracted from {file_path}")

#             txt_filename = os.path.splitext(os.path.basename(file_path))[0] + ".txt"
#             txt_path = os.path.join(save_directory, txt_filename)
            
#             if txt_filename not in os.listdir(save_directory):
#                 with open(txt_path, "w", encoding="utf-8") as txt_file:
#                     txt_file.write(full_text)
#                     logging.info(f"Text file has been added")
#             else: logging.info(f"A text file with this name exists")

#             return full_text
#     except Exception as e:
#         logging.error(f"Error occured while processing {file_path}: {e}")
#         return None


       
# def process_self.pdf_save_directory(self.pdf_save_directory, save_directory):
#     """
#     Function to process all PDF files in the specified directory and save their text.
#     """
#     # Create a directory for text files if there isn't one
#     os.makedirs(save_directory, exist_ok=True)
    
#     # Go through all PDF files in the directory
#     for filename in os.listdir(self.pdf_save_directory):
#         if filename.endswith('.pdf'):
#             self.pdf_save_directory = os.path.join(self.pdf_save_directory, filename)
#             parse_pdf(self.pdf_save_directory, save_directory)
#         else:
#             logging.info(f"Missed file (not PDF): {filename}")