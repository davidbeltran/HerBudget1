from PyPDF2 import PdfReader
import regex as re
from database import Database
import os

class Statement:
    def __init__(self, pdfDocument):
        self.pdfDocument = pdfDocument
        self.reDetail = ('(?:\n((?:0[1-9]|1[1,2])/(?:0[1-9]|[12][0-9]|3[01]))\s*(.+)'
            + ' ((?:-\d+\.\d{2})|(?:\d+\.\d{2})))')

    def __checkDuplicatePdf(self):
        fileName = "idStore.txt"
        if not self.__searchForPdfFile(fileName):
            try:
                f = open(fileName, "a")
                f.write(self.pdfDocument + "\n")
                f.close()
                return False
            except IOError:
                print("Error writing to file")
        else:
            print(self.pdfDocument + " has already been processed.")
        return True

    def __searchForPdfFile(self, fileName):
        if os.path.exists(fileName):
            try:
                f = open(fileName, "r")
                if re.match(self.pdfDocument, f.read()):
                    f.close()
                    return True
                f.close()
                return False
            except IOError:
                print("Error reading file")
        return False
    
    def __getYear(self):
            yearRegex = re.compile(r'\d{2}')
            yearReSearch = yearRegex.search(self.pdfDocument)
            return yearReSearch.group()

    def __preparePdf(self):
        reader = PdfReader(self.pdfDocument)
        pg = reader.pages[2]
        return pg.extract_text()
    
    def __createExpenseList(self):
        pdfTxt = self.__preparePdf()
        return self.__castDateAmount(re.findall(self.reDetail, pdfTxt))
    
    def __castDateAmount(self, strExpenseList):
        expenseList = []
        for exp in strExpenseList:
            temp = []
            temp.append(f"{exp[0]}/{self.__getYear()}")
            temp.append(exp[1])
            temp.append(exp[2])
            expenseList.append(temp)
        return expenseList
    
    def sendToDatabase(self):
        if not self.__checkDuplicatePdf():
            db = Database(self.__createExpenseList())
            db.createExpenseTable()
            db.fillExpenseTable()

    def showExpenses(self):
        for expense in self.expenseList:
            print(expense)

    def practice(self):
        print()