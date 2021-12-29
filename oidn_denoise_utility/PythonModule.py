def singleDenoise(self):
    import subprocess
    
    infile = hou.pwd().evalParm("infile")
    outfile = hou.pwd().evalParm("outfile")
    oidndir = hou.pwd().evalParm("oidndir")
    nrmlplane = hou.pwd().evalParm("nrmlplane")
    albedoplane = hou.pwd().evalParm("albedoplane")
    cmd = 'oidndenoise --hdr ' + infile + ' -o ' + outfile
        
    if nrmlplane == 1:
        normalfile = hou.pwd().evalParm("nrmlfile")
        cmd = cmd + " --nrm " + normalfile
        
    if albedoplane == 1:
        albedofile = hou.pwd().evalParm("albedofile")
        cmd = cmd + " -alb " + albedofile
    
    
    subprocess.call(cmd, shell=True, cwd = oidndir)

def batchDenoise(self):
    import subprocess
    
    denoiser = hou.pwd().evalParm("oidnexe")
    denoisedir = hou.pwd().evalParm("denoisedir")
    usenrml = hou.pwd().evalParm("busenormal")
    usealbedo = hou.pwd().evalParm("busealbedo")
    
    if usenrml == 1:
        nrmlaov = hou.pwd().evalParm("bnrmlfile")

    if usealbedo == 1:
        albedoaov = hou.pwd().evalParm("balbedofile")
  
    cmd = 'for %i in (*.pfm) do ' + denoiser + ' --hdr "%i" -o "%~ni_denoised.pfm" --nrm ' + nrmlaov + ' --alb ' + albedoaov      
#    print(cmd)
#    print(denoiser)
    subprocess.call(cmd, shell=True, cwd = denoisedir)
    
def singleConvert(self):
    import subprocess
    
    filetoconv = hou.pwd().evalParm("filetoconv")
    convtype = hou.pwd().evalParm("convtype")
    
    if convtype == 0:
        outputfile = filetoconv.replace(".exr",".pfm")
    if convtype == 1:
        outputfile = filetoconv.replace(".pfm",".exr")
        
    cmd = 'magick ' + filetoconv + ' ' + outputfile
    
    subprocess.call(cmd)
    
def batchConvert(self):
    import subprocess
    
    convdir = hou.pwd().evalParm("convdir")
    convtype = hou.pwd().evalParm("convtype")
    
    if convtype == 0:
        cmd = 'for %i in (*.exr) do magick -endian LSB "%i" "%~ni.pfm"'
    if convtype == 1:
        cmd = 'for %i in (*.pfm) do magick -endian LSB "%i" "%~ni.exr"'
        
    subprocess.call(cmd, shell=True, cwd = convdir)
    
    
    