
import sys
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, \
    QVBoxLayout,QHBoxLayout, QDesktopWidget, QFormLayout, QLabel, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from matplotlib.figure import Figure
from PRI.src.Back import Server


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Blue Ocean Whale Sharks'
        self.left = 200
        self.top = 200
        self.width = 700
        self.height = 100
        self.my_line_edit = QLineEdit()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('six_sigma.ico'))
        # self.my_line_edit = QtGui.QLineEdit()

        # self.my_line_edit.setStyleSheet("color: red;")
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.showMaximized()
        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: rgb(73,120,120);")


        # The dataframe
        self.df = pd.DataFrame()
        # The data for the data table
        self.gs = []
        # Initialize the labels for the first tab

        self.productLabel = QLabel("Product", self)
        self.productLabel.setStyleSheet("font: bold; font-size: 16px;")
        self.countryLabel = QLabel("Country", self)
        self.countryLabel.setStyleSheet("font: bold; font-size: 16px")

        # Initialise the textbox for all the labels along with the tooltips

        self.productTextBox = QLineEdit(self)
        self.productTextBox.setToolTip("Enter the product here")
        self.productTextBox.setStyleSheet("font: bold; font-size: 16px;")
        self.countryTextBox = QLineEdit(self)
        self.countryTextBox.setToolTip("Enter the country here")
        self.countryTextBox.setStyleSheet("font: bold; font-size: 16px;")




        # Canvas and Toolbar
        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # Buttons to be added to the first tab
        self.submitButton = QPushButton("Submit")
        self.submitButton.setToolTip("To submit and get results")
        self.submitButton.resize(self.submitButton.sizeHint())
        self.submitButton.clicked.connect(self.on_click)
        self.submitButton.setStyleSheet("background: white; height: 50px; max-width: 400px; font: bold; font-size: 30px; text-align: center")
        self.show()


        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.resize(self.clearAllButton.sizeHint())
        self.clearAllButton.setToolTip("To clear all the fields")
        self.clearAllButton.clicked.connect(self.clear_on_click)
        self.clearAllButton.setStyleSheet("background: white; font: bold;")

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabInput = QWidget()
        self.tabTrendingScore = QWidget()
        self.tabComparision = QWidget()
        self.tabRelated = QWidget()
        self.tabs.resize(480, 320)

        # Add tabs
        self.tabs.addTab(self.tabInput, "The Input Tab")
        self.tabs.addTab(self.tabTrendingScore, "The TrendingScore")
        self.tabs.addTab(self.tabComparision, "The Comparision")
        self.tabs.addTab(self.tabTrendingScore, "The TrendingScore")
        self.tabs.addTab(self.tabRelated, "Related")

        self.tabInputform = QFormLayout()

        self.tabInputform.addRow(self.productLabel,self.productTextBox)
        self.tabInputform.addRow(self.countryLabel,self.countryTextBox)
        self.tabInputform.addRow(self.clearAllButton,self.submitButton)


        self.tabInput.setLayout(self.tabInputform)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Canvas and Toolbar
        # a figure instance to plot on
        self.figure = Figure(figsize=(100,100))
        self.figure.suptitle('Trending search score')
        self.figureComp = Figure(figsize=(100,100))
        self.figureComp.suptitle('Analog VS Digital')
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.canvasComp = FigureCanvas(self.figureComp)
        # this is the Navigation widget
        # Set a table to show the data
        self.tabTrendingScoreForm = QFormLayout()
        self.tabTrendingScoreFormsub = QHBoxLayout()


        self.tabComparisionForm = QFormLayout()
        self.tabComparisionFormSub = QHBoxLayout()
        self.tabRelatedForm = QFormLayout()
        self.tabRelatedBox = QHBoxLayout()

        self.font = QtGui.QFont("Times", 8, QtGui.QFont.Bold)


        self.widgetRelatedTopics = QTableWidget()
        self.widgetRelatedQuery = QTableWidget()
        self.widgetRelatedTopics.adjustSize()
        self.widgetRelatedTopics.setMaximumSize(1500,16000)
        self.widgetRelatedQuery.setMaximumSize(1500,1600)
        self.widgetRelatedTopics.horizontalHeader().setStretchLastSection(True)
        self.widgetRelatedQuery.horizontalHeader().setStretchLastSection(True)
        self.recommendationText = QLabel()
        self.recommendationText.setMinimumSize(800,200)
        self.recommendationText.setToolTip("This tab shows the recommendation ")
        self.relQuerry = QLabel('Related Query')
        self.relQuerry.setStyleSheet("font: bold; font-size: 20px; width : auto; text-align: left")
        self.relTop = QLabel('Related Topics')
        self.relTop.setStyleSheet("font: bold; font-size: 20px; width: auto; text-align: left")
        self.relTop.setMaximumSize(400,400)
        self.relQuerry.setMaximumSize(400,400)

        self.tabTrendingScoreForm.addRow(self.canvas)

        self.tabTrendingScoreForm.addRow(self.tabTrendingScoreFormsub)
        self.tabTrendingScore.setLayout(self.tabTrendingScoreForm)
        self.recommendationText.setStyleSheet("font-size: 25px; font-style: bold; text-align: center;")
        self.tabComparisionFormSub.addWidget(self.recommendationText)
        self.tabComparisionFormSub.setAlignment(Qt.AlignCenter)

        self.tabComparisionForm.addRow(self.canvasComp)
        self.tabComparisionForm.addRow(self.tabComparisionFormSub)
        self.tabComparision.setLayout(self.tabComparisionForm)
        self.relQuerry.setAlignment(Qt.AlignCenter)
        self.tabRelatedForm.addRow(self.relQuerry)
        self.tabRelatedForm.addRow(self.widgetRelatedQuery)
        self.tabRelatedForm.addRow(self.relTop)
        self.tabRelatedForm.addRow(self.widgetRelatedTopics)
        self.tabRelated.setLayout(self.tabRelatedForm)

        #Provide labels and data as lists and the number of subplot to draw the bar chart
    def barPainting(self,labels,data,n_subplot):
        width = 0.5
        self.axes = self.figureComp.add_subplot(n_subplot)
        self.axes.clear()
        self.axes.barh(labels,data,width,align="center")

        self.axes.set_yticklabels(labels, rotation=40)
        self.axes.tick_params(axis='y', labelsize=5)
        self.canvasComp.draw()



    # Create the data table in tab 4, parameter is the table you want to set(widgetRelatedTopics and widgetRelatedQuery)
    def createTable(self,tableWidget):
        # Create table
        # find the table length
        self.lsTest = self.gs
        rows = len(self.lsTest)
        columns = 1
        # set the rows and columns of the table
        tableWidget.setRowCount(rows)
        tableWidget.setColumnCount(columns)
        i = 0
        for value in self.lsTest:
            if i < int(rows):
                tableWidget.setItem(i, 0, QTableWidgetItem(value))
                i = i + 1

    # Function while the button is clicked.
    def on_click(self):
        self.productName=self.productTextBox.text()
        self.countryName = self.countryTextBox.text()
        # Draw the comparison bar chart
        ls, rel_quer, rel_top = Server.forCountry(self.countryName,self.productName)
        digital, analog = Server.forCountryMarketing(self.countryName)
        labeld = ['Email Marketing','Radio Advertising','Mobile Marketing','Television Advertising','Facebook Advertisement']
        labela = ['Newspaper Marketing','Billboards','Bus Shelter Ads','Print Ads','Fliers']
        E = digital['Email marketing'].mean()  # Print average popularity for marketing on this country
        R = digital['Radio Advertising'].mean()
        M = digital['Mobile Marketing'].mean()
        T = digital['Television Advertising'].mean()
        S = digital['Facebook Advertisement'].mean()
        datad = [E, R, M, T, S]
        N = analog['Newspaper Marketing'].mean() # Print average popularity for marketing on this country
        B = analog['Billboards'].mean()
        BUS = analog['Bus Shelter Ads'].mean()
        ADS = analog['Print Ads'].mean()
        Fil = analog['Fliers'].mean()
        dataa = [N, B, BUS, ADS, Fil]

        ReccomendedString = Server.RecommendationText(self.countryName,dataa,datad)
        self.recommendationText.setText(ReccomendedString)

        self.barPainting(labela,dataa,121)
        self.barPainting(labeld,datad,122)
        # Generate the related top and querry in the tab 4
        self.gs = rel_quer
        self.createTable(self.widgetRelatedTopics)
        self.gs = rel_top
        self.createTable(self.widgetRelatedQuery)
        # Paint the line chart
        self.plot(ls)

    # CLear the productTextBox and the country text box
    def clear_on_click(self):
        self.productTextBox.clear()
        self.countryTextBox.clear()
        print('all clear')

    # function to draw the line chart
    def plot(self,data):

        # hit only if we have values on all the four components
        #if (self.productTextBox.text()):

            # create an axis
            ax = self.figure.add_subplot(111)

            # discards the old graph
            ax.clear()

            # plot data

            for tick in ax.get_xticklabels():
                tick.set_rotation(20)
            ax.plot(data, '*-')

            # refresh canvas
            self.canvas.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

