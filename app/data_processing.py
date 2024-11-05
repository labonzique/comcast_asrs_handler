import os
import re
import logging
import copy

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def parse_text_folder(self): # This one is okay
        results = []
        logger.info("Starting to parse text files in folder: %s", self.folder_path)

        for filename in os.listdir(self.folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.folder_path, filename)
                
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()

                # Extract value starting with 'OF'
                of_pattern = r"\bOF\w+\b"
                of_match = re.search(of_pattern, text)
                of_value = of_match.group(0) if of_match else None

                # Extract value after 'FA'
                # fa_pattern = r"FA\s+(\d+)"
                fa_pattern = r"FA\s*:?\s*(\d{8})"
                fa_match = re.search(fa_pattern, text)
                fa_value = fa_match.group(1) if fa_match else None

                # Extract text between 'REMARKS' and 'BILLNM'
                remarks_pattern = r"REMARKS([\s\S]*?)BILLNM"
                remarks_match = re.search(remarks_pattern, text)
                remarks_text = remarks_match.group(1).replace("\n", " ").strip() if remarks_match else None

                # Extract and format date
                date_pattern = r"(\b2\s02.+):"
                date_match = re.search(date_pattern, text)
                if date_match:
                    raw_date = date_match.group(1).replace(" ", "")
                    formatted_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
                else:
                    formatted_date = None

                # Store the extracted data
                result = {
                    "of": of_value,
                    "fa": fa_value,
                    "remarks": remarks_text,
                    "filename": filename,
                    "date": formatted_date
                }
                results.append(result)
                logger.info("Parsed file: %s", filename)

        return results


    @staticmethod
    def trim_to_last_digits(value):
        digit_count = 0
        last_digit_index = None
        
        try:
            for i in range(len(value) - 1, -1, -1):
                if value[i].isdigit():
                    digit_count += 1
                    if last_digit_index is None:
                        last_digit_index = i
                else:
                    if digit_count >= 3:
                        return value[:last_digit_index + 1]
                    digit_count = 0
                    last_digit_index = None
        except TypeError: None

        return value if digit_count < 3 else value[:last_digit_index + 1]


    def process_data(self, data):
        result = {}
        logging.info("Processing OF data")
        data = copy.deepcopy(data)
        
        for item in data:
            item['of_short'] = self.trim_to_last_digits(item['of']) 
            
            if item['of_short'] in result:
                # Add the value 'of' to the all_of list
                result[item['of_short']]['all_of'].append(item['of'])
                # Add filename to the all_files list
                result[item['of_short']]['all_files'].append(item['filename'].replace(".txt", ".pdf"))
            else:
                item['all_of'] = [item['of']]  # Create a list with the initial value 'of'
                item['all_files'] = [item['filename'].replace(".txt", ".pdf")]  # Create a list with the first file
                # Delete unnecessary keys
                del item['of']
                del item['filename']
                # Add the processed item to the result
                result[item['of_short']] = item
        
        logger.info("Completed processing OF data")
        return list(result.values())


    def complete_data(self, data):
        prep_data = data.copy()
        filtered_data = {}
        for item in prep_data:
            try:
                remaining_ofs = item['all_of'][:]
                
                for of_value in remaining_ofs:
                    # Apply regular expression filters
                    if re.match(r"\b\w*E1\w*\b", of_value):
                        filtered_data["pon1"] = of_value
                        item['all_of'].remove(of_value)
                    elif re.match(r"\b\w*E2\w*\b", of_value):
                        filtered_data["pon2"] = of_value
                        item['all_of'].remove(of_value)
                    else: 
                        filtered_data["uni"] = of_value
                        item['all_of'].remove(of_value)

                # Check if the 'all_of' list is empty
                if not item['all_of']:
                    del item['all_of']
            except Exception as e:
                logger.error(f"Error: {e}")
            
            item.update(filtered_data)

        return prep_data




# import os
# import re
# import logging
# from typing import List, Dict

# logger = logging.getLogger(__name__)

# class DataProcessor:
#     def __init__(self, folder_path: str):
#         self.folder_path = folder_path
    
#     def parse_text_folder(self) -> List[Dict[str, str]]:
#         results = []
#         logger.info("Starting parsing of text files in folder: %s", self.folder_path)
        
#         for filename in os.listdir(self.folder_path):
#             if filename.endswith('.txt'):
#                 file_path = os.path.join(self.folder_path, filename)
                
#                 with open(file_path, "r", encoding="utf-8") as file:
#                     text = file.read()

#                 of_value = self._extract_of(text)
#                 fa_value = self._extract_fa(text)
#                 remarks_text = self._extract_remarks(text)
#                 date = self._extract_date(text)

#                 result = {
#                     "of": of_value,
#                     "fa": fa_value,
#                     "remarks": remarks_text,
#                     "filename": filename,
#                     "date": date
#                 }
#                 results.append(result)
#                 logger.info("Parsed file: %s", filename)
                
#         return results

#     @staticmethod
#     def _extract_of(text: str) -> str:
#         match = re.search(r"\bOF\w+\b", text)
#         return match.group(0) if match else None

#     @staticmethod
#     def _extract_fa(text: str) -> str:
#         match = re.search(r"FA\s+(\d+)", text)
#         return match.group(1) if match else None

#     @staticmethod
#     def _extract_remarks(text: str) -> str:
#         match = re.search(r"REMARKS([\s\S]*?)BILLNM", text)
#         return match.group(1).replace("\n", " ").strip() if match else None

#     @staticmethod
#     def _extract_date(text: str) -> str:
#         match = re.search(r"(\b2\s02.+):", text)
#         if match:
#             raw_date = match.group(1).replace(" ", "")
#             return f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
#         return None

#     def trim_to_last_digits(self, value: str) -> str:
#         digit_count = 0
#         last_digit_index = None
        
#         for i in range(len(value) - 1, -1, -1):
#             if value[i].isdigit():
#                 digit_count += 1
#                 if last_digit_index is None:
#                     last_digit_index = i
#             else:
#                 if digit_count >= 3:
#                     return value[:last_digit_index + 1]
#                 digit_count = 0
#                 last_digit_index = None
        
#         return value if digit_count < 3 else value[:last_digit_index + 1]

#     def process_of_data(self, data: List[Dict[str, str]]) -> List[Dict[str, str]]:
#         result = {}
#         logger.info("Processing OF data with deduplication")
        
#         for item in data:
#             item['OF_short'] = self.trim_to_last_digits(item['of'])
            
#             if item['OF_short'] in result:
#                 result[item['OF_short']]['other_of'].append(item['of'])
#             else:
#                 item['other_of'] = []
#                 result[item['OF_short']] = item
        
#         logger.info("Completed processing of OF data")
#         return list(result.values())



#     def prep_to_ss(self, data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    
#         prep_data = []
#         data_copy = data.copy()
        
#         for item in data_copy:
#             prep_inst = {}
#             item['of_short'] = self.trim_to_last_digits(item['of'])
#             prep_inst['of_short'] = item.get("of_short")
#             prep_inst['all_ofs'] = [i['of'] for i in data if i.get('of_short') == prep_inst['of_short']]
#             prep_inst['all_files'] = [i['filename'] for i in data if i.get('of_short') == prep_inst['of_short']]
            
#             for key, value in item.items():
#                 if key not in prep_inst and key not in ("of", "filename"):
#                     prep_inst[key] = value
            
#             prep_data.append(prep_inst)
        
#         prep_data.reverse()
#         unique_data = self._remove_duplicates(prep_data)
#         logger.info("Preparation of data for Smartsheet completed")
        
#         return unique_data


#     @staticmethod
#     def _remove_duplicates(prep_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
#         unique_data = []
#         check_of = set()
        

#         for item in prep_data:
#             if item["of_short"] not in check_of:
#                 check_of.add(item["of_short"])
#                 unique_data.append(item)

#         for item in unique_data:
#             filtered_data = {}
#             remaining_ofs = item['all_ofs'][:]
            
#             for of_value in remaining_ofs:
#                 if re.match(r"\b\w*E1\w*\b", of_value):
#                     filtered_data["pon1"] = of_value
#                     item['all_ofs'].remove(of_value)
#                 elif re.match(r"\b\w*E2\w*\b", of_value):
#                     filtered_data["pon2"] = of_value
#                     item['all_ofs'].remove(of_value)
#                 else: 
#                     filtered_data["uni"] = of_value
#                     item['all_ofs'].remove(of_value)
            
#             if not item['all_ofs']:
#                 del item['all_ofs']
                
#             item.update(filtered_data)
        
#         logger.info("Duplicate removal completed for OF data")
#         return unique_data
