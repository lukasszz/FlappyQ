# setup stuff

from paramiko import SSHClient
from scp import SCPClient

def ssh_scp_files(ssh_host, ssh_user, ssh_password, source_volume, destination_volume):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(ssh_host, username=ssh_user, password=ssh_password, look_for_keys=False)

    with SCPClient(ssh.get_transport()) as scp:
        scp.put(source_volume, recursive=True, remote_path=destination_volume)
    






# run the following whenever you want to trigger a rainbow
    
text_file = open("wipe.txt", "w")
text_file.write('0')
text_file.close()

text_file = open("pw.txt") # you'll need this file locally that contains the password
pw = text_file.read()
text_file.close()

ssh_scp_files('chandelier.local', 'pi', pw, 'wipe.txt', '/home/pi/quantilier2/')
