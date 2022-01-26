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

***selectednodes***
The material library nodes for the material network to be created in. This reads a single string or a list of strings which can be obtained through the `hou.ui.selectNode` function with `multiple_select=true`.

***matname*** 
This is the name of the material which will be appended to each node in the material network. Takes a string input that must be a valid node name. To validate names you can use `re.sub("[^0-9a-zA-Z\.]+", "_", name)`. To obtain names you can use `hou.ui.readInput()` which will return a tuple which you can take the [1] index of to get the string name. 

***importtextures***
This takes an integer of either 1 or 0 where 0 is True and 1 is False. This can be obtained through the `hou.ui.displayMessage()` function. If importtexture == 0 then the function will run `hou.ui.selectFile()` and have the user choose files for diffuse, roughness and normal. 


---

## splitToComponents

---
