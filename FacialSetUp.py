# -*- coding: utf-8 -*-

from maya import cmds
from maya import mel
from maya import OpenMayaUI as OMUI

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import *
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtUiTools import *
    from shiboken import wrapInstance

mayaMainWindowPtr = OMUI.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)


class AIFAE_FacialSetup(QWidget):
    def __init__(self, *args, **kwargs):
        super(AIFAE_FacialSetup, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("AIFAE Facial Setup Window")
        self.initUI()

    def initUI(self):
        loader = QUiLoader()
        currentDir = 'F:/QtProject'
        file = QFile( currentDir+"/createNode.ui")
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=self)

        self.ui.parentConstraintBtn.clicked.connect(self.doParentConstraint)
        self.ui.pointConstraintBtn.clicked.connect(self.doPointConstraint)
        self.ui.setDrivenKeyBtn.clicked.connect(self.doSetDrivenKey)
        self.ui.deleteConstraintBtn.clicked.connect(self.doDeleteConstraint)

    def doParentConstraint(self):  #遍历场景根据名称进行约束
        driverName = self.ui.driverNameLine.text()
        drivenName = self.ui.drivenNameLine.text()
        print  (driverName, drivenName)
        transformsObjects = cmds.ls(tr = True)
        for driverObj in transformsObjects:                                 #遍历场景中的物体
            if driverName in driverObj:                                     #查找驱动物体
                drivenObj =  driverObj.replace(driverName,drivenName)       #设置驱动物体名称
                if cmds.objExists(drivenObj):                               #确认被驱动物体是否存在
                    cmds.parentConstraint(driverObj, drivenObj , mo = True) #约束物体

    def doPointConstraint(self): #遍历场景根据名称进行约束
        driverName = self.ui.driverNameLine.text()
        drivenName = self.ui.drivenNameLine.text()
        print  driverName,drivenName
        transformsObjects = cmds.ls(tr = True)
        for driverObj in transformsObjects:                                 #遍历场景中的物体
            if driverName in driverObj:                                     #查找驱动物体
                drivenObj =  driverObj.replace(driverName,drivenName)       #设置驱动物体名称
                if cmds.objExists(drivenObj):                               #确认被驱动物体是否存在
                    #print driverObj,drivenObj
                    cmds.pointConstraint(driverObj,drivenObj , mo = True)   #约束物体

    def doDeleteConstraint(self):#遍历场景根据名称进行删除
        #driverName = self.ui.driverNameLine.text()
        drivenName = self.ui.drivenNameLine.text()
        #print  driverName
        transformsObjects = cmds.ls(tr=True)
        for obj in transformsObjects:
            if "Constraint" in obj and  drivenName in obj:  #确认被约束物体
                cmds.delete(obj)                            #删除约束

    def doSetDrivenKey(self):#遍历场景根据名称进行驱动
        driverName = self.ui.driverNameLine_2.text()
        drivenName = self.ui.drivenNameLine_2.text()
        driverAttrA = self.ui.driverAttrA.text()
        driverAttrB = self.ui.driverAttrB.text()
        drivenAttrA = self.ui.drivenAttrA.text()
        drivenAttrB = self.ui.drivenAttrB.text()
        minRotateX = self.ui.minSpinBoxX.value()
        midRotateX = self.ui.midSpinBoxX.value()
        maxRotateX = self.ui.maxSpinBoxX.value()
        minRotateY = self.ui.minSpinBoxY.value()
        midRotateY = self.ui.midSpinBoxY.value()
        maxRotateY = self.ui.maxSpinBoxY.value()
        #print (minRotateX, midRotateX, maxRotateX, minRotateY, midRotateY, maxRotateY)
        drivers = cmds.ls(sl=True)                                      #选择驱动关键帧的控制器
        if len(drivers)!=0:
            for driver in drivers:
                drivenObj = driver.replace(driverName, drivenName)      #查找被驱动物体名称
                if cmds.objExists(drivenObj):                           #如果被驱动物体存在，设置驱动关键帧
                    cmds.setDrivenKeyframe(drivenObj + ".%s"%drivenAttrA, currentDriver=driver+driverAttrA,
                                           driverValue=-1, value=minRotateX)
                    cmds.setDrivenKeyframe(drivenObj + ".%s" % drivenAttrA, currentDriver=driver + driverAttrA,
                                           driverValue=0, value=midRotateX)
                    cmds.setDrivenKeyframe(drivenObj + ".%s"%drivenAttrA, currentDriver=driver+driverAttrA,
                                           driverValue=1, value=maxRotateX)
                    cmds.setDrivenKeyframe(drivenObj + ".%s"%drivenAttrB, currentDriver=driver+driverAttrB,
                                           driverValue=-1, value=minRotateY)
                    cmds.setDrivenKeyframe(drivenObj + ".%s" % drivenAttrB, currentDriver=driver + driverAttrA,
                                           driverValue=0, value=midRotateY)
                    cmds.setDrivenKeyframe(drivenObj + ".%s"%drivenAttrB, currentDriver=driver+driverAttrB,
                                           driverValue=1, value=maxRotateY)
                else:
                    print ("Your select %s is not exists!"%drivenObj)
        else:
            print ("No object is selected!")

def main():
    ui = AIFAE_FacialSetup()
    ui.show()
    return ui


if __name__ == '__main__':
    main()
