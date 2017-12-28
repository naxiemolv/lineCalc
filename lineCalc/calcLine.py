# -*- coding:utf-8 -*-
import os,re
import linecache
files = []

# 查询后缀
suffixs = [".h",".c",".m",".hpp",".cpp",".mm"]

# 过滤的文件夹
filterDirName = ["YYKit"]



regexps = {'.py': ['(.*#.*)|(.*\'\'\'.*\'\'\'.*)', '.*\'\'\'.*', '.*\'\'\'.*'],
           '.h': ['.*//.*|(.*/\*.*\*/.*)', '.*/\*.*', '.*\*/.*'],
           '.hpp': ['.*//.*|(.*/\*.*\*/.*)', '.*/\*.*', '.*\*/.*'],
           '.m': ['.*//.*|(.*/\*.*\*/.*)', '.*/\*.*', '.*\*/.*'],
           '.mm': ['.*//.*|(.*/\*.*\*/.*)', '.*/\*.*', '.*\*/.*'],
           '.c': ['.*//.*|(.*/\*.*\*/.*)', '.*/\*.*', '.*\*/.*']
           }


SPMODE = "\n"

totalLine = 0

def fetchDir(path):
    traverse(path)
def traverse (path):
    parents = os.listdir(path)

    for parent in parents:
        child = os.path.join(path,parent)

        if os.path.isdir(child):
            isFilted = False
            for dirs in filterDirName:
                print(child)
                print(dirs)
                if child.endswith(dirs):
                    isFilted = True
                    break
            if isFilted:
                pass
            else:
                traverse(child)
        else:
            if anyf(child) == True:
                files.append(child)
def anyf(filePath):
    for suffix in suffixs:
        if filePath.endswith(suffix):
            return True
    return False

def parserFile():
    for filePath in files:
        print("文件=>"+filePath)
        suffix = "."+filePath.split(".")[-1]

        linecache.clearcache()
        lines = linecache.getlines(filePath)
        parserLines(lines,suffix)

def parserLines(lines,suffix):
    global totalLine
    patterns = regexps[suffix]
    isMuti = False
    current = 0
    for line in lines :
        if regexMatch(line, patterns[0]) and isMuti == False:
            if line.replace(" ","").replace("\t","").startswith("//"):
                pass
            else:
                print(line)
                totalLine+=1
                current+=1
        else :
            if isMuti :
                if regexMatch(line, patterns[2]):
                    isMuti = False
                else :
                    pass
            else :
                isMuti = regexMatch(line, patterns[1])
                if isMuti:
                    
                    if regexMatch(line, patterns[2]):
                    	isMuti = False
                    	line = replaces(line)
                    	if line.startswith("/*"):
                    		if line.endswith("*/"):
                    			continue
                    	else:
                    		totalLine+=1
                    		current+=1


                    
                else:
                    
                    sline = replaces(line)
                    if len(sline)>0:
                        totalLine+=1
                        current+=1
    print("此文件代码数:%d"%(current)+"  总计:%d"%(totalLine))
def replaces(line):
	return line.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
def regexMatch(text, pattern) :
    p = re.compile(pattern)
    m = p.match(text)
    return m

def main():
    document = raw_input("拖入文件夹:")
    fetchDir(document.replace(" ",""))
    parserFile()

if __name__ == '__main__':
    main()