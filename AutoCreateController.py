# -*-coding: utf-8 -*-
from maya import cmds
# import json
# import types
'''不能有重名的字符串'''
face_rig_dict = {
  "face_rig": [
    { "face_constraint": "face_constraint1" },
    {
      "face_ctrl": [
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
                            { "mouthCorner_left_locator_grp": "mouthCorner_left_locator" },
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
                            { "mouthCorner_right_locator_grp": "mouthCorner_right_locator" },
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
global depth
depth = 1
'''
递归路径，将路径按照[(path, depth)]的方式进行保存。
其中path为每一遍叶子的绝对路径
    depth为叶子的深度。
'''

final_list = []
def go_though_dict(json_data , path=""):
    global depth
    if isinstance(json_data, dict):
        #depth += 1
        for key in json_data:
            path = path + key + "-->"
            go_though_dict(json_data[key], path)
    elif isinstance(json_data, list):
        #print len(json_data)
        for i in range(len(json_data)):
            #print json_data[i]
            if isinstance(json_data[i], dict):
                for sub_key in json_data[i]:
                    depth += 1
                    go_though_dict(json_data[i], path)
                depth -= 1
            else:
                final_list.append((path + json_data[i],depth))
    else:
        final_list.append((path +json_data, depth))


go_though_dict(face_rig_dict)
order_list = sorted(final_list, key=lambda x:x[1])


def  create_tree(tree_leaf_edges):
    for element in order_list:
        element_list = element[0].split("-->")
        for i in  range(len(element_list)):
            if cmds.objExists(element_list[i]):
                print (("{} has been created already!").format(element_list[i]))
            else:
                if i!=0:
                    cmds.select(clear=True)
                    if "_loc" in element_list[i]:
                        cmds.spaceLocator(name=element_list[i])
                    elif "_bn_" in element_list[i] or "Joint" in element_list[i]:
                        cmds.joint(name=element_list[i])
                    else:
                        cmds.group(empty=True, name=element_list[i])
                    cmds.parent(element_list[i], element_list[i-1])
                else:
                    cmds.group(empty=True, name=element_list[i])
        print ("-------------------------------------------------------------------------")
        #cmds.group(name=element_list[i])

create_tree(tree_leaf_edges=order_list)



































