import gspread

class GoogleSheet:
    def __init__(self, credencials, document, sheet_name):
        self.gc = gspread.service_account_from_dict(credencials)
        self.sh = self.gc.open(document)
        self.sheet = self.sh.worksheet(sheet_name) 
        
    def write_data(self, range, data):
        self.sheet.update(range, data)
        
    def get_last_row_range(self):
        last_row = len(self.sheet.get_all_values()) + 1
        deta = self.sheet.get_values()
        range_start = f"A{last_row}"
        range_end = f"{chr(ord('A') + len(deta[0]) -1 )}{last_row}"    
        return f"{range_start}:{range_end}"   
