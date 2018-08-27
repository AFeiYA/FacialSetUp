# -*- coding:utf-8 -*-
import maya.cmds as cmds
import math
import re
class CreateJointsOnSurface():
    def __init__(self):
        '''create joints on a surface depend on the span of the surface. '''
        self.grp=[]
        #self.joint = []

    def create_joints(self, name="lip", dir='V'):
        if cmds.ls(sl=True):
            nb = cmds.ls(sl=True)[0]
            shapeNode = cmds.listRelatives(nb, shapes=True)
            if cmds.nodeType(shapeNode[0])=="nurbsSurface":
                span = cmds.getAttr(shapeNode[0]+".spans"+dir)
                print(span)
                created_group_list=[]
                for i in range(span):
                    cmds.select(cl=True)
                    joint_name = name + "_joint" + "_" + str(i)
                    locator_name = joint_name.replace("_joint", "_locator")
                    point_on_surface_name = joint_name + "_pos"
                    grp_name = joint_name.replace("_joint", "_grp")
                    if not cmds.objExists(joint_name):
                        cmds.spaceLocator(name=locator_name)
                        cmds.select(cl=True)
                        cmds.joint(n=joint_name)
                        cmds.createNode("pointOnSurfaceInfo", name=point_on_surface_name)
                        cmds.setAttr(point_on_surface_name + ".parameter"+dir,  span * 1.0 / span * i)
                        if dir=='V':
                            cmds.setAttr(point_on_surface_name + ".parameterU", 1)
                        else:
                            cmds.setAttr(point_on_surface_name + '.parameterV', 1)
                        cmds.connectAttr(shapeNode[0] + ".worldSpace", point_on_surface_name + ".inputSurface")
                        cmds.connectAttr(point_on_surface_name + ".result.position", locator_name + ".translate")
                        cmds.parentConstraint(locator_name, joint_name)
                        cmds.select(locator_name, r=True)
                        cmds.group(name=grp_name)
                    else:
                        cmds.warning('%s is already created!'%joint_name)
                    created_group_list.append(grp_name)
                self.grp = created_group_list
            else:
                cmds.warning('You need select a nurbsSurface to create joints.')
        else:
            cmds.warning('Please select a object')
        self.end = self.grp.__len__()/4
        print(self.end)

    def batch_constraint(self, control_name='upperLip_secondary_ctrl',group_name='',add_at=False):
        if self.grp:
            for group_name in self.grp:
                cmds.parentConstraint(control_name, group_name, mo=True)
                if add_at:
                    if not cmds.attributeQuery(group_name+'_weight', n=control_name,exists=True ):
                        cmds.addAttr(control_name, ln=group_name+"_weight", at='float', min = 0, max = 1)
                        cmds.setAttr("%s.%s_weight"%(control_name, group_name), keyable=True)
                    else:
                        print('attr %s_weight exists'%group_name)
    def auto_set_end(self, end=0):
        if end==0:
            end = len(self.grp)/2
        else:
            end =end+1
        return end

    def linear_weight(self,lower_ctrl='lowerLip_ctrl', start=0, end=10, step=1):
        end = self.auto_set_end(end=end)
        for i in range(start, end, step):
            weight = 1.0 * abs(i-start+1)/abs(end+1-start)
            cmds.setAttr("%s.%s" % (lower_ctrl, 'lip_grp_%s_weight' % i), weight)

    def sin_weight(self,lower_ctrl='lowerLip_ctrl',start=0, end=10, step=1):
        end = self.auto_set_end(end=end)
        for i in range(start, end, step):
            weight = math.sin(math.pi* abs(i-start+1)/abs(end-start+1)/2.0)
            cmds.setAttr("%s.%s" % (lower_ctrl, 'lip_grp_%s_weight' % i), weight)

    def sqrt_weight(self, lower_ctrl='lowerLip_ctrl',start=0, end=10, step=1):
        end = self.auto_set_end(end=end)
        for i in range(start, end+1, step):
            cur_value = cmds.getAttr("%s.%s" % (lower_ctrl, 'lip_grp_%s_weight' % i))
            cmds.setAttr("%s.%s" % (lower_ctrl, 'lip_grp_%s_weight' % i), math.sqrt(cur_value))

    def reset_weight(self, lower_ctrl='lowerLip_ctrl', start=0, end =10):
        if len(self.grp)!=0:
            end = len(self.grp)
        for i in range(start, end):
            cmds.setAttr("%s.%s" % (lower_ctrl, 'lip_grp_%s_weight' % i), 0)

    def mirror_weight(self,control_name ='lowerLip_ctrl',name="lip", start=0, end = 10, axis = 11):
        for i in range(start,end,1):
            weight = cmds.getAttr("%s.%s"%(control_name, 'lip_grp_{0}_weight'.format(i)))
            cmds.setAttr("%s.%s" % (control_name, '%s_grp_%s_weight'%(name, (2*axis - i))), weight)
            print(i, 2*axis-i)

    def set_weight_expression(self, lower_ctrl = 'lowerLip_ctrl', upper_ctrl = 'upperLip_secondary_ctrl'):
        if self.grp:
            # regex1 = r'W+0'
            # regex2 = r'W+1'
            for group_name in self.grp:
                constraint = group_name + "_parentConstraint1"
                w0 = "%s.%sW0"%(constraint,lower_ctrl)
                w1 = "%s.%sW1"%(constraint,upper_ctrl)
                cmds.expression(s = '%s = 1-%s; '%(w1, w0))
                cmds.connectAttr("%s.%s_weight"%(lower_ctrl, group_name), w0)






# c=CreateJointsOnSurface()
# c.create_joints()
# c.batch_constraint()
# c.reset_weight(end=0)
# print (c.grp)
# c.batch_constraint(control_name='upperLip_secondary_ctrl')
# c.set_weight_expression()
# c.reset_weight()
# c.linear_weight()
# c.sin_weight()
# c.mirror_weight(start=7, end=10, axis=6)

