
import numpy as np
import seaborn as sns
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys


#GLOBALS
fc = 0.0
vc = 0.0
p = 0.0
q = 0.0

class Ui(QtWidgets.QMainWindow):
	def __init__(self):
		super(Ui, self).__init__() 
		uic.loadUi('gui.ui', self) 

		self.show() 
		self.calculate_but.clicked.connect(self.change)

	def error(self,e):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle("Error")
		msg.setText(e)
		msg.exec_()

	def change(self):
		global fc,vc,p,q
		try:
			fc = float(self.fc_line.text())
			vc = float(self.vc_line.text())
			p = float(self.p_line.text())
		except:
			self.error("Invalid Inputs!")
			return
		try:
			q = float(self.q_line.text())
		except:
			q = False

		self.result = Final()
		self.result.show()


class Final(QtWidgets.QMainWindow):
	def __init__(self):
		super(Final,self).__init__()
		uic.loadUi('result.ui', self) 

		self.set_val()
		self.pl()

	def set_val(self):
		global fc,vc,p,q
		if p-vc == 0:
			beq = 0	
		else:
			beq = fc / (p-vc)
		if q == False:
			self.beq_reach_val.setText("Quantity Not Specified")
			self.q_required_val.setText("Quantity Not Specified")
			self.net_profit_val.setText("Quantity Not Specified")
			self.r_val.setText("Quantity Not Specified")
			self.q_val.setText("Quantity Not Specified")
		else:
			self.beq_reach_val.setText(str(q >= beq))
			if q >= beq:
				self.q_required_val.setText("Already Reached")
			else:
				self.q_required_val.setText(str(beq - q))
			self.net_profit_val.setText(str(q*(p-vc) - fc))
			self.r_val.setText(str(p*q))
			self.q_val.setText(str(q))
		self.beq_val.setText(str(round(beq,2)))
		self.p_val.setText(str(p))
		self.fc_val.setText(str(fc))
		self.vc_val.setText(str(vc))




	def pl(self):
		global fc,vc,p,q
		if p-vc == 0:
			beq = 0	
		else:
			beq = fc / (p-vc)

		x = np.arange(beq * 3)
		
		self.widget.canvas.ax.axhline(fc,linestyle = "--",label = "Fixed Costs")
		self.widget.canvas.ax.plot(x, vc*x, label = "Variable Costs")
		self.widget.canvas.ax.plot(x, p*x, label = "Total Revenue" )
		self.widget.canvas.ax.plot(x, vc*x + fc, label = "Total Costs" )

	
		self.widget.canvas.ax.axhline(0, color = "black")
		self.widget.canvas.ax.axvline(0, color = "black", label = "Axis")
		#self.widget.canvas.ax.set_xlim([beq - beq/2, beq + beq/2])
		self.widget.canvas.ax.set_xlim([0, beq + beq/2])

		self.widget.canvas.ax.vlines(x = beq, ymin = 0, ymax = beq*p,linestyle = "--")
		self.widget.canvas.ax.hlines(y = beq*p,xmin = 0, xmax = beq,linestyle = "--")

		#Annotation on the graph
		#self.widget.canvas.ax.annotate(f"BEQ: {round(beq,2)} Units \nRevenue: {beq*p}",xy = (beq - beq*0.2,beq*p + beq*p*0.2))

		self.widget.canvas.ax.legend()
		self.widget.canvas.ax.set_xlabel("Quantity")
		self.widget.canvas.ax.set_ylabel("Revenue")
		self.widget.canvas.draw()


		


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv) 
	window = Ui()
	app.exec_() 

