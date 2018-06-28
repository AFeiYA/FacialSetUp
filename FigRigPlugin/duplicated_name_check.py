#!/usr/bin/python
# -*- coding: utf-8 -*-
import unicodedata
import re
import maya.cmds as cmds
def duplicated_transform_nodes():
    d_list=[]
    tr_nodes =  cmds.ls( tr=True)
    filter(None, tr_nodes)   #remove NoneType
    maj_set = set(tr_nodes)
    duplicates = [f for f in maj_set if '|' in f]
    duplicates.sort(key=lambda obj:obj.count('|'), reverse = True)
    if duplicates:
        for name in duplicates:
            # extract the base name
            m = re.compile("[^|]*$").search(name)
            short_name=m.group(0)
            d_list.append(short_name)
    d_set = set(d_list)
    warning=""
    for d_name in d_set:
        warning += str(d_list.count(d_name))+u'个叫' + d_name + u'在场景中'+"\n"+"\n"
        #warning += str(d_list.count(d_name))+" objects named "+d_name +"in the scene!"+"\n"
    if warning:
        cmds.confirmDialog( title=u'重名检查', message=warning, button = u"确认")
    else:
        cmds.confirmDialog( title=u'重名检查', message="Scene is cleaned", button = u"确认")
duplicated_transform_nodes()