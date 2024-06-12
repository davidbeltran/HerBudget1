from PyPDF2 import PdfReader
import regex as re
from database import Database

class Statement:
    def __init__(self, pdfDocument):
        self.pdfDocument = pdfDocument
        self.reDetail = ('(?:\n((?:0[1-9]|1[1,2])/(?:0[1-9]|[12][0-9]|3[01]))\s*(.+)'
            + ' ((?:-\d+\.\d{2})|(?:\d+\.\d{2})))')
        self.expenseList = []

    def __preparePdf(self):
        reader = PdfReader(self.pdfDocument)
        pg = reader.pages[2]
        return pg.extract_text()
    
    def __createExpenseList(self):
        pdfTxt = self.__preparePdf()
        self.expenseList = re.findall(self.reDetail, pdfTxt)
        return self.expenseList
    
    def sendToDatabase(self):
        db = Database(self.__createExpenseList())
        db.createExpenseTable()
        db.fillExpenseTable()

    def showExpenses(self):
        for expense in self.expenseList:
            print(expense)
