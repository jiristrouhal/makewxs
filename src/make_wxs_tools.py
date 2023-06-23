import os
from write_wxs_files import *
from typing import Tuple


def get_wxs_files(source_path:str, target_path:str, project_name:str)->None:
    components, dirs, group_refs = __collect_from_subdirs(source_path,2,target_path)

    source_relpath_id = __dir_id(os.path.relpath(source_path,target_path))

    components = components.replace(f'\"group_{source_relpath_id}\"','\"Root\"')
    components = components.replace(f'\"{source_relpath_id}\"','\"INSTALLFOLDER\"')

    group_refs = group_refs.replace(f'\"group_{source_relpath_id}\"','\"Root\"')
    group_refs = group_refs.replace(f'\"{source_relpath_id}\"','\"INSTALLFOLDER\"')

    dirs = __new_folder(project_name,"INSTALLFOLDER", dirs, 2)

    write_component_wxs(target_path,components,project_name)
    write_component_groups_ref_xml(target_path,group_refs,project_name)
    write_dir_wxs(target_path,dirs,project_name)
    write_base_wxs_if_missing(target_path,project_name)
    write_wixproj_if_missing(target_path,project_name)


def __collect_from_subdirs(source_dir_path:str,indent:int,root_dir_path:str)->Tuple[str,str,str]:
    component_groups, dirs, group_refs = "", "", ""

    for item in os.listdir(source_dir_path):

        itempath = os.path.join(source_dir_path,item)

        if os.path.isdir(itempath):
            subd_components, subd_dirs, subd_group_refs = __collect_from_subdirs(itempath,indent+1,root_dir_path)
            if subd_components.strip() == "": continue
            component_groups += '\n'+subd_components
            dirs += __new_folder(item,__dir_id(os.path.relpath(itempath,root_dir_path)),subd_dirs,indent+1)
            if subd_group_refs.strip()!="": group_refs += subd_group_refs 

    curr_dir_id = __dir_id(os.path.relpath(source_dir_path,root_dir_path))
    components = __collect_components(source_dir_path, root_dir_path)
    if not components.strip()=="":
        component_groups += __new_group(__group_id(curr_dir_id),curr_dir_id,components)
        group_refs += '\n'+__new_group_ref(__group_id(curr_dir_id))

    return component_groups, dirs, group_refs

    
def __new_folder(name:str,id:str,content:str,indents:int)->str:
    opening = "\n"+"\t"*indents + f'<Directory Name=\"{name}\" Id=\"{id}\">'
    closing = "\t"*indents + '</Directory>'
    if content.strip()!="": 
        content = content+'\n'
        return opening + content + closing
    else:
        return opening + ' </Directory>'

def __new_component(relpath:str)->str:
    return '\t\t' + f'<Component> <File Source=\"{relpath}\"/> </Component>'

def __collect_components(source_path:str,root_dir_path:str)->str:
    collected = ""
    for item in os.listdir(source_path):
        itempath = os.path.join(source_path,item)
        if os.path.isfile(itempath): 
            collected += '\n'+__new_component(os.path.relpath(itempath,root_dir_path))
    return collected

def __new_group(group_id:str,directory:str,components:str)->str:
    opening = f'\t<ComponentGroup Id=\"{group_id}\" Directory=\"{directory}\">'
    closing = '\t</ComponentGroup>\n'
    if components.strip()=="": return opening + closing
    return opening + components + '\n' + closing

def __new_group_ref(id:str)->str:
    return f'<ComponentGroupRef Id=\"{id}\"/>'

def __dir_id(dirpath:str)->str: return dirpath.replace("/","_").replace("\\",'_').replace(":","")
def __group_id(dir_id:str)->str: return 'group_'+dir_id
