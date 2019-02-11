
import sys
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, \
    QVBoxLayout,QHBoxLayout, QDesktopWidget, QFormLayout, QLabel, QLineEdit
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from matplotlib.figure import Figure
from src.Back import ScorceCode


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Blue Ocean Whale Sharks'
        self.left = 200
        self.top = 200
        self.width = 700
        self.height = 100
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('six_sigma.ico'))

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



        # The dataframe
        self.df = pd.DataFrame()
        # The data for the data table
        self.gs = []
        # Initialize the labels for the first tab

        self.productLabel = QLabel("Product", self)
        self.countryLabel = QLabel("Country", self)

        # Initialise the textbox for all the labels along with the tooltips

        self.productTextBox = QLineEdit(self)

        self.productTextBox.setToolTip("Enter the product here")
        self.countryTextBox = QLineEdit(self)
        self.countryTextBox.setToolTip("Enter the country here")



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
        self.show()


        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.resize(self.clearAllButton.sizeHint())
        self.clearAllButton.setToolTip("To clear all the fields")
        self.clearAllButton.clicked.connect(self.clear_on_click)



        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(480, 320)

        # Add tabs
        self.tabs.addTab(self.tab1, "The Input Tab")
        self.tabs.addTab(self.tab4, "The Recommendation")

        self.tab1form = QFormLayout()

        self.tab1form.addRow(self.productLabel,self.productTextBox)
        self.tab1form.addRow(self.countryLabel,self.countryTextBox)
        self.tab1form.addRow(self.submitButton,self.clearAllButton)


        self.tab1.setLayout(self.tab1form)

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
        self.tab4Form = QFormLayout()
        self.tab4Formsub = QHBoxLayout()
        #self.tab4Formsub1 = QFormLayout()
        #self.tab4Formsub2 = QFormLayout()
        self.tablewidget = QTableWidget()
        self.tablewidget2 = QTableWidget()
        self.tablewidget.adjustSize()
        self.tablewidget.setMaximumSize(300,80)
        self.tablewidget2.setMaximumSize(300,80)
        self.tablewidget.horizontalHeader().setStretchLastSection(True)
        self.tablewidget2.horizontalHeader().setStretchLastSection(True)
        self.recommendationText = QLabel()
        self.recommendationText.setMinimumSize(400,100)
        self.recommendationText.setToolTip("This tab shows the recommendation ")
        self.relQuerry = QLabel('Related Querry')
        self.relTop = QLabel('Related Topics')
        self.linechartLabel = QLabel('The trends')
        self.barchartLabel = QLabel('The comparision')
        self.relTop.setMaximumSize(100,100)
        self.relQuerry.setMaximumSize(100,100)
        self.test1 = QLabel('test')
        self.test2 = QLabel('test')
        self.test3 = QLabel('test')
        self.test4 = QLabel('test')
        self.tab4Formsub.addWidget(self.relQuerry)
        self.tab4Formsub.addWidget(self.tablewidget)
        self.tab4Formsub.addWidget(self.relTop)
        self.tab4Formsub.addWidget(self.tablewidget2)
        self.tab4Formsub.addWidget(self.recommendationText)
        self.tab4Form.addRow(self.linechartLabel,self.canvas)
        self.tab4Form.addRow(self.barchartLabel,self.canvasComp)

        self.tab4Form.addRow(self.tab4Formsub)
        #self.tab4Form.addRow(self.relQuerry,self.tablewidget)
        #self.tab4Form.addRow(self.relTop,self.tablewidget2)
        self.tab4.setLayout(self.tab4Form)
        #self.tab4Form.addRow(self.recommendationText)


        #Provide labels and data as lists and the number of subplot to draw the bar chart
    def barPainting(self,labels,data,n_subplot):
        width = 0.5
        self.axes = self.figureComp.add_subplot(n_subplot)
        self.axes.clear()
        self.axes.barh(labels,data,width,align="center")
        #self.axes.set_xticks([0,1,2,3])
        self.axes.set_yticklabels(labels, rotation=40)
        self.axes.tick_params(axis='y', labelsize=5)
        self.canvasComp.draw()



    # Create the data table in tab 4, parameter is the table you want to set(tablewidget and tablewidget2)
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
        print("\n")
        print(self.productTextBox.text())
        self.productName=self.productTextBox.text()
        self.countryName = self.countryTextBox.text()
        # Draw the comparison bar chart
        ls, rel_quer, rel_top = ScorceCode.forCountry(self.countryName,self.productName)
        digital, analog = ScorceCode.forCountryMarketing(self.countryName)
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

        ReccomendedString = ScorceCode.RecommendationText(dataa,datad)
        self.recommendationText.setText(ReccomendedString)

        self.barPainting(labela,dataa,121)
        self.barPainting(labeld,datad,122)
        # Generate the related top and querry in the tab 4
        self.gs = rel_quer
        self.createTable(self.tablewidget)
        self.gs = rel_top
        self.createTable(self.tablewidget2)
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

            print("Inside the plot method")
            # Call the api #TODO
            print('plotBreak')
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

