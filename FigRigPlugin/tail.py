import  maya.cmds as cmds
import re
def connect_joint_rotate(src='joint_a', dst='joint_b', control_name=None , mul_strength=1.0):
    #create a multiply connection from source to destination, use a control object named 'control_name' to control the input1
    #use mul_strength to control the input2
    connect_node = src+"_to_"+dst
    if cmds.objExists(connect_node):
        print(connect_node)
    else:
        connect_node = cmds.createNode('multiplyDivide', name = connect_node)

    cmds.connectAttr("%s.rotate"%src, "%s.input1"%connect_node, f=True)
    cmds.connectAttr("%s.output"%connect_node, "%s.rotate"%dst, f=True)
    if control_name:
        cmds.connectAttr( control_name, "%s.input2"%connect_node)
    else:
        cmds.setAttr("%s.input2"%connect_node, mul_strength,mul_strength,mul_strength)

def connect_to_child(root=None, target_attr = 'rotate', add_multiply = True):
    """select a joint,this function will connect the rotation of the joint to the rotation of its child step by step."""
    if root:
        control_name = root
        add_attr_double3(name=control_name, attr_name="offset")
        cmds.select(root, r=True)
        child = cmds.pickWalk(d="down")[0]
        while root != child:
            if add_multiply:
                connect_joint_rotate(src=root,dst= child , control_name=control_name+".offset")
            else:
                cmds.connectAttr("%s.%s"%(root, target_attr), "%s.%s"%(child, target_attr))
            root = child
            cmds.select(root, r=True)
            child = cmds.pickWalk(d = 'down')[0]

def duplicate_joint_only(node=''):
    ''' 1. duplicate a joint only '''
    if node:
        if cmds.objectType(node, isType="joint"):
            root = cmds.duplicate(node, parentOnly=True, name='%s_root' % node)[0]
            return root

def duplicate_joint_hierarchy(node=''):
    ''' 2. duplicate  joint hierarchy.  '''
    if node:
        if cmds.objectType(node, isType="joint"):
            fk_joint = cmds.duplicate(node, renameChildren=True)[0]
            return joint_hierarchy_list(fk_joint)

def joint_parent(node=''):
    if not node:
        node=cmds.ls(sl=True)[0]
    if cmds.objectType(node, isType='joint'):
        parent = cmds.listConnections(node, s=True, d=False , type="joint")[0]
        return parent

def joint_childern(node=''):
    if not node:
        node=cmds.ls(sl=True)[0]
    if cmds.objectType(node, isType='joint'):
        children = cmds.listConnections(node, s=False, d=True, type="joint")
        return children

def joint_hierarchy_list(root_joint):
    cmds.select(root_joint, hi=True, r=True)
    objects = cmds.ls(sl=True,type="joint")
    return objects

def auto_create_fk_orient_constraint(fk_list, joint_list):
    for i in range(len(fk_list)):
        cmds.orientConstraint(fk_list[i],joint_list[i] )


def auto_orient_to_target(source, destination):
    for i in range(len(source)):
        cmds.delete(cmds.orientConstraint(destination[i] , source[i]))



def add_attr_double3(name='', attr_name='offset'):
    if cmds.objExists(name):
        if not cmds.attributeQuery('offset', n=name, exists=True):
            cmds.addAttr(name, ln="offset", at='double3')
            cmds.addAttr(name, longName='offsetX', attributeType='double', parent=attr_name, defaultValue=1)
            cmds.addAttr(name, longName='offsetY', attributeType='double', parent=attr_name, defaultValue=1)
            cmds.addAttr(name, longName='offsetZ', attributeType='double', parent=attr_name, defaultValue=1)
            cmds.setAttr("%s.offsetX" % name, keyable=True)
            cmds.setAttr("%s.offsetY" % name, keyable=True)
            cmds.setAttr("%s.offsetZ" % name, keyable=True)
            return "%s.%s"%(name, attr_name)

def set_constraint_weight_expression(objects_list, type='orientConstraint'):
    """create expression for constraints. eg: weight1 = 1 - weight0. attr_a is weight0  attr_b is weight1,
    shape is the constraint type. eg: joint_skin_{num}_parentConstraint1.attr_a_W0
    """
    for i in range(len(objects_list)):
        constraint_node = cmds.listConnections(objects_list[i], type=type,shapes=True)[0]
        attr_weight0 =  cmds.listAttr(constraint_node, string='*W0')[0]
        attr_weight1 = cmds.listAttr(constraint_node,  string='*W1')[0]
        expression_str = '{0}.{2} = 1 - {0}.{1};'.format(constraint_node, attr_weight0, attr_weight1)
        cmds.expression(s=expression_str)
        #cmds.connectAttr(blend, constraint_node+"."+attr_weight0)
        # print(constraint_node,attr_weight0, attr_weight1)

def weight_controller(objects_list, controller='',type="orientConstraint" ):
    if not controller:
        controller=cmds.spaceLocator()[0]
    else:
        if not cmds.objExists(controller):
            cmds.spaceLocator(name=controller)
    attr = add_attr_float(name=controller)
    for i in range(len(objects_list)):
        constraint_node = cmds.listConnections(objects_list[i], type=type,shapes=True)[0]
        attr_weight0 =  cmds.listAttr(constraint_node, string='*W0')[0]
        cmds.connectAttr(attr,"%s.%s"%(constraint_node, attr_weight0), f=True)
    return controller

def add_attr_float(name='nurbsSphere1', attr_name='global_local_blend'):
    if not cmds.attributeQuery(attr_name, n=name, exists=True ):
        cmds.addAttr(name, longName=attr_name, defaultValue=1, minValue=0, maxValue=1)
        cmds.setAttr('%s.%s'%(name,attr_name), keyable=True)
    return '%s.%s'%(name,attr_name)

def set_joint_shape_to_circle(joint_name):
    if joint_name:
        circle_name = joint_name+"_cv"
        if not cmds.objExists(circle_name +'Shape'):
            cmds.delete(cmds.parentConstraint(joint_name, cmds.circle(n=circle_name,normal=(1,0,0))))
            cmds.parent(circle_name+"Shape", joint_name, s=True, r=True)
            cmds.delete(circle_name)
            cmds.setAttr("%s.drawStyle"%joint_name, 2)

def connect_to_list_elements(list, target_attr = 'rotate', add_multiply = True):
    """select a joint,this function will connect the rotation of the joint to the rotation of its child step by step."""
    if list:
        root = list[0]
        add_attr_double3(name=list[0], attr_name="offset")
        for i in range(len(list)-1):
            if add_multiply:
                connect_joint_rotate(src=list[i],dst= list[i+1] , control_name=root+".offset")
            else:
                cmds.connectAttr("%s.%s"%(list[i], target_attr), "%s.%s"%(list[i+1], target_attr))

def rename_fk_joint(joint_list, fk_joint_list, suffix="fk"):
    for i in range(len(joint_list)):
        cmds.rename(fk_joint_list[i], "%s_%s"%(joint_list[i], suffix) )
        fk_joint_list[i] = joint_list[i] + "_" + suffix
    return fk_joint_list

class Tail():
    def __init__(self):
        self.selected_joint = None
        self.ctrl_name = 'tail_control_loc'
        self.joint_list = []
        self.fk_local = []
        self.fk_global = []

    def create_rig(self):
        try:
            self.selected_joint = cmds.ls(sl=True)[0]
        except:
            cmds.error("Failed to query root selected root joint!")
        finally:
            try:
                self.joint_list = joint_hierarchy_list(self.selected_joint)
            except:
                cmds.error('Failed to query joint list')
            finally:
                if not cmds.objExists(self.selected_joint+"fk_global"):
                    self.fk_global = duplicate_joint_hierarchy(self.selected_joint)
                    self.fk_global = rename_fk_joint(self.joint_list, self.fk_global, suffix='fk_global')
                    cmds.setAttr("%s.template"%self.fk_global[1],1)
                if not cmds.objExists(self.selected_joint+"fk_local"):
                    self.fk_local = duplicate_joint_hierarchy(self.selected_joint)
                    self.fk_local = rename_fk_joint(self.joint_list, self.fk_local, suffix='fk_local')

                auto_create_fk_orient_constraint(self.fk_local, self.joint_list)
                auto_create_fk_orient_constraint(self.fk_global,self.joint_list)

                set_constraint_weight_expression(self.joint_list)

                self.ctrl_name = weight_controller(self.joint_list, controller=self.ctrl_name)#set local control with fk_a
                for joint in self.fk_global:
                    set_joint_shape_to_circle(joint)
                for joint in self.fk_local:
                    set_joint_shape_to_circle(joint)


                #set global control with fk_b

                connect_to_list_elements(self.fk_global)
                root = duplicate_joint_only(self.fk_global[0])
                cmds.parent(self.fk_global[0],root)
                connect_joint_rotate(self.fk_global[0], root, mul_strength=-0.5)
                #
                cmds.setDrivenKeyframe("%s.visibility"%self.fk_global[0] ,currentDriver="%s.global_local_blend"%self.ctrl_name,driverValue=0, value = 1)
                cmds.setDrivenKeyframe("%s.visibility"%self.fk_global[0] ,currentDriver="%s.global_local_blend"%self.ctrl_name,driverValue=1, value = 0)
                cmds.setDrivenKeyframe("%s.visibility"%self.fk_local[0] ,currentDriver="%s.global_local_blend"%self.ctrl_name,driverValue=0, value = 0 )
                cmds.setDrivenKeyframe("%s.visibility"%self.fk_local[0] ,currentDriver="%s.global_local_blend"%self.ctrl_name,driverValue=1, value = 1 )

    def set_to_local_fk(self):
        local_fk = joint_hierarchy_list(cmds.ls(sl=True)[0])
        global_fk =  joint_hierarchy_list(local_fk[0].replace("local", "global"))
        auto_orient_to_target(local_fk, global_fk)




t =  Tail()
t.create_rig()

