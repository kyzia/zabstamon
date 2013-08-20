#!/usr/bin/python
# -*- coding: utf-8 -*-

############################ Powered by Oleg G. Kuznetsov ############################
############################   smalloleg@gmail.com        ############################
######################################################################################

import sys
#import PyQt4
from PyQt4 import QtGui, QtCore
import time
import random
import copy

from zabbix_api.zabbix_api import ZabbixAPI, ZabbixAPIException

############## Passsword and url ####################
username = 'username'
password = 'password'
server = 'http://zabbix.domain/zabbix'



############## Platform identification ##############

#if sys.platform == 'win32':
#  import win32_sysinfo as sysinfo
#elif sys.platform == 'darwin':
#  import mac_sysinfo as sysinfo
#elif 'linux' in sys.platform:
#  import linux_sysinfo as sysinfo


############## Active triggerlist load from zabbix ####################

class Triggerlist():
        def __init__(self):
                self.info_trg_function1=self.trigger_list(server, username, password, listtype="1")
                self.info_trg_function2=self.trigger_list(server, username, password, listtype="2")

        def result1( self ) :
                return self.info_trg_function1
        def result2( self ) :
                return self.info_trg_function2

        def trigger_list(self, server, username, password, listtype):
                zapi = ZabbixAPI(server=server, path="", log_level=0)
                zapi.login(username, password)
                triggerlist = zapi.trigger.get(
                        {'active' : True,
                        'monitored': True,
                        'sortfield': 'priority',
                        'sortorder' : 'DESC',
                        #'sortfield': 'lastchange',
                        'filter': {'value': 1},
                        'expandData': '1', 
                        #'expandDescription': '1',
                        'output': 'extend',
                        'skipDependent': False})
                resulttext = u''
                if listtype == '1' :
                    nm = 0
                    for x in triggerlist :
##################### Full  data example
#                            print x
                            if x['priority'] == '0' :
                                    message = u'NOT CLASSIFIED'
                                    nm = nm + 1
                            elif x['priority'] == '1' :
                                    message = u'INFORMATIONAL'
                                    nm = nm + 1
                            elif x['priority'] == '2' :
                                    message = u'WARNING'
                                    nm = nm + 1
                            elif x['priority'] == '3' :
                                    message = u'AVERAGE'
                                    nm = nm + 1
                            elif x['priority'] == '4' :
                                    message = u'HIGH'
                                    nm = nm + 1
                            elif x['priority'] == '5' :
                                    message = u'DISASTER'
                                    nm = nm + 1
################ Internal information
################ priority 0 - not classified, 1 -informational, 2 - warning, 3 - Average, 4 - High, 5 - Disaster

                            resulttext = resulttext + u'\n' + message + u'::::' + x['hostname'] + u'::::' + x['description']

################ Code for Debug
#                    print u'Resulttext1' + resulttext
#                    print nm
#                    print "__________________________________________________"
#                    print len(hashmassive)
#                    print hashmassive[2]
#                    print "__________________________________________________"
#                    return str(nm)
                    return resulttext
                elif listtype == '2' :
                    hashmassive = []
                    nc = 0
                    inf = 0
                    warn = 0
                    avg = 0
                    high = 0
                    dis = 0
                    for x in triggerlist :
                            hashmassive.append(x['triggerid'])
                            if x['priority'] == '0' :
                                    message = u'NOT CLASSIFIED'
                                    nc = nc + 1
                            elif x['priority'] == '1' :
                                    message = u'INFORMATIONAL'
                                    inf = inf + 1
                            elif x['priority'] == '2' :
                                    message = u'WARNING'
                                    warn = warn + 1
                            elif x['priority'] == '3' :
                                    message = u'AVERAGE'
                                    avg = avg + 1
                            elif x['priority'] == '4' :
                                    message = u'HIGH'
                                    high = high + 1
                            elif x['priority'] == '5' :
                                    message = u'DISASTER'
                                    dis = dis + 1
#priority 0 - not classified, 1 -informational, 2 - warning, 3 - Average, 4 - High, 5 - Disaster
                    resulttext = u''
                    if nc > 0 : 
                        resulttext = str(resulttext) + u'NOT CLASSIFIED:' + str(nc) + u' '
                    else :
                        print u'NOT CLASSIFIED:' + str(nc)
                    if inf > 0 : 
                        resulttext = str(resulttext) + u'INFORMATIONAL:' + str(inf) + u' '
                    else :
                        print u'INFORMATIONAL:' + str(inf)
                    if warn > 0 : 
                        resulttext = str(resulttext) + u'WARNING:' + str(warn) + u' '
                    else :
                        print u'WARNING:' + str(warn)
                    if avg > 0 : 
                        resulttext = str(resulttext) + u'AVERAGE:' + str(avg) + u' '
                    else :
                        print u'AVERAGE:' + str(avg)
                    if high > 0 : 
                        resulttext = str(resulttext) + u'HIGH:' + str(high) + u' '
                        pass
                    else :
                        print u'HIGH:' + str(high)
                    if dis > 0 : 
                        resulttext = str(resulttext) + u'DISASTER:' + str(dis)
                    else :
                        print u'DISASTER:' + str(dis)
###### Old code
#                    resulttext = u'NOT CLASSIFIED:' + str(nc) + u' ' + u'INFORMATIONAL:' + str(inf) + u' ' + u'WARNING:' + str(warn) + u' ' + u'AVERAGE:' + str(avg) + u' ' + u'HIGH:' + str(high) + u' ' + u'DISASTER:' + str(dis)
#                    errcount = nc + inf + warn + avg + high + dis
#                    return (resulttext, errcount)

                    return (resulttext, hashmassive)

############## Thread - check by while(true) cycle triggers and send list with triggers id to main window ####################
class MyThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str, str, list)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)

    def set_status (self):
        self.status_value = 0

    def setup(self, thread_no):
        self.thread_no = thread_no


    def run(self):
###### Test code
#        time.sleep(random.random()*5)  # random sleep to imitate working
        status_tmp = 0
        self.status_value = 0
        while(True):
            print "Loop"
            time.sleep(2)
            Trg=Triggerlist()
            triggers = Trg.result1()
            triggers2, hashmassive = Trg.result2()
###### Debug code
#            print len(hashmassive)
#            print hashmassive
#            a = 0
###### Hashmassive list count elements - by triggers number
#            for x in hashmassive:
#                a = a + int (x) 
#                print a

            self.trigger.emit(triggers, triggers2, hashmassive)

############## Popup window ####################
class Popup(QtGui.QWidget):
        def __init__(self, xx, yy, info):
            QtGui.QWidget.__init__(self)
#            self.resize(800, 300)
            self.setGeometry(100, 100, 800, 300)
##### Window position
            self.move(xx, yy + 75)
            self.setWindowFlags(QtCore.Qt.Tool)
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool )
            self.setStyleSheet( 'background-color: white;' )
            self.label1 = QtGui.QLabel(info, self)
            l=QtGui.QVBoxLayout(self)
            l.setContentsMargins(0,0,0,0)
            l.setSpacing(0)
            s=QtGui.QScrollArea()
            l.addWidget(s)
            w=QtGui.QWidget(self)        
            vbox=QtGui.QVBoxLayout(w)
            _l=QtGui.QHBoxLayout()
            _l.addWidget(self.label1)
            _l.addStretch(1)
            vbox.addLayout(_l)
     
            s.setWidget(w)
     
        def leaveEvent(self,event):
                self.close()
###                print("Leave")

############## Main window ####################
class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            QtGui.QMainWindow.__init__( self, None)
            self.setFocusPolicy( QtCore.Qt.StrongFocus )
            self.setAttribute( QtCore.Qt.WA_QuitOnClose, True )
            self.resize(200, 40)
            self.move(10, 10)
###### Test code
#            self.setStyleSheet( 'background-color: red;color: white;' )
            self.setStyleSheet( 'font-size:12px; background-color: #ffffff; color: #000000; border-style: outset; border-width: 2px; border-color: beige;' )
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool )
            self.name = "name"
            self.status = 0
            self.hashtable_main = []
            self.label2 = QtGui.QLabel("No data. Connecting to server.", self)
            central_widget = QtGui.QWidget()
            central_layout = QtGui.QHBoxLayout()
            central_layout.addWidget(self.label2)
            central_widget.setLayout(central_layout)
            self.setCentralWidget(central_widget)
###### Create timer for check status and blinking
            self.i = 0
            self.start_thread()
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.doBlinkMethod)
            self.timer.start(1000)

###### Blink function
        def doBlinkMethod(self):
            if self.status == 0:
                self.setStyleSheet( 'font-size:12px; background-color: #ffffff; color: #000000; border-style: outset; border-width: 2px; border-color: beige;' )
            if self.status > 0 and self.i == 0:
                self.setStyleSheet( 'font-size:12px; background-color: #b50404; color: #ffffff; border-style: outset; border-width: 2px; border-color: beige;' )
                self.repaint()
                self.i = 1
            elif self.status > 0 and self.i == 1 :
                self.setStyleSheet( 'font-size:12px; background-color: #ffffff; color: #000000; border-style: outset; border-width: 2px; border-color: beige;' )
                self.repaint()
                self.i = 0
###### Test code
##                print "blah"

        def alarm(self) :
            while self.status <=1:
                self.setStyleSheet( 'background-color: #b50404;' )
                time.sleep(1)
                print u'work'
                self.setStyleSheet( 'background-color: #ffffff;' )

        def mousePressEvent(self, event):
            self.w2.close()
            self.offset = event.pos()

        def mouseMoveEvent(self, event):
            x=event.globalX()
            y=event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.xx=x-x_w
            self.yy=y-y_w
            self.move(self.xx, self.yy)

        def contextMenuEvent(self, event):
            menu = QtGui.QMenu(self)

            Action = menu.addAction("Exit")
            Action.triggered.connect(self.closeEvent)

            menu.exec_(event.globalPos())

        def closeEvent( self, event ):
            QtGui.QApplication.exit()

        def physheight( self ):
            screen_count = QtGui.QDesktopWidget().screenCount()
            if screen_count == 1 :
                screen_number = QtGui.QDesktopWidget().screenNumber(self)
                geom = QtGui.QDesktopWidget().screenGeometry(screen_number);
                x = geom
            else :
                screen_number = QtGui.QDesktopWidget().screenNumber(self)
                geom = QtGui.QDesktopWidget().screenGeometry(screen_number);
                x = geom
            return x.height()

###### Starting trhread
        def start_thread(self):
            self.param=u'No Data'
            self.threads = []              # this will keep a reference to threads
#            for i in range(10):
            thread = MyThread(self)    # create a thread
            thread.trigger.connect(self.update_text)  # connect to it's signal
            thread.setup(2)            # just setting up a parameter
            thread.start()             # start the thread
            self.threads.append(thread) # keep a reference

        def check_hashlists(self, hashtable):
            n = 0
            if self.hashtable_main :
                for x in hashtable :
                    if not x in self.hashtable_main :
                        print "Gotcha!"
                        self.status = 1
###### Debug code
#                for y in hashtable_main :
#                    if y = x :
#                        n = n +1
#            
#                print x
            self.hashtable_main = copy.deepcopy(hashtable)


        def update_text(self, triggers, triggers2, hashmassive):
###### Debug code
#            print hashmassive
            self.param = str(triggers.toUtf8()).decode('utf-8')
###### Debug code
#            print len(hashmassive)
            self.check_hashlists(hashmassive)
###### Old check by error count

##            self.status = status
##            self.errcount = status_errcount
###            print "Self Errcount:"
###            print self.errcount
            
###            print "Errcount from thread:"
###            print status_errcount
            
###            if self.status == 1:
###                pass
###            else :
###                if status_errcount == self.errcount :
###                    print "status_errcount = self.errcount"
###                    self.status = 0
###                if self.errcount == 0 :
###                    print "first iteration"
###                    self.errcount = status_errcount
###                if status_errcount > self.errcount :
###                    self.status = 1
###                    self.errcount = status_errcount
###                if status_errcount < self.errcount :
#                    self.status = 1
###                    self.errcount = status_errcount

            self.label2.setText(str(triggers2.toUtf8()).decode('utf-8'))
        def info( self ):
            return self.param

        def enterEvent(self,event):
            test = self.physheight()
            print "__geometry__here_"
            print test
            self.status = 0
            coord = self.pos()
###### Debug code
            #print coord.x()
##            print coord.y()
#            resolution = QtGui.QDesktopWidget().availableGeometry()
###### Debug code
##            print self.physheight()
            if coord.y() > self.physheight() - ( self.physheight() / 2 ) :
                print u'Yeah'
                self.w2 = Popup(xx=coord.x(), yy=coord.y() - 400, info=self.param)
                self.w2.show()
            else :
                    self.w2 = Popup(xx=coord.x(), yy=coord.y(), info=self.param)
                    self.w2.show()

############## Function main - start Main Window ####################
def main():
        app = QtGui.QApplication(sys.argv)
        w = MainWindow()
        w.show()
        sys.exit( app.exec_() )

if __name__ == '__main__':
###### Debug code
#        Trg=Triggerlist()
#        abv=Trg.getresult()
#        print Trg.result()
        main()
