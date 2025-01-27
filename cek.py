from io import BytesIO
import PIL.Image as Image
from service.main.CheckEnviroment import check_environment
import os

# Cek dan siapkan lingkungan R
path = os.path.join(os.path.dirname(__file__), 'R', 'R-4.4.2')
original_path = os.path.dirname(__file__)
check_environment(path, original_path)

from service.main.LoadingR import loadR  # Load modul R setelah check_environment

import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QByteArray
pandas2ri.activate()

r = ro.r

r('''
    library(ggplot2)

    # Create a sample data frame
    data <- data.frame(
        x = rnorm(100),
        y = rnorm(100)
    )

    # Create a scatter plot
    p <- ggplot(data, aes(x = x, y = y)) +
        geom_point()
    p
''')
# Convert the R plot to a PNG image in memory
r('png(filename="Rplot.png")')
r('print(p)')
r('dev.off()')

# Read the PNG image from memory
with open("Rplot.png", "rb") as image_file:
    image_data = image_file.read()

# Create a PyQt6 application
app = QApplication([])

# Create a widget to display the image
widget = QWidget()
layout = QVBoxLayout()
label = QLabel()
layout.addWidget(label)
widget.setLayout(layout)

# Convert the image data to a QPixmap and set it on the label
pixmap = QPixmap()
pixmap.loadFromData(QByteArray(image_data))
label.setPixmap(pixmap)

# Show the widget
widget.show()

# Delete the image file after displaying it
os.remove("Rplot.png")

# Start the PyQt6 event loop
app.exec()