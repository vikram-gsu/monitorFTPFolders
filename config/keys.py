import os
# print(__file__)
# print(os.path.dirname(__file__))
# print(os.path.abspath(os.path.join(os.path.dirname(__file__))))
# print(os.path.join(os.path.dirname(__file__), __file__))

def getConfig():
    return {
        'serverIP': '', #FTP server
        'landingZone': '', #FTP folder location
        'credentials': {
            'hpcc':{
                'userID': '',
                'password': ''
            },
            'ftp':{
                'userID': '',
                'password': ''
            }
        }
    }