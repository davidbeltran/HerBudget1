from PyPDF2 import PdfReader
import regex as re
import os
import datetime

class WorkerPDF:
    def __init__(self, fileStorage, pdfDoc):
        self.fileStorage = fileStorage
        self.reDetail = ('(?:\n((?:0[1-9]|1[1,2])/(?:0[1-9]|[12][0-9]|3[01]))\s*(.+)'
            + ' ((?:-\d+\.\d{2})|(?:\d+\.\d{2})))')
        self.reYear = r'\d{2}'
        self.pdfDoc = pdfDoc

    def __searchForPdfFile(self, fileName):
        if os.path.exists(fileName):
            try:
                f = open(fileName, "r")
                if re.match(self.pdfDoc, f.read()):
                    f.close()
                    return True
                f.close()
                return False
            except IOError:
                print("Error reading file")
        return False
    
    def checkDuplicatePdf(self):
        if not self.__searchForPdfFile(self.fileStorage):
            try:
                f = open(self.fileStorage, "a")
                f.write(self.pdfDoc + "\n")
                f.close()
                return False
            except IOError:
                print("Error writing to file")
        else:
            print(self.pdfDoc + " has already been processed.")
        return True
    
    def __getYear(self):
            yearRegex = re.compile(self.reYear)
            yearReSearch = yearRegex.search(self.pdfDoc)
            return yearReSearch.group()
    
    def __turnToDate(self, dateStr):
        format = "%m/%d/%y"
        dt = datetime.datetime.strptime(dateStr, format)
        return dt.date()

    def __castDateAmount(self, strExpenseList):
        expenseList = []
        for exp in strExpenseList:
            temp = []
            temp.append(self.__turnToDate(f"{exp[0]}/{self.__getYear()}"))
            temp.append(exp[1])
            temp.append(float(exp[2]))
            expenseList.append(temp)
        return expenseList
    
    def __preparePdf(self):
        reader = PdfReader(self.pdfDoc)
        pg = reader.pages[2]
        return pg.extract_text()
    
    def createExpenseList(self):
        pdfTxt = self.__preparePdf()
        return self.__castDateAmount(re.findall(self.reDetail, pdfTxt))