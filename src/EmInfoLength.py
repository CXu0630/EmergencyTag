class EmInfoLength():
    def __init__(self):
        info_page_dict = {}
        info_page_dict['name'] = (4, 8)
        info_page_dict['blood_type'] = (9, 9)
        info_page_dict['em_contact'] = (10, 14)
        info_page_dict['birth_date'] = (15, 16)
        info_page_dict['allergies'] = (17, 26)
        info_page_dict['med_history'] = (27, 32)
        self.info_page_dict = info_page_dict
    def byte_length(self, category):
        if category not in self.info_page_dict:
            raise KeyError(f"Category '{category}' not found in info_page_dict.")
        byte_length = (self.info_page_dict[category][1] - self.info_page_dict[category][0] + 1)*4
        return byte_length
# if __name__ == "__main__":
#     em_info = EmInfoLength()
#     try:
#         print(em_info.byte_length('name'))  # Should print byte length for 'name'
#         print(em_info.byte_length('blood_type'))  # Should print byte length for 'blood_type'
#         print(em_info.byte_length('unknown'))  # This will raise an error
#     except KeyError as e:
#         print(e)