# Connection to Wi-Fi network
STA_SSID = "rosebud"
STA_PSWD = "87654321"
CONNECT_TRIES = 5     # number of attempts to connect to Wi-Fi
CONNECT_TIMEOUT = 20  # seconds to wait for a connection

# Set STA_FIXED_IP to "0.0.0.0" for dynamic IP
STA_FIXED_IP = "192.168.1.59"
STA_SUBNET = "255.255.255.0"
STA_GATEWAY = "192.168.1.1"
STA_DNS = "192.168.1.1"

# Access point parameters if connection as station not possible
AP_UP_TIME = 600      # leaving AP on for 10 minutes line before reset
AP_SSID = "w600AP"    # access point name
AP_PSWD = None        # access point password

# FTP server created in station or access point mode
FTP_PORT = 21         # ftp port 21 is default
FTP_USER = "user"     # ftp user name
FTP_PSWD = "12345678" # ftp password



