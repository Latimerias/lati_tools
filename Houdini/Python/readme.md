# Josh Weber Houdini Import Utils Python Functions

This is a series of functions used to automate node creation originally used for imported BIM files for quick process visualization within solaris. 

For ease of use you can copy the .py files containing the functions into your houdini python library like this: `D:\Programs\side_effects\Houdini 19.0.478\python37\lib`

---

# Table of Functions:
- [mtlxUsdImporter](#mtlxUsdImporter)
- [splitToComponents](#splitToComponents)

---

## mtlxUsdImporter

mtlxUsdImporter(selectednodes, matname, importtextures)

This creates a material network using USD preview surfaces for viewport and materialX nodes for render materials. 

***selectednodes***         
The material library nodes for the material network to be created in. This reads a single string or a list of strings which can be obtained through the `hou.ui.selectNode` function with `multiple_select=true`. This means the function can create the same material in multiple material libraries.

***matname***   
This is the name of the material which will be appended to each node in the material network. Takes a string input that must be a valid node name. To validate names you can use `re.sub("[^0-9a-zA-Z\.]+", "_", name)`. To obtain names you can use `hou.ui.readInput()` which will return a tuple which you can take the [1] index of to get the string name. 

***importtextures***    
This takes an integer of either 1 or 0 where 0 is True and 1 is False. This can be obtained through the `hou.ui.displayMessage()` function. If importtexture == 0 then the function will run `hou.ui.selectFile()` and have the user choose files for diffuse, roughness and normal. 

---

## splitToComponents

splitToComponents(infile, removeprefix, generate_materials, importtextures, uvtransform, uvunwrap):

This splits the selected file into multiple components based on the unique name attribute values. Used for imported BIM files for quick procedural process visualization in Solaris.

***infile***             
This takes a string input for the absolute path to the file being imported. This can be obtained using `hou.ui.selectFile()`.

***removeprefix***            
This removes a prefix from the name attribute on the imported geometry, sometimes this happens when import files from BIM or CAD softwares and cna be used to simplify component/material names. For example if your name attribute has values like `my_architecture_project/Foundation` you would set `removeprefix = "my_architecture_project/" to return 'foundation'.

***generate_materials***                     
This takes a 0 or 1 integer where 0 is True and 1 is False. This can be obtained through the `hou.ui.displayMessage()` function. If set to 0 every component will get a generate a single materialX based network using the mtlxUsdImporter function with the material name set to the component name. 

***importtextures***            
This takes an integer of either 1 or 0 where 0 is True and 1 is False. This can be obtained through the `hou.ui.displayMessage()` function. If importtexture == 0 then the function will run `hou.ui.selectFile()` and have the user choose files for diffuse, roughness and normal. ***Warning*** this will ask for textures for every component in your project which can add up quickly.

***uvtransform***           
This takes an integer of either 1 or 0 where 0 is True and 1 is False. This can be obtained through the `hou.ui.displayMessage()` function. If set to 0 a uvtransform SOP will be appended to the end of each component geometry.

***uvunwrap***            
This takes an integer of either 1 or 0 where 0 is True and 1 is False. This can be obtained through the `hou.ui.displayMessage()` function. If set to 0 a uvunwrap SOP will be appended to the end of each component geometry.

---
