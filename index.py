import pafy
import humanize

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.uic import loadUiType
import urllib.request

import os
from os import path


# import for ui file
# why we use (,_)?
ui,_ = loadUiType('ui1.ui')

# intiate ui file or loading it
class MainApp(QMainWindow , ui):
    def __init__(self , parent=None):
        super(MainApp , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttons()


    def Handel_UI(self):
        self.setWindowTitle('PyDownloader')
        self.setFixedSize(690,480)

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)
        self.pushButton_3.clicked.connect(self.Download_YouTube_Video)
        self.pushButton_7.clicked.connect(self.get_YouTube_Video)
        self.pushButton_4.clicked.connect(self.save_browse)


    def Handel_Browse(self):
        # . = the main partition | with any file type
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        text = str(save_location)
        name = (text[2:].split(',')[0].replace("'" , ''))
        self.lineEdit_2.setText(name)

        # print(save_location)
        '''
        
        - make it string
        x = "('F:/مشاريع/مشاريع بايثون/pyqt5/downloader pj/ui/kk.txt', 'All Files(*.*)')"
        
        - let's split it 
        s = x.split('.')
        s = s[0]  ==>x.split('.')[0]
        
        s = (x[2:].split('.'))[0].replace("'" , ''))
        '''

    '''
    file size -> 100 MB
    
    1  2  3  4  ...
    10 10 10 10 10 10 10 10 10 10 = 100 mb
    '''
    def Handel_Progress(self , blocknum , blocksize , totalsize):
        read = blocknum * blocksize

        if totalsize > 0:
            percent = read * 100/totalsize
            self.progressBar.setValue(percent)
            #threading is better than this
            QApplication.processEvents() #solve not responding

    def Download(self):
        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        try:
            urllib.request.urlretrieve(url, save_location, self.Handel_Progress)
        except Exception:
            QMessageBox.warning(self , "Download Error" , "the Download Faild")
            return

        QMessageBox.information(self , "Download Completed" , "the Download Finished")
        self.progressBar.setValue(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')


    def save_browse(self):
        save = QFileDialog.getExistingDirectory(self , "select downloade directory")
        self.lineEdit_4.setText(save)

    def get_YouTube_Video(self):
        video_url = self.lineEdit_3.text()
        video = pafy.new(video_url)
        # print(video.title)
        # print(video.duration)
        # print(video.author)
        # print(video.length)
        # print(video.viewcount)
        # print(video.likes)
        # print(video.dislikes)
        st = video.videostreams
        # print(st)

        for stream in st:
            print(stream.get_filesize())
            size = humanize.naturalsize(stream.get_filesize())
            data = "{} {} {} {}".format(stream.mediatype, stream.extension, stream.quality, size)
            self.comboBox_2.addItem(data)


    def Download_YouTube_Video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()
        video = pafy.new(video_url)
        st = video.videostreams
        quality = self.comboBox_2.currentIndex()
        # print(quality)

        down = st[quality].download(filepath = save_location)
        QMessageBox.information(self , "Download Completed" , "the Download Finished")




def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinte loop to make the app alwase on display

# make me run the code from any where i want
if __name__ == '__main__':
    main()
