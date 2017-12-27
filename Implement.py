from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from urllib.request import Request, urlopen
import sys
import tD_ui

class HelloWorld(QMainWindow, tD_ui.Ui_MainWindow):

    # defining constructor
    def __init__(self):

        QMainWindow.__init__(self)

        self.setupUi(self)

        self.setWindowTitle("Downloader")
        self.pushButton.clicked.connect(self.getStarted)
        self.setWindowIcon(QIcon(':/download.png'))


    def getStarted(self):

        self.putValues()

    def getContent(self):


        search_term=self.searchBar.text()
        search_term=search_term.replace(" ","+")

        try:
            url = "https://zooqle.com/search?q="+search_term+"%20category%3AApps&s=dt&v=t&sd=d"
            response = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            web_byte = urlopen(response).read()  # server returns a byte object
            webpage = web_byte.decode('utf-8')  # making it a string object
            print(webpage)

            return webpage
        except(Exception):
            QMessageBox.warning(self, "Warning", "Check your internet connection!") #exception if internet is not there
            return







    def putValues(self):


        # Data
        webpage = self.getContent()  # getting webpage from getContent method or throws exception if internet is not there

        self.tableWidget.setRowCount(30)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Size', 'Age', 'Health'])

        # Hide vertical header
        vheader = self.tableWidget.verticalHeader()
        vheader.setVisible(False)

        # Add Header
        header = self.tableWidget.horizontalHeader()
        # resizing first column
        header.setResizeMode(0, QHeaderView.Stretch)
        # removing editing capabilities from QTableWidget
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        # adjusting selection behaviour to select only one row
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        start=0
        for x in range(30):
            start = webpage.index('<a class=" small"', start+1)
            stop = webpage.index('</tr>', start)
            scraped_content = webpage[start:stop] # scarped xth row of the site

            # name of the item
            name_start='>'
            start_name = scraped_content.index(name_start)
            stop_name = scraped_content.index('</a>',start_name)
            scraped_name=scraped_content[start_name+len(name_start):stop_name]
            scraped_name = scraped_name.replace("(<hl>", "")
            scraped_name = scraped_name.replace("</hl>)", "")
            scraped_name = scraped_name.replace("<hl>", "")
            scraped_name = scraped_name.replace("</hl>", "")
            self.tableWidget.setItem(x, 0, QTableWidgetItem(scraped_name))

            # size of the item
            size_start='%">'
            start_size = scraped_content.index(size_start)
            stop_size = scraped_content.index('</div', start_size)
            scraped_size = scraped_content[start_size + len(size_start):stop_size]
            item=QTableWidgetItem(scraped_size)
            item.setTextAlignment(Qt.AlignCenter) # aligning to center
            self.tableWidget.setItem(x, 1, item)


            # age of the item
            age_start='class="text-nowrap text-muted smaller">'
            start_age = scraped_content.index(age_start,stop_size)
            stop_age = scraped_content.index('</td',start_age)
            scraped_age = scraped_content[start_age+len(age_start):stop_age]
            item = QTableWidgetItem(scraped_age)
            item.setTextAlignment(Qt.AlignCenter) # aligning to center
            self.tableWidget.setItem(x, 2,item)

            # health of the item
            health_start='Seeder'
            start_health = scraped_content.index(health_start, stop_age)
            stop_health = scraped_content.index('| ', start_health)
            scraped_health = scraped_content[start_health:stop_health]
            item = QTableWidgetItem(scraped_health)
            item.setTextAlignment(Qt.AlignCenter) # aligning to center
            self.tableWidget.setItem(x, 3, item)






app = QApplication(sys.argv)
helloworld = HelloWorld()



helloworld.show()
app.exec_()