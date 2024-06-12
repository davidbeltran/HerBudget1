from PyPDF2 import PdfReader
import regex as re
from database import Database
import os

class Statement:
    def __init__(self, pdfDocument):
        self.pdfDocument = pdfDocument
        self.reDetail = ('(?:\n((?:0[1-9]|1[1,2])/(?:0[1-9]|[12][0-9]|3[01]))\s*(.+)'
            + ' ((?:-\d+\.\d{2})|(?:\d+\.\d{2})))')
        self.expenseList = []

    def __checkDuplicatePdf(self):
        fileName = "idStore.txt"
        if not self.__searchPdf(fileName):
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

    def __searchPdf(self, fileName):
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

    def __preparePdf(self):
        reader = PdfReader(self.pdfDocument)
        pg = reader.pages[2]
        return pg.extract_text()
    
    def __createExpenseList(self):
        pdfTxt = self.__preparePdf()
        self.expenseList = re.findall(self.reDetail, pdfTxt)
        return self.expenseList
    
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