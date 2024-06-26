"""
Author: David Beltran
"""
from PyPDF2 import PdfReader
import regex as re
import os
import datetime

# Class constructor
class WorkerPDF:
    def __init__(self, fileStorage, pdfDoc):
        self.fileStorage = fileStorage
        self.reDetail = ('(?:\n((?:0[1-9]|1[1,2])/(?:0[1-9]|[12][0-9]|3[01]))\s*(.+)'
            + ' ((?:-\d+\.\d{2})|(?:\d+\.\d{2})))')# RegEx string for finding expense info
        self.reYear = r'\d{2}'# Regex string for finding year from PDF file
        self.pdfDoc = pdfDoc

    """
    Reads through idStore.txt to find if PDF file name exists
    """
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
    
    """
    Ensures PDF file not already processed.
    Writes PDF file name to idStore.txt file if not already processed
    """
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
    
    """
    Uses Regex library and RegEx string to find year from PDF file name
    """
    def __getYear(self):
            yearRegex = re.compile(self.reYear)
            yearReSearch = yearRegex.search(self.pdfDoc)
            return yearReSearch.group()
    
    """
    Takes expense string date and converts to datetime type
    """
    def __turnToDate(self, dateStr):
        format = "%m/%d/%y"
        dt = datetime.datetime.strptime(dateStr, format)
        return dt.date()

    """
    Fills list with correctly casted data types for Date and Amount
    """
    def __castDateAmount(self, strExpenseList):
        expenseList = []
        for exp in strExpenseList:
            temp = []
            temp.append(self.__turnToDate(f"{exp[0]}/{self.__getYear()}")) # Date
            temp.append(exp[1]) # Details
            temp.append(float(exp[2])) # Amount
            expenseList.append(temp)
        return expenseList
    
    """
    Scrapes PDF text from page 2 of PDF file and converts into single string
    """
    def __preparePdf(self):
        reader = PdfReader(self.pdfDoc)
        pg = reader.pages[2]
        return pg.extract_text()
    
    """
    Returns fully casted list of expenses only from PDF file
    """
    def createExpenseList(self):
        pdfTxt = self.__preparePdf()
        return self.__castDateAmount(re.findall(self.reDetail, pdfTxt))