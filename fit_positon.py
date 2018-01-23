# -*- coding: utf-8 -*-

from maya import cmds


# 根据角色骨骼自动对位控制器位置。source_name为控制器名称， destination为移动目标。
def move_to_position(source_name, destination_name):
    if cmds.objExists(source_name) and cmds.objExists(destination_name):
        destination_position = cmds.xform(destination_name, q=True, translation=True, worldSpace=True)
        cmds.move(destination_position[0],destination_position[1],destination_position[2], source_name)
    else:
        print (source_name, destination_name)

move_list = [{"face_rig":"Head"},
                 {"face_constraint":""},
                 {"face_ctrl":""},
                     {"brows_left":"eye_control"},
                         {"brows_left_1_locator":"brows_left_1_bn"},
                         {"brows_left_2_locator":"brows_left_2_bn"},
                         {"brows_left_3_locator":"brows_left_3_bn"},
                     {"brows_right":"eye_control"},
                         {"brows_right_1_locator": "brows_right_1_bn"},
                         {"brows_right_2_locator": "brows_right_2_bn"},
                         {"brows_right_3_locator": "brows_right_3_bn"},
                     {"ctrl_grp": "Head"},
                         {"lowerEyelid_left_ctrl_locator": ""},
                             {"lowerEyelid_left": ""},
                                {"lowerEyelid_left_1_bn_ctrl": "lowerEyelid_left_1_bn"},
                                {"lowerEyelid_left_2_bn_ctrl": "lowerEyelid_left_2_bn"},
                                {"lowerEyelid_left_3_bn_ctrl": "lowerEyelid_left_3_bn"},
                                {"lowerEyelid_left_4_bn_ctrl": "lowerEyelid_left_4_bn"},
                                {"lowerEyelid_left_5_bn_ctrl": "lowerEyelid_left_5_bn"},
                         {"upperEyelid_left_ctrl_locator": ""},
                             {"lowerEyelid_left": ""},
                                {"upperEyelid_left_1_bn_ctrl": "upperEyelid_left_1_bn"},
                                {"upperEyelid_left_2_bn_ctrl": "upperEyelid_left_2_bn"},
                                {"upperEyelid_left_3_bn_ctrl": "upperEyelid_left_3_bn"},
                                {"upperEyelid_left_4_bn_ctrl": "upperEyelid_left_4_bn"},
                                {"upperEyelid_left_5_bn_ctrl": "upperEyelid_left_5_bn"},
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
                                        {"mouthCorner_right_locater": ""},             ] #位置信息对位字典


#根据字典对位所有位置信息
def set_position(obj_list):
    for element in obj_list:
        for key,value in element.items():
            move_to_position(key, value)

set_position(move_list)


