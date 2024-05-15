import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from scraper import main as scrape_main


class ScraperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sales Scraping Project')

        layout = QVBoxLayout()

        self.label = QLabel('Enter keyword:', self)
        layout.addWidget(self.label)

        self.keyword_input = QLineEdit(self)
        layout.addWidget(self.keyword_input)

        self.run_button = QPushButton('Run Scraper', self)
        self.run_button.clicked.connect(self.run_scraper)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def run_scraper(self):
        keyword = self.keyword_input.text()
        if keyword:
            asyncio.run(scrape_main(keyword))
            QMessageBox.information(self, 'Completed', 'Scraping completed. Check the products.html file.')
        else:
            QMessageBox.warning(self, 'Input Error', 'Please enter a keyword.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScraperApp()
    ex.show()
    sys.exit(app.exec_())