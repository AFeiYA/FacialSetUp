# -*-coding: utf-8 -*-
# from maya import cmds
# import json
# import types
from anytree import RenderTree, Node
from anytree.importer import DictImporter

importer = DictImporter()

face_rig_dict = {
  "root": "face_rig",
  "children": [
    { "face_constraint": "face_constraint" },
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
                    "lowerEyelid_left_3_bn_ctrl"
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
                    "upperEyelid_left_3_bn_ctrl"
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
                            { "mouthCorner_left_locater_grp": "mouthCorner_left_locater" },
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
                            { "mouthCorner_right_locater_grp": "mouthCorner_right_locater" },
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

data = {"a":"root", 'children': [{'a': 'sub0','children': [{'a': 'sub0A', 'b': 'foo'}, {'a': 'sub0B'}]},{'a': 'sub1'}]}
root = importer.import_(data)
rootB = importer.import_(face_rig_dict)
print(RenderTree(root))
print(RenderTree(rootB))

dict = {"a":"b", "c":"d"}
print (len(dict))