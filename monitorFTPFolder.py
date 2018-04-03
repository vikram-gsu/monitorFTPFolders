from ftplib import FTP
from time import sleep
import re
import time
from submitWuid import submitWorkunit
from subprocess import run
# from io import BytesIO
# import json
import sys
sys.path.insert(0, './config')
import keys

dConfig = keys.getConfig()
ftp_userID = dConfig['credentials']['ftp']['userID']
ftp_password = dConfig['credentials']['ftp']['password']

hpcc_userID = dConfig['credentials']['hpcc']['userID']
hpcc_password = dConfig['credentials']['hpcc']['password']


# r = BytesIO()
# ftp.retrbinary('RETR keys.json', r.write) # retrieving keys file from ftp
# dConfig = json.loads(r.getvalue())

def changemon(dir=dConfig['landingZone']):
    ls_prev = set()

    while True:
        ftp = FTP(dConfig['serverIP'], timeout=2000)
        ftp.login(user=ftp_userID, passwd = ftp_password) #enter FTP ID and password

        ls = set(ftp.nlst(dir))

        add, rem = ls-ls_prev, ls_prev-ls
        if add or rem: yield add, rem

        ls_prev = ls
        # if ftp != None:
        #     ftp.quit()
        sleep(10)

def deployServices():
    for v in dConfig["deployment"]["services"].values():
        yield run('ecl publish --target=' + dConfig['deployment']['roxieTarget'] + '  --name=' +v['name']+ ' --main=' + v['main'] + ' -v --daliip=' + dConfig['deployment']['daliIP'] + ' -s ' + dConfig['deployment']['roxieIP'] + ' -u ' + hpcc_userID + ' -pw ' + hpcc_password + ' --allow-foreign', shell=True).returncode


print('Monitoring Landing zone: ' + dConfig['landingZone'])
for add, rem in changemon():

    addedfileNames = [s[s.rfind('/')+1:len(s)] for s in add]
    addedFilesList = [f[:-4] for f in addedfileNames]
    newFilesList = [m for m in filter(lambda f:re.match('^(\d{2})(\d{2})(\d{4})([_0-9]*)$', f) is not None, addedFilesList)]
    # print('Added files list:')
    # print('\n'.join("%s" % i for i in addedFilesList))

    # print('new files list:')
    # print('\n'.join("%s" % i for i in newFilesList))
    print('new files list count: ' + str(len(newFilesList)))
    if len(newFilesList) == 1:
        # print('\n'.join("%s" % i for i in newFilesList))
        f = newFilesList[0]
        print(f)
        sNewFile = f
        # Call Key build
        # print('Generated Workunit: ' + sWuid)
    elif(len(addedFilesList) == 1 and addedFilesList[0].find('_triggerFile') != -1):
        sNewFile = addedFilesList[0][0:addedFilesList[0].find('_triggerFile')]
        sum = 0
        for d in deployServices():
            print(sum)
            sum += d

        if sum == 0:
            # Call comparison process
            # print('Generated Workunit: ' + sWuid)

# except Exception as e:
#     submitWorkunit('QACCreditMigration_PT.modCommon(\'\').fSendEmail(\'FAILURE NOTICE\', \'Exception while running Python code\');', 'CCreditMigration: Failure Notification')
#     with open('log.txt', 'w') as f:
#         f.write(time.strftime("%Y%m%d%H%M%S", time.localtime()) + '\n' + str(e))

# sum = 0
# for d in deployServices():
#     print('Sum: ' + str(sum))
#     print('d value: ' + str(d))
#     sum += d


