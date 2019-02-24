'''http://mrleeh.square7.ch/?p=1349'''

import sys

import pylab
from PyQt4.QtGui import QWidget, QVBoxLayout, QApplication
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg


class MyForm (QWidget):
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)

        #plotting area
        self.x_axis = []
        self.y_axis = []
        self.fig = pylab.figure(1)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis([0, 100, -1.5, 1.5])
        self.line1 = self.ax.plot(self.x_axis, self.y_axis, "-")

        #widget layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        #Timer object for periodical drawing
        self.generator = SinwaveGenerator()
        self.timer = self.fig.canvas.new_timer(interval=100)
        self.timer.add_callback(self.realtime_plotter)
        self.timer.start()

    def realtime_plotter(self):
        #get new value
        self.generator.next()
        #set x axis to show the last 100 values
        current_xaxis = pylab.arange(len(self.generator.values) - 100, len(self.generator.values), 1)
        #adjust visible axis
        self.ax.axis([current_xaxis.min(), current_xaxis.max(), -1.5, 1.5])
        #pass last 100 values to line object
        self.line1[0].set_data(current_xaxis, pylab.array(self.generator.values[-100:]))
        #refresh canvas
        self.canvas.draw()

class SinwaveGenerator():
    def __init__(self):
        self.Ta = 0.01
        self.fa = 1.0 / self.Ta
        self.fcos = 3.5

        self.Konstant = pylab.cos(2 * pylab.pi * self.fcos * self.Ta)
        self.t0 = 1.0
        self.t1 = self.Konstant

        self.values = [0 for x in range(100)]

    def next(self):
        Tnext = ((self.Konstant * self.t1) * 2) - self.t0
        if len(self.values) % 100 > 70:
            self.values.append(pylab.random() * 2 - 1)
        else:
            self.values.append(Tnext)
        self.t0 = self.t1
        self.t1 = Tnext


app = QApplication(sys.argv)
frm = MyForm()
frm.show()
app.exec_()
