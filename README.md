
# About MakeWxs

MakeWxs aims to speed up work with the [WiX Toolset](https://wixtoolset.org/).

It enables partial automation of creating .wxs source files containing the installation components and the directory structure and defining the main .wxs source file containing the Package element and the .wixproj. The program was created originally for the author's personal use and to avoid using more complex tools (like the [HeatWave](https://www.firegiant.com/wix/heatwave/)).

MakeWxs is designed primarily to be used with **Wix v4**.


**IMPORTANT**: This project **is not** related to the WiX Toolset development in any way and does not use it. 

&nbsp;
# How to get and install MakeWxs

You can download MakeWxs installer from [here](https://jiristrouhal.wordpress.com/makewxs/download-makewxs). Run the MakeWxs.msi and do the following:
- Read carefully and accept the terms in the License Agreement.
- Choose the destination folder.
- Proceed with installation. 

&nbsp;
# Quick tutorial

MakeWxs will now help you to create directory and component structure for a simple msi package. 

As indicated in the [About](#about-makewxs) section, we will use Wix v4 together with MSBuild (here version 17.6.3).

1) Download the zip archive with a simple directory hierarchy, that we want to bundle into msi. Extract the *root* directory into some location by your choice. 
2) Run the **MakeWxs.exe** in the **MakeWxs installation folder**. 
3) Specify the **target directory**, where .wxs containing the directory structure and program components should be created. Here for example, it is the directory containing the **root** folder.
4) Specify the **source directory**, containing all the files to be bundled into msi package. In this case, it is the **root** folder itself.
5) Specify the project (msi package) **name** (*MWTutorial* for example) and click **Ok**. Five files should appear next to the root folder. 

<p style="margin-left: 50px;">  
    <img src="produced_files.png" alt= “Produced_files” width="200" height="150" >
</p>

6) Specify the attributes of the Package element in **MWTutorial.wxs**. 
    ```xml  
    <Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
        <Package Name="MWTutorial" Manufacturer="MyName" Version="1.2.3" UpgradeCode="##some guid">
            <MajorUpgrade DowngradeErrorMessage="A newer version has already been installed!" />
            <Feature Id="Main">
                <ComponentGroupRef />
            </Feature>
        </Package>
    </Wix>
    ```

7) Copy the *ComponentGroupRef* Elements from the **MWTutorial_group_refs.xml** under the *Main* Feature in the **MWTutorial.wxs**.
    ```xml
        ...
        <Feature Id="Main">
            <ComponentGroupRef Id="group_root_nonempty_dir"/>
            <ComponentGroupRef Id="Root"/>
        </Feature>
        ...
    ```
8) Build the project. Find and run the installer **MWTutorial.msi**.  
9) MWTutorial directory should appear in the Program Files (x86) with the following structure. Note that empty folder was excluded.
    ```cmd
    MWTutorial
    ├───textfile.txt
    └───nonempty_dir
        ├───emptymarkdown.md
        └───helloworld.py
    ```