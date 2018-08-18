import subprocess
import os


def runCPP(filepath, programInput,processTimeout):
    # this will compile the cpp and output result
    #filepath = r'/home/j/shareWindows/hw2/Adams, Danielle(da2435)/Submission attachment(s)/da2435_hw2_q1.cpp'

    temp = subprocess.call(["g++", filepath])

    #temp = subprocess.call("./a.out")
    temp1 = subprocess.Popen("./a.out",shell = True, stdout = subprocess.PIPE,stdin = subprocess.PIPE,stderr = subprocess.PIPE)
    #out,err = temp.communicate()
    try:
        out = temp1.communicate(input=programInput,timeout = processTimeout)
    except subprocess.TimeoutExpired:
        print("Timeout happened.\n")
        out = [[],[],["timeout"]]
        temp1.kill()
        #b'25\n5\n12\n103\n'
    return [temp,temp1,out]

def findStudentID(text):
    start = text.find("(")
    end = text.find(")")
    return text[start+1:end]

def cleanCPP(filepath):
    try:
        filedata = open(filepath, newline='', encoding="utf16").read()
    except:
        filedata = open(filepath, newline='').read()
    newdata = filedata.replace('#include "stdafx.h"',"").replace('뿃뻃',"")
    print("converted")
    f = open(filepath,'w')
    f.write(newdata)
    f.close()

    return
   


def getStudentCPPResults(directory, program_input,question,processTimeout):
    result = {"results":[]}

    print("running")
    for file in os.listdir(directory):
        subDir1 = directory+file#+"/"
        #print(file)
        if os.path.isdir(subDir1):
            #print(subDir1) # this is the first level 
            #print (findStudentID(subDir1))
            studentID=findStudentID(subDir1)
            for file in os.listdir(subDir1+"/"):
                subDir2 = subDir1+"/"+file#+"/"
                #print(subDir2)
                if os.path.isdir(subDir2):
                    for file in os.listdir(subDir2):
                        filename = os.fsdecode(file)
                        #print(filename)
                        if filename.endswith(question+".cpp"): 
                            # print(os.path.join(directory, filename))
                            print(subDir2+"/"+filename)
                            filepath = subDir2+"/"+filename
                            # get rid of #include "stdafx.h"
                            cleanCPP(filepath)
                            temp = runCPP(filepath, program_input,processTimeout)
                            #print (temp[0].returncode)
                            if temp[0] == 0:# if no error
                                #print(temp)
                                programresult = {"student_id":studentID,"output":temp[2][0]}
                                result["results"].append(programresult)
                            #print(filename)
                            continue
                        else:
                            continue
    return result
	
	
	
	


directory = r'/home/user/VMShared/homework #4/' # put location of folder here
question ='1' #question you are grading
program_input = b'4\n4\n' # the stdin
processTimeout = 2

results = getStudentCPPResults(directory, program_input,question,processTimeout)

print("done running")	


#below are the results
for x in results["results"]:
    print (str(x["student_id"]) + ";"+str(x["output"]) )