import errno
import os
import traceback
from winsound import Beep

from tqdm import tqdm

NCOLS=70
SELF_NAME='BitSinger'
VERSION='1.0.0'

DEFAULT_FREQ_START=100
DEFAULT_FREQ_STEP=4
DEFAULT_DURA=500
DEFAULT_NCOLS=60

#====Language System.Supports zh and en(default)====#
SYSTEM_LANGUAGE=0
try:
    import win32api
    SYSTEM_LANGUAGE=win32api.GetSystemDefaultLangID()
except:pass

def getStrByLanguage(en='',zh=''):
    if SYSTEM_LANGUAGE==0x804:return zh
    return en
def gsbl(en='',zh=''):return getStrByLanguage(en=en,zh=zh)
def prbl(en='',zh=''):return print(gsbl(en=en,zh=zh))
def inputBL(en='',zh=''):return input(gsbl(en=en,zh=zh))
def printPath(message,path):return print(message%('\"'+path+'\"'))
def printPathBL(path,en,zh):return printPath(gsbl(en=en,zh=zh),path=path)
#New
def inputIntWithDefaultValueBL(en='',zh='',defaultValue=50,minV=0,maxV=0xffff):return inputIntWithDefaultValue(head=gsbl(en=en,zh=zh)%defaultValue,defaultValue=defaultValue,minV=minV,maxV=maxV)
def inputStrListBL(en='',zh='',endChar=''):return inputStrList(gsbl(en=en,zh=zh),endChar=endChar)

#====Functions Utils====#
def printExcept(exc,funcPointer):
    print(funcPointer+gsbl(en="A exception was found:",zh="\u53d1\u73b0\u5f02\u5e38\uff1a"),exc,"\n"+traceback.format_exc())

def InputYN(head,defaultFalse=True):
    yn=input(head)
    if not bool(yn):
        return False
    elif defaultFalse and (yn.lower()=='n' or yn.lower()=="no" or yn.lower()=="false" or yn in '\u5426\u9634\u9682\u9519\u53cd\u5047'):
        return False
    return yn.lower()=='y' or yn.lower()=="yes" or yn.lower()=="true" or yn in '\u662f\u9633\u967d\u5bf9\u6b63\u771f'

#====Functions about IO====#
def readFileBytes(path):
    try:
        file0=open(path,'rb')
        if file0==None:
            return (False,FileNotFoundError(path))
        return (True,file0.read())
    except BaseException as error:return (False,error)
#returns (success,bytes/error)

def inputIntWithDefaultValue(head,defaultValue=50,minV=0,maxV=0xffff):
    result=defaultValue
    try:
        if maxV<minV:result=int(input(head))
        else:result=min(max(int(input(head)),minV),maxV)
    except:
        pass
    return result

def inputStrList(head,endChar=''):
    result=[]
    i=input(head)
    while(i!=endChar):
        result.append(i)
        i=input(head)
    return result
#returns list

#====Functions about Singing====#
#returns (list,int)
def generateSingContext(duration=DEFAULT_DURA,freqStart=DEFAULT_FREQ_START,freqStep=DEFAULT_FREQ_STEP):
    fList=[(freqStart+freqStep*x) for x in range(0,256)]
    return (fList,duration)

def playBytesWithContext(Bytes,context):
    for i in tqdm(Bytes,desc='',ncols=50):
        Beep(context[0][int(i)],context[1])

def playBytes(Bytes,duration=DEFAULT_DURA,freqStart=DEFAULT_FREQ_START,freqStep=DEFAULT_FREQ_STEP):
    playBytesWithContext(Bytes,generateSingContext(duration,freqStart,freqStep))

def singByteList(bList,context):
    for b in bList:
        playBytesWithContext(b,context=context)

def singFileList(pathList,context):
    bList=[]
    for path in pathList:
        b=readFileBytes(path=path)
        if b[0]==True:
            bList.append(b[1])
    singByteList(bList,context=context)

def singFileBytes(path,context):
    b=readFileBytes(path=path)
    if b[0]==True:
        playBytesWithContext(b[1],context)

def singByCMDLine(pathList=None):
    pList=pathList
    if pList==None:pList=inputStrListBL(en='Please append PATH:',zh='\u8bf7\u8ffd\u52a0\u8def\u5f84\uff1a')
    dura=inputIntWithDefaultValueBL(en='Please input <duration=%s>:',zh='\u8bf7\u8f93\u5165\u003c\u6301\u7eed\u65f6\u95f4\u003d%s\u003e\uff1a',defaultValue=DEFAULT_DURA,minV=100,maxV=0xfff)
    freqStart=inputIntWithDefaultValueBL(en='Please input <freqStart=%s>:',zh='\u8bf7\u8f93\u5165\u003c\u8d77\u59cb\u9891\u7387\u003d%s\u003e\uff1a',defaultValue=DEFAULT_FREQ_START,minV=37,maxV=32767)
    freqStep=inputIntWithDefaultValueBL(en='Please input <freqStep=%s>:',zh='\u8bf7\u8f93\u5165\u003c\u9012\u589e\u9891\u7387\u003d%s\u003e\uff1a',defaultValue=DEFAULT_FREQ_STEP,minV=0,maxV=-1)
    singFileList(pathList=pList,context=generateSingContext(duration=dura,freqStart=freqStart,freqStep=freqStep))

#====Function in CommandLine====#
def cmdLineMode():
    print("<===="+SELF_NAME+" v"+VERSION+"====>")
    while(True):
        try:
            singByCMDLine(None)
        except BaseException as e:
            printExcept(e,"cmdLineMode()->")
        print()#new line

#====Function Main====#
try:
    if __name__=='__main__':
        import sys
        if len(sys.argv)>1:
            try:
                singByCMDLine(sys.argv[1:])
            except BaseException as error:
                catchExcept(error,file_path,"main->")
            print()
        else:
            cmdLineMode()
except BaseException as e:
    printExcept(e,"main->")
    if InputYN((gsbl(en="Do you need to switch to command line mode?",zh="\u4f60\u9700\u8981\u5207\u6362\u5230\u547d\u4ee4\u884c\u6a21\u5f0f\u5417\uff1f")+"Y/N:")):
        cmdLineMode()