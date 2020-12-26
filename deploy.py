import os, sys, shutil, tarfile, datetime

#-----------------------------Parameter Def
#Output destination
destPath = './ccu_sbas_out'
destFileName = ''

#AP Image file path
#APSdcardImagePath = '../build/bootimg.txt'
APExt4FilePath = '../build/ext4img.txt'
APBootimgFilePath = '../build/bootimg.txt'
#MCU Image file path
#Switch Image file path
SwitchFilePath = '../build/switch'

#Argument list
listVehicle = ['RS4', 'JW1', 'CE']
listEvent = ['PROTO', 'MCAR', 'P1', 'P2', 'M', 'SOP']
inVehicle = ''
inEvent = ''

#Log print
logInfo = '[INFO]'
logError = '[ERROR]'

#-----------------------------Function Def
class customEx(Exception): 
    def __str__(self):
        return logError,"Input argument is incorrect"

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def createFolder(directory):
    try:
        if os.path.exists(directory):
            print(logInfo, 'TargetFloder exist, remove folder')
            shutil.rmtree(directory)
        print(logInfo, 'Make target floder')
        os.makedirs(directory)
    except OSError:
        print (logError, 'Creating directory. '+ directory)


def copyFileToDest(directory):
    dir, file = os.path.split(directory)
    print(logInfo, 'Copy file: ', os.path.join(dir,file))
    shutil.copyfile(os.path.join(dir, file),
    os.path.join(destPath, file))

def checkArgument(vehicle, event):
    global inEvent, inVehicle, destFileName

    if vehicle in listVehicle:
        print(logInfo, 'Vehicle Type [%s] exist'%vehicle)
        inVehicle = vehicle
    else:
        print(logError, 'Vehicle Type [%s] is incorrect'%vehicle)
        raise customEx

    if event in listEvent:
        print(logInfo, 'Event Type [%s] exist'%event)
        inEvent = event
    else:
        print(logError, 'Event Type [%s] is incorrect'%event)
        raise customEx
    
    destFileName = datetime.datetime.now().strftime('%Y%m%d') + '_' + inVehicle + '_' + inEvent

def copySwitchImageToDest(inputvehicle, inputevent):
    switchfilename = "".join(os.listdir(os.path.join(SwitchFilePath,inputvehicle)))
    copyFileToDest(os.path.join(SwitchFilePath, inputvehicle, switchfilename))

#--------------------------------Run
#Check argument and make compress file name(Vehicle, Event type)
checkArgument(sys.argv[1], sys.argv[2])

#make directory
createFolder(destPath)

#copy AP sdcard file
#copyFileToDest(APSdcardImagePath)

#copy AP rootfs file
copyFileToDest(APBootimgFilePath)
copyFileToDest(APExt4FilePath)

#copy MCU image 
#copyFileToDest()

#copy Switch image
copySwitchImageToDest(inVehicle, inEvent)

#compress all imge using tar
make_tarfile(destFileName + '.tar.gz', destPath)

#test print