"""
Author: David Beltran
"""
from database import Database
from workerPdf import WorkerPDF

# Class constructor
class Statement:
    def __init__(self, pdfDocument):
        self.pdfDocument = pdfDocument
        self.reDetail = ('(?:\n((?:0[1-9]|1[1,2])/(?:0[1-9]|[12][0-9]|3[01]))\s*(.+)'
            + ' ((?:-\d+\.\d{2})|(?:\d+\.\d{2})))')
    
    """
    If PDF file has not been processed, list of expenses is sent to database
    """
    def sendToDatabase(self):
        wp = WorkerPDF("idStore.txt", self.pdfDocument)
        if not wp.checkDuplicatePdf():
            db = Database(wp.createExpenseList())
            db.fillExpenseTable()

    def practice(self):
        print()