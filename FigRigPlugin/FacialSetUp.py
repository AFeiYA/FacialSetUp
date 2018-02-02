# -*- coding: utf-8 -*-
#import fit_position

from maya import cmds
from maya import mel
from maya import OpenMayaUI as OMUI
import os
from  inspect import getsourcefile


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
    '''不能有重名的字符串'''
    face_rig_dict = {
        "face_rig": [
            {"face_constraint": "face_constraint1"},
            {
                "face_ctrl": [
                    {"uppEyelid_left_conner": ["lowerEyelid_left_1_bn_ctrl", "lowerEyelid_left_3_bn_ctrl", "upperEyelid_left_1_bn_ctrl", "upperEyelid_left_3_bn_ctrl"]},
                    {"uppEyelid_right_conner": ["lowerEyelid_right_1_bn_ctrl", "lowerEyelid_right_3_bn_ctrl", "upperEyelid_right_1_bn_ctrl", "upperEyelid_right_3_bn_ctrl"]},
                    {
                        "ctrl_grp": [
                            {
                                "jaw_ctrl_locator": [
                                    {
                                        "lowerlip": [
                                            {
                                                "lowerlip2": "lowerlip_2_sufaceJoint"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "lowerEyelid_left_ctrl_locator": [
                                    {
                                        "lowerEyelid_left": [
                                            "lowerEyelid_left_1_bn_ctrl",
                                            "lowerEyelid_left_2_bn_ctrl",
                                            "lowerEyelid_left_3_bn_ctrl",
                                            "lowerEyelid_left_4_bn_ctrl",
                                            "lowerEyelid_left_5_bn_ctrl"
                                        ]
                                    }
                                ]
                            },
                            {
                                "lowerEyelid_right_ctrl_locator": [
                                    {
                                        "lowerEyelid_right": [
                                            "lowerEyelid_right_1_bn_ctrl",
                                            "lowerEyelid_right_2_bn_ctrl",
                                            "lowerEyelid_right_3_bn_ctrl",
                                            "lowerEyelid_right_4_bn_ctrl",
                                            "lowerEyelid_right_5_bn_ctrl"
                                        ]
                                    }
                                ]
                            },
                            {
                                "upperEyelid_left_ctrl_locator": [
                                    {
                                        "upperEyelid_left": [
                                            "upperEyelid_left_1_bn_ctrl",
                                            "upperEyelid_left_2_bn_ctrl",
                                            "upperEyelid_left_3_bn_ctrl",
                                            "upperEyelid_left_4_bn_ctrl",
                                            "upperEyelid_left_5_bn_ctrl",
                                        ]
                                    }
                                ]
                            },
                            {
                                "upperEyelid_right_ctrl_locator": [
                                    {
                                        "upperEyelid_right": [
                                            "upperEyelid_right_1_bn_ctrl",
                                            "upperEyelid_right_2_bn_ctrl",
                                            "upperEyelid_right_3_bn_ctrl",
                                            "upperEyelid_right_4_bn_ctrl",
                                            "upperEyelid_right_5_bn_ctrl",
                                        ]
                                    }
                                ]
                            }

                        ]
                    },
                    {
                        "brows_left": [
                            "brows_left_1_locator",
                            "brows_left_2_locator",
                            "brows_left_3_locator"
                        ]
                    },
                    {
                        "brows_right": [
                            "brows_right_1_locator",
                            "brows_right_2_locator",
                            "brows_right_3_locator"
                        ]
                    },
                    {
                        "mouth_conner": [
                            {
                                "upperlip": "upperlip_2_surfaceJoint"
                            },
                            {
                                "mouthCorner_left": [
                                    {
                                        "mouthCorner_left": [
                                            {
                                                "mouthCorner_left_jaw": [
                                                    {
                                                        "mouthCorner_left_ctrl": [
                                                            {
                                                                "mouthCorner_left_locator_grp": "mouthCorner_left_locator"},
                                                            "upperlip_1_sufaceJoint",
                                                            "lowerlip_1_sufaceJoint"
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "mouthCorner_right": [
                                    {
                                        "mouthCorner_right": [
                                            {
                                                "mouthCorner_right_jaw": [
                                                    {
                                                        "mouthCorner_right_ctrl": [
                                                            {
                                                                "mouthCorner_right_locator_grp": "mouthCorner_right_locator"},
                                                            "upperlip_3_sufaceJoint",
                                                            "lowerlip_3_sufaceJoint"
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    final_list = []
    move_list = [{"face_rig": "Head"},
                 {"face_constraint": ""},
                 {"face_ctrl": ""},
                 {"uppEyelid_left_conner": ""},
                 {"uppEyelid_right_conner": ""},
                 {"brows_left": "eye_control"},
                 {"brows_left_1_locator": "brows_left_1_bn"},
                 {"brows_left_2_locator": "brows_left_2_bn"},
                 {"brows_left_3_locator": "brows_left_3_bn"},
                 {"brows_right": "eye_control"},
                 {"brows_right_1_locator": "brows_right_1_bn"},
                 {"brows_right_2_locator": "brows_right_2_bn"},
                 {"brows_right_3_locator": "brows_right_3_bn"},
                 {"ctrl_grp": "Head"},

                 {"lowerEyelid_left_ctrl_locator": "eyelid_left_bn"},
                 {"lowerEyelid_left": ""},
                 {"lowerEyelid_left_1_bn_ctrl": "lowerEyelid_left_1_bn"},
                 {"lowerEyelid_left_2_bn_ctrl": "lowerEyelid_left_2_bn"},
                 {"lowerEyelid_left_3_bn_ctrl": "lowerEyelid_left_3_bn"},
                 {"lowerEyelid_left_4_bn_ctrl": "lowerEyelid_left_4_bn"},
                 {"lowerEyelid_left_5_bn_ctrl": "lowerEyelid_left_5_bn"},

                 {"upperEyelid_left_ctrl_locator": "eyelid_left_bn"},
                 {"lowerEyelid_left": ""},
                 {"upperEyelid_left_1_bn_ctrl": "upperEyelid_left_1_bn"},
                 {"upperEyelid_left_2_bn_ctrl": "upperEyelid_left_2_bn"},
                 {"upperEyelid_left_3_bn_ctrl": "upperEyelid_left_3_bn"},
                 {"upperEyelid_left_4_bn_ctrl": "upperEyelid_left_4_bn"},
                 {"upperEyelid_left_5_bn_ctrl": "upperEyelid_left_5_bn"},

                 {"lowerEyelid_right_ctrl_locator": "eyelid_right_bn"},
                 {"lowerEyelid_right": ""},
                 {"lowerEyelid_right_1_bn_ctrl": "lowerEyelid_right_1_bn"},
                 {"lowerEyelid_right_2_bn_ctrl": "lowerEyelid_right_2_bn"},
                 {"lowerEyelid_right_3_bn_ctrl": "lowerEyelid_right_3_bn"},
                 {"lowerEyelid_right_4_bn_ctrl": "lowerEyelid_right_4_bn"},
                 {"lowerEyelid_right_5_bn_ctrl": "lowerEyelid_right_5_bn"},

                 {"upperEyelid_right_ctrl_locator": "eyelid_right_bn"},
                 {"lowerEyelid_right": ""},
                 {"upperEyelid_right_1_bn_ctrl": "upperEyelid_right_1_bn"},
                 {"upperEyelid_right_2_bn_ctrl": "upperEyelid_right_2_bn"},
                 {"upperEyelid_right_3_bn_ctrl": "upperEyelid_right_3_bn"},
                 {"upperEyelid_right_4_bn_ctrl": "upperEyelid_right_4_bn"},
                 {"upperEyelid_right_5_bn_ctrl": "upperEyelid_right_5_bn"},

                 {"jaw_ctrl_locator": "jaw_ctrl_bn"},
                 {"lowerlip": ""},
                 {"lowerlip_2": ""},
                 {"lowerlip_2_sufaceJoint": "jaw_1_bn"},
                 {"mouth_conner": "jaw_ctrl_bn"},
                 {"upperlip": ""},
                 {"upperlip_2_surfaceJoint": "jaw_1_bn"},
                 {"mouthCorner_right": "mouthCorner_right_bn"},
                 {"mouthCorner_right_jaw": "jaw_ctrl_bn"},
                 {"mouthCorner_right_ctrl": "mouthCorner_right_bn"},
                 {"lowerlip_3_sufaceJoint": ""},
                 {"upperlip_3_sufaceJoint": ""},
                 {"mouthCorner_right_locater_grp": ""},
                 {"mouthCorner_right_locater": ""},
                 {"mouthCorner_left": "mouthCorner_left_bn"},
                 {"mouthCorner_left_jaw": "jaw_ctrl_bn"},
                 {"mouthCorner_left_ctrl": "mouthCorner_left_bn"},
                 {"lowerlip_1_sufaceJoint": ""},
                 {"upperlip_1_sufaceJoint": ""},
                 {"mouthCorner_left_locater_grp": ""},
                 {"mouthCorner_right_locater": ""}, ]  # 位置信息对位字典
    depth = 1
    def __init__(self, *args, **kwargs):
        super(AIFAE_FacialSetup, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("AI FAE Facial Setup Window")
        self.initUI()

    def initUI(self):
        loader = QUiLoader()
        file_path =  os.path.abspath(getsourcefile(lambda : 0)) #获取脚本的绝对路径
        currentUI = file_path.replace(file_path.split('\\')[-1], "FacialSetUp.ui")
        #currentUI = file_path.replace(".py", ".ui")             #获取UI的的绝对路径
        print (file_path)
        file = QFile( currentUI)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=self)

        self.ui.createControllerBtn.clicked.connect(self.auto_create_controller)
        self.ui.fitPositionBtn.clicked.connect(self.fit_position)
        self.ui.parentConstraintBtn.clicked.connect(self.doParentConstraint)
        self.ui.pointConstraintBtn.clicked.connect(self.doPointConstraint)
        self.ui.setDrivenKeyBtn.clicked.connect(self.doSetDrivenKey)
        self.ui.deleteConstraintBtn.clicked.connect(self.doDeleteConstraint)
        self.ui.parentConstraintBtn_2.clicked.connect(self.doParentConstraint2)
        self.ui.pointConstraintBtn_2.clicked.connect(self.doPointConstraint2)

    def go_though_dict(self, json_data, path=""):
        #global depth
        if isinstance(json_data, dict):
            # depth += 1
            for key in json_data:
                path = path + key + "-->"
                self.go_though_dict(json_data[key], path)
        elif isinstance(json_data, list):
            # print len(json_data)
            for i in range(len(json_data)):
                # print json_data[i]
                if isinstance(json_data[i], dict):
                    for sub_key in json_data[i]:
                        self.depth += 1
                        self.go_though_dict(json_data[i], path)
                    self.depth -= 1
                else:
                    self.final_list.append((path + json_data[i], self.depth))
        else:
            self.final_list.append((path + json_data, self.depth))
        return self.final_list

    def create_tree(self, tree_leaf_edges):
        for element in  tree_leaf_edges:
            element_list = element[0].split("-->")
            for i in range(len(element_list)):
                if cmds.objExists(element_list[i]):
                    print (("{} has been created already!").format(element_list[i]))
                else:
                    if i != 0:
                        cmds.select(clear=True)
                        if "_loc" in element_list[i]:
                            cmds.spaceLocator(name=element_list[i])
                        elif "_bn_" in element_list[i] or "Joint" in element_list[i]:
                            cmds.joint(name=element_list[i])
                        else:
                            cmds.group(empty=True, name=element_list[i])
                        cmds.parent(element_list[i], element_list[i - 1])
                    else:
                        cmds.group(empty=True, name=element_list[i])
            print ("-------------------------------------------------------------------------")

    # 根据角色骨骼自动对位控制器位置。source_name为控制器名称， destination为移动目标。
    def move_to_position(self, source_name, destination_name):
        if cmds.objExists(source_name) and cmds.objExists(destination_name):
            destination_position = cmds.xform(destination_name, q=True, translation=True, worldSpace=True)
            cmds.move(destination_position[0], destination_position[1], destination_position[2], source_name)
        else:
            pass
            #print (source_name, destination_name)

    def set_position(self, obj_list):
        for element in obj_list:
            for key, value in element.items():
                self.move_to_position(key, value)

    def auto_create_controller(self):
        self.go_though_dict(json_data=self.face_rig_dict,path="")
        self.create_tree(tree_leaf_edges=sorted(self.final_list, key=lambda x: x[1]))

    def fit_position(self):
        if len(self.final_list)>0:
            self.set_position(self.move_list)
        else:
            cmds.error("Please create the controllers!")

    def doParentConstraint(self):  #遍历场景根据名称进行约束
        driverName = self.ui.driverNameLine.text()
        drivenName = self.ui.drivenNameLine.text()
        print  (driverName, drivenName)
        transformsObjects = cmds.ls(tr = True)
        for driverObj in transformsObjects:                                 #遍历场景中的物体
            if driverName in driverObj:                                     #查找驱动物体
                drivenObj =  driverObj.replace(driverName,drivenName)       #设置驱动物体名称
                if cmds.objExists(drivenObj):
                    cmds.parentConstraint(driverObj, drivenObj , mo = True) #约束物体

    def doPointConstraint(self): #遍历场景根据名称进行约束
        driverName = self.ui.driverNameLine.text()
        drivenName = self.ui.drivenNameLine.text()
        print  (driverName,drivenName)
        transformsObjects = cmds.ls(tr = True)
        for driverObj in transformsObjects:                                 #遍历场景中的物体
            if driverName in driverObj:                                     #查找驱动物体
                drivenObj =  driverObj.replace(driverName,drivenName)       #设置驱动物体名称
                if cmds.objExists(drivenObj):                               #确认被驱动物体是否存在
                    #print driverObj,drivenObj
                    cmds.pointConstraint(driverObj,drivenObj , mo = True)   #约束物体

    def doParentConstraint2(self ):  #遍历场景根据名称进行约束
        driverName = self.ui.driverNameLineSecond.text()
        drivenName = self.ui.drivenNameLineSecond.text()
        print  (driverName, drivenName)
        transformsObjects = cmds.ls(tr = True)
        for driverObj in transformsObjects:                                 #遍历场景中的物体
            if driverName in driverObj:                                     #查找驱动物体
                drivenObj =  driverObj.replace(driverName,drivenName)       #设置驱动物体名称
                if cmds.objExists(drivenObj):
                    cmds.parentConstraint(driverObj, drivenObj , mo = True) #约束物体

    def doPointConstraint2(self): #遍历场景根据名称进行约束
        driverName = self.ui.driverNameLineSecond.text()
        drivenName = self.ui.drivenNameLineSecond.text()
        print  (driverName,drivenName)
        transformsObjects = cmds.ls(tr = True)
        for driverObj in transformsObjects:                                 #遍历场景中的物体
            if driverName in driverObj:                                     #查找驱动物体
                drivenObj =  driverObj.replace(driverName,drivenName)       #设置驱动物体名称
                if cmds.objExists(drivenObj):                       #确认被驱动物体是否存在
                    cmds.pointConstraint(driverObj,drivenObj , mo = True)   #约束物体

    def doDeleteConstraint2(self):  # 遍历场景根据名称进行删除
        # driverName = self.ui.driverNameLine.text()
        drivenName = self.ui.drivenNameLineSecond.text()
        # print  driverName
        transformsObjects = cmds.ls(tr=True)
        for obj in transformsObjects:
            if "Constraint" in obj and drivenName in obj:  # 确认被约束物体
                cmds.delete(obj)  # 删除约束

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
