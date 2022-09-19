import pdfplumber
class pdftoexcel:

    def __init__(self, path) -> None:
        self.__path = path


    def get_data_from_pdf(self):
        with pdfplumber.open(self.__path) as pdf:
            __first_page = pdf.pages[0]
            __extracted_tabel = __first_page.extract_table() 
            self.__Employees_social_security_number = __extracted_tabel[0][2].split("\n")
            self.__ein = __extracted_tabel[1][0].split("\n")
            self.__full_address = __extracted_tabel[2][0].split("\n")
            self.__control_number = __extracted_tabel[5][0].split("\n")

            
            def exists(a):
                try:
                    return " ".join(a[1:])
                except:
                    return None
    
            return {
                self.__Employees_social_security_number[0]:exists(self.__Employees_social_security_number), 
                self.__ein[0]: exists(self.__ein), 
                self.__full_address[0]: self.__full_address[1:],
                self.__control_number[0]: exists(self.__control_number),
            }