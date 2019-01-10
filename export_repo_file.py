#!/usr/bin/env python
import datetime
import os,sys
import shutil

# get current directory
currDir = os.getcwd()
print 'currDir ' + currDir

# create patch dir
nowTime = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
patch_dir = '_diff_patch_' + nowTime
os.mkdir(patch_dir)

# create file list
fileList = patch_dir + "/fileList.txt"
if os.path.exists(fileList):
    os.remove(fileList)
fileList = open(fileList, "a+")

# define build.prop path
otherList = [
    "out/target/product/rk3288/system/build.prop",
]

project_name = ""
result = os.popen('repo status')
res = result.read()  # type: unicode
for line in res.splitlines():
    print line

    # copy diff file
    if line.startswith("project"):
        line = line.split(' ')[1]
        project_name = line.replace('/', '')
        print "project_name:" + project_name
    elif "NO BRANCH" in line:
        print "ignore:" + line
    elif len(line.strip()) > 0:
        fileMark = line.split('	')[0]
        filePath = line.split('	')[1]
        print "file:" + filePath
        filePath = project_name + '/' + filePath  # type: unicode
        lastIdx = filePath.rindex('/')
        fileDir = ""
        if lastIdx > 0:
            fileDir = patch_dir + '/' + filePath[:lastIdx]
            print "fileDir:" + fileDir
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
        
        if os.path.exists(filePath) and  os.path.isfile(filePath):
            shutil.copyfile(filePath, patch_dir + '/' + filePath)
            try:
                fileList.write( fileMark + ' ' + filePath + '\n')
            except IOError:
                print '*** file open error:' + fileList

# copy other file
for otherFile in otherList:
    if os.path.exists(otherFile):
        lastIdxN = otherFile.rindex('/')
        fileDir = ""
        if lastIdxN > 0:
            fileDir = patch_dir + '/' + otherFile[:lastIdxN]
            print "fileDir:" + fileDir
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
        shutil.copyfile(otherFile, patch_dir + '/' + otherFile)
        try:
            fileList.write("other" + ' ' + otherFile + '\n')
        except IOError:
            print '*** file open error:' + fileList
