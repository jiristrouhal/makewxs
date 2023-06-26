#   Created by Jiří Strouhal (2023).
#   Written in Python 3.10.10
#   Licensed under the MIT License. See the LICENSE in the project root folder. 
#   Public repository: https://github.com/jiristrouhal/makewxs.
#   Use MznStrouhal@gmail.com to reach the author.


import os
import xml.etree.ElementTree as et

WXS_SCHEMA_LINK = "http://wixtoolset.org/schemas/v4/wxs"
SDK = "Wixtoolset.Sdk/4.0.0"
DEFAULT_DOWNGRADE_MESSAGE = "A newer version has already been installed!"


WXS_OPENER = '<Wix xmlns=\"'+WXS_SCHEMA_LINK+'\">'
WXS_CLOSING = '</Wix>'

STANDARD_DIRECTORY_OPENING = "\t<StandardDirectory Id=\"ProgramFilesFolder\">"
STANDARD_DIRECTORY_CLOSING = "\t</StandardDirectory>"


def write_component_groups_ref_xml(target_path:str,refs:str,project_name:str)->None:
    with open(target_path+"/"+project_name+"_group_refs.xml",'w') as group_refs_xml: group_refs_xml.write(refs)

def write_component_wxs(target_path:str,components:str,project_name:str)->None:
    components = WXS_OPENER + '\n\n' + "<Fragment>" + components + "</Fragment>" + '\n' + WXS_CLOSING
    with open(target_path+"/"+project_name+"_components.wxs",'w') as component_wxs: component_wxs.write(components)

def write_dir_wxs(target_path:str,folders:str,project_name:str)->None:
    folders = STANDARD_DIRECTORY_OPENING + folders + '\n' + STANDARD_DIRECTORY_CLOSING
    folders = WXS_OPENER + '\n\n' + "<Fragment>\n" + folders + "\n</Fragment>" + '\n\n' + WXS_CLOSING
    with open(target_path+"/"+project_name+"_dirs.wxs",'w') as folder_wxs: 
        folder_wxs.write(folders)

def write_base_wxs_if_missing(target_path:str,project_name:str)->None:
    try: 
        et.parse(project_name+".wxs")
    except: 
        wxs_root = et.Element("Wix", attrib={"xmlns":WXS_SCHEMA_LINK})
        package = et.SubElement(wxs_root,"Package", attrib={"Name":project_name, "Manufacturer":"","Version":"M.m.p","UpgradeCode":""})
        et.SubElement(package,"MajorUpgrade", attrib={"DowngradeErrorMessage":DEFAULT_DOWNGRADE_MESSAGE})
        main_feature = et.SubElement(package,"Feature",attrib={"Id":"Main"})
        et.SubElement(main_feature,"ComponentGroupRef")
        et.indent(wxs_root,space="\t")
        et.ElementTree(wxs_root).write(os.path.join(target_path,project_name+".wxs"),encoding="UTF-8",xml_declaration=True)


def write_wixproj_if_missing(target_path:str,project_name:str)->None:
    try: 
        et.parse(project_name+".wixproj")
    except: 
        wxs_root = et.Element("Project", attrib={"Sdk":SDK})
        et.indent(wxs_root,space="\t")
        et.ElementTree(wxs_root).write(os.path.join(target_path,project_name+".wixproj"))

