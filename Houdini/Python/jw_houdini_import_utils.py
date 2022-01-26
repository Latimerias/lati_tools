## This creates a mtlx network for use with USD in solaris.
def mtlxUsdImporter(selectednodes, matname, importtextures):
    for nodepath in selectednodes:
    
        if importtextures == 0:
            diffuse_texture = hou.ui.selectFile(title='Diffuse Texture For ' + matname)
            roughness_texture = hou.ui.selectFile(title='Roughness Texture For ' + matname)
            normal_texture = hou.ui.selectFile(title='Normal Texture For ' + matname)
        elif importtextures == 1:
            diffuse_texture = ""
            roughness_texture = ""
            normal_texture = ""

        matlib_node = hou.node(nodepath)
        ## create nodes
        collect_node = matlib_node.createNode("collect", matname)
        mtlxstandsurf_node = matlib_node.createNode("mtlxstandard_surface", "mtlxstandard_surface_" + matname)
        usdpreviewsurf_node = matlib_node.createNode("usdpreviewsurface", "usdpreviewsurface_" + matname)
        usddiff_node = matlib_node.createNode("usduvtexture::2.0", "usduvtexture_diffuse_" + matname)
        usdrough_node = matlib_node.createNode("usduvtexture::2.0", "usduvtexture_roughness_" + matname)
        mtlxtexcoord_node = matlib_node.createNode("mtlxtexcoord", "mtlxtexcoord_" + matname)
        mtlxdiff_node = matlib_node.createNode("mtlximage", "mtlximage_diffuse_" + matname)
        mtlxrough_node = matlib_node.createNode("mtlximage", "mtlximage_roughness_" + matname)
        mtlxnrml_node = matlib_node.createNode("mtlximage", "mtlximage_normal_" + matname)
        mtlxnrmlmap_node = matlib_node.createNode("mtlxnormalmap", "mtlxnormalmap_" + matname)
        
        ## connect nodes
        collect_node.setInput(0, usdpreviewsurf_node, 0)
        collect_node.setInput(1, mtlxstandsurf_node, 0)
        usdpreviewsurf_node.setInput(0, usddiff_node, 4)
        usdpreviewsurf_node.setInput(5, usdrough_node, 0)
        mtlxstandsurf_node.setInput(1, mtlxdiff_node, 0)
        mtlxstandsurf_node.setInput(6, mtlxrough_node, 0)
        mtlxstandsurf_node.setInput(40, mtlxnrmlmap_node, 0)
        mtlxnrmlmap_node.setInput(0, mtlxnrml_node, 0)
        mtlxnrml_node.setInput(1, mtlxtexcoord_node, 0)
        mtlxdiff_node.setInput(1, mtlxtexcoord_node, 0)
        mtlxrough_node.setInput(1, mtlxtexcoord_node, 0)
        matlib_node.layoutChildren()
        
        ## set parameters
        mtlxtexcoord_node.parm('signature').set('vector2')
        usddiff_node.parm('sourceColorSpace').set('sRGB')
        usdrough_node.parm('sourceColorSpace').set('raw')
        mtlxdiff_node.parm('filecolorspace').set('srgb_texture')
        mtlxrough_node.parm('filecolorspace').set('srgb_texture')
        mtlxnrml_node.parm('filecolorspace').set('srgb_texture')
        mtlxrough_node.parm('signature').set('float')
        mtlxnrml_node.parm('signature').set('vector3')
        
        usddiff_node.parm('file').set(diffuse_texture)
        usdrough_node.parm('file').set(roughness_texture)
        mtlxdiff_node.parm('file').set(diffuse_texture)
        mtlxrough_node.parm('file').set(roughness_texture)
        mtlxnrml_node.parm('file').set(normal_texture)
        
        ## turn off render flags
        
        mtlxstandsurf_node.setMaterialFlag(False)
        usdpreviewsurf_node.setMaterialFlag(False)
        
def splitToComponents(infile, removeprefix, generatematerials, importtextures, uvtransform, uvunwrap):        
    import re
    
    ## set node context
    stage = hou.node('/stage')   

    ## import file in sopnet
    sopnet_node = stage.createNode('sopnet', "objectimport")
    file_node = sopnet_node.createNode('file')
    file_node.parm('file').set(infile)

    ## remove prefix 
    name_node = sopnet_node.createNode('name')
    name_node.setInput(0, file_node, 0)
    name_node.parm('numnames').set(0)
    name_node.parm('numrenames').set(1)
    name_node.parm('from1').set(removeprefix + "*")
    name_node.parm('to1').set("*")

    ## create output null
    null_node = sopnet_node.createNode('null', 'OUT')
    null_node.setInput(0, name_node, 0)
    sopnet_node.layoutChildren()

    ## get name attrib from file
    filegeo = null_node.geometry()
    name_attribs = filegeo.findPrimAttrib('name').strings()

    ## create component builder for each name
    for name in name_attribs:
        
        ## create component geo
        geo_node = stage.createNode('componentgeometry')
        geosubpath = geo_node.path() ## component geo uses subnetsworks this gets that node
        geosub_node = hou.node(geosubpath + "/sopnet/geo")
        objmerge_node = geosub_node.createNode('object_merge')
        objmerge_node.parm('objpath1').set(null_node.path())
        suboutput_node = hou.node(geosubpath + "/sopnet/geo/default")
        
        ## delete extra geometry
        delextra_node = geosub_node.createNode('blast')
        delextra_node.parm('group').set("@name=" + name)
        delextra_node.parm('negate').set(1)
        
        ## delete attributes and groups
        attribdelete_node = geosub_node.createNode('attribdelete')
        groupdelete_node = geosub_node.createNode('groupdelete')
        attribdelete_node.parm('negate').set(1)
        attribdelete_node.parm('ptdel').set("P")
        attribdelete_node.parm('vtxdel').set("N uv")
        groupdelete_node.parm('group1').set("*")
        
        ## set geo node inputs
        delextra_node.setInput(0, objmerge_node, 0)
        attribdelete_node.setInput(0, delextra_node, 0)
        groupdelete_node.setInput(0, attribdelete_node, 0)
        suboutput_node.setInput(0, groupdelete_node, 0)
        
        ## create component material
        matlib_node = stage.createNode('materiallibrary')
        
        ## turn name variable into houdini compatible node names
        nodename = re.sub("[^0-9a-zA-Z\.]+", "_", name)
        
        ## component output nodes
        assignmat_node = stage.createNode('componentmaterial')
        componentoutput_node = stage.createNode('componentoutput', nodename)
        assignmat_node.setInput(0, geo_node, 0)
        assignmat_node.setInput(1, matlib_node, 0)
        componentoutput_node.setInput(0, assignmat_node, 0)
        stage.layoutChildren()

        ## Create UV Transform Nodes
        if (uvtransform == 0) and (uvunwrap == 0):
            uvtrans_node = geosub_node.createNode('uvtransform::2.0')
            uvunwrap_node = geosub_node.createNode('uvunwrap')
            uvunwrap_node.setInput(0, groupdelete_node, 0)
            uvtrans_node.setInput(0, uvunwrap_node, 0)
            suboutput_node.setInput(0, uvtrans_node, 0)

        elif (uvtransform == 0) and (uvunwrap == 1):
            uvtrans_node = geosub_node.createNode('uvtransform::2.0')   
            uvtrans_node.setInput(0, groupdelete_node, 0)
            suboutput_node.setInput(0, uvtrans_node, 0)

        elif (uvtransform == 1) and (uvunwrap == 0):
            uvunwrap_node = geosub_node.createNode('uvunwrap')   
            uvunwrap_node.setInput(0, groupdelete_node, 0)
            suboutput_node.setInput(0, uvunwrap_node, 0)   

        geosub_node.layoutChildren()

        ## autogenerate materials
        if generatematerials == 0:  
            
            matname = nodename
        
            if importtextures == 0:
                diffuse_texture = hou.ui.selectFile(title='Diffuse Texture For ' + matname)
                roughness_texture = hou.ui.selectFile(title='Roughness Texture For ' + matname)
                normal_texture = hou.ui.selectFile(title='Normal Texture For ' + matname)
            elif importtextures == 1:
                diffuse_texture = ""
                roughness_texture = ""
                normal_texture = ""
    
            ## create nodes
            collect_node = matlib_node.createNode("collect", matname)
            mtlxstandsurf_node = matlib_node.createNode("mtlxstandard_surface", "mtlxstandard_surface_" + matname)
            usdpreviewsurf_node = matlib_node.createNode("usdpreviewsurface", "usdpreviewsurface_" + matname)
            usddiff_node = matlib_node.createNode("usduvtexture::2.0", "usduvtexture_diffuse_" + matname)
            usdrough_node = matlib_node.createNode("usduvtexture::2.0", "usduvtexture_roughness_" + matname)
            mtlxtexcoord_node = matlib_node.createNode("mtlxtexcoord", "mtlxtexcoord_" + matname)
            mtlxdiff_node = matlib_node.createNode("mtlximage", "mtlximage_diffuse_" + matname)
            mtlxrough_node = matlib_node.createNode("mtlximage", "mtlximage_roughness_" + matname)
            mtlxnrml_node = matlib_node.createNode("mtlximage", "mtlximage_normal_" + matname)
            mtlxnrmlmap_node = matlib_node.createNode("mtlxnormalmap", "mtlxnormalmap_" + matname)
            
            ## connect nodes
            collect_node.setInput(0, usdpreviewsurf_node, 0)
            collect_node.setInput(1, mtlxstandsurf_node, 0)
            usdpreviewsurf_node.setInput(0, usddiff_node, 4)
            usdpreviewsurf_node.setInput(5, usdrough_node, 0)
            mtlxstandsurf_node.setInput(1, mtlxdiff_node, 0)
            mtlxstandsurf_node.setInput(6, mtlxrough_node, 0)
            mtlxstandsurf_node.setInput(40, mtlxnrmlmap_node, 0)
            mtlxnrmlmap_node.setInput(0, mtlxnrml_node, 0)
            mtlxnrml_node.setInput(1, mtlxtexcoord_node, 0)
            mtlxdiff_node.setInput(1, mtlxtexcoord_node, 0)
            mtlxrough_node.setInput(1, mtlxtexcoord_node, 0)
            matlib_node.layoutChildren()
            
            ## set parameters
            mtlxtexcoord_node.parm('signature').set('vector2')
            usddiff_node.parm('sourceColorSpace').set('sRGB')
            usdrough_node.parm('sourceColorSpace').set('raw')
            mtlxdiff_node.parm('filecolorspace').set('srgb_texture')
            mtlxrough_node.parm('filecolorspace').set('srgb_texture')
            mtlxnrml_node.parm('filecolorspace').set('srgb_texture')
            mtlxrough_node.parm('signature').set('float')
            mtlxnrml_node.parm('signature').set('vector3')
            
            usddiff_node.parm('file').set(diffuse_texture)
            usdrough_node.parm('file').set(roughness_texture)
            mtlxdiff_node.parm('file').set(diffuse_texture)
            mtlxrough_node.parm('file').set(roughness_texture)
            mtlxnrml_node.parm('file').set(normal_texture)
            
            ## turn off render flags
            
            mtlxstandsurf_node.setMaterialFlag(False)
            usdpreviewsurf_node.setMaterialFlag(False)