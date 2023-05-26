import os, ftplib, zipfile

class Transfer():
    def __init__(self):
        # SERVER
        self.FTP_SERVER = "ftp.guiacomercialbrasil.com.br"
        # BASE DIRECTORY
        self.UP_DIR = "/public_html/uploads/" 
        # TRIAL FILE
        self.TRIALFN = "thumb_galeria_5a3aa564983b8.jpg" #"e2c8c0953ea6b992ee9d409424f32a5b.jpg"
        # INITIAL SETUP
        self._setup()

    def _connect(self):
        self.ftp = ftplib.FTP(self.FTP_SERVER)
        print("CONNECTED")

    def _login(self, username = "guiacome", password = "3hepA191Fm"):
        self._connect()
        self.ftp.login(username, password)
        print("LOGGED IN AS " + username)

    def _setup(self):
        print("STARTING SETUP")
        self._login()
        self.ftp.cwd(self.UP_DIR)
        print("SETUP COMPLETE")

    def get_remotefile(self, filename):
        print("RETRIEVING FILE: " + filename)
        file = open(filename, "wb")
        
        try:
            self.ftp.retrbinary("RETR " + self.ftp.pwd() + "/" + filename, file.write)
            file.close()
            print("RETRIEVED FILE: " + filename)
        except Exception as e:
            file.close()
            os.remove(filename)
            print("FAILED TO RETRIEVE FILE: " + filename + " - " + e)
    
    def remove_localfile(self, filename):
        os.remove(filename)
        print("REMOVED FILE: " + filename)
        

    def disconnect(self):
        self.ftp.close()
        print("CLOSED CONNECTION")
