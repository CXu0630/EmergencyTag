class EmInfoLength():
    def __init__(self):
        info_page_dict = {}
        info_page_dict['name'] = (4, 8)
        info_page_dict['blood_type'] = (9, 9)
        info_page_dict['em_contact'] = (10, 14)
        info_page_dict['birth_date'] = (15, 16)
        info_page_dict['allergies'] = (17, 26)
        info_page_dict['med_history'] = (27, 31)
        info_page_dict['nonce'] = (32, 35)
        self.info_page_dict = info_page_dict
    '''
    calculate byte availability for each category
    '''
    def byte_length(self, category):
        if category not in self.info_page_dict:
            raise KeyError(f"Category '{category}' not found in info_page_dict.")
        byte_length = self.get_num_pages(category) * 4
        return byte_length
    '''
    check if the information length fits into the byte availability, returns negative when string length exceeds
    byte length, positive when string length is below byte length, 0 when string length is equal to byte length
    '''
    def check_str_length(self, category, info):
        return self.byte_length(category) - len(info)
    
    def trim_string(self, category, info):
        if self.check_str_length(category, info) < 0:
            info = info[:self.byte_length(category)]
        return info
    
    def get_start_page(self, category):
        return self.info_page_dict[category][0]
    
    def get_page_range(self, category):
        return self.info_page_dict[category]

    def get_num_pages(self, category):
        return (self.info_page_dict[category][1] - self.info_page_dict[category][0] + 1)
# if __name__ == "__main__":
#     em_info = EmInfoLength()
#     try:
#         print(em_info.byte_length('name'))  # Should print byte length for 'name'
#         print(em_info.byte_length('blood_type'))  # Should print byte length for 'blood_type'
#         print(em_info.byte_length('unknown'))  # This will raise an error
#     except KeyError as e:
#         print(e)