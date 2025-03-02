# Copyright: Marcus Adair, Ivan Rodero, University of Utah, SCI Institute
#   October, 2022
#
#
# This files SSH's into OSG and runs the script there to get time throughput after
# a DAGMan FakeQuakes run is complete. It then retrieves a txt file with the throughput and brings
# it back to the current directory.
#
# To run this just import ssh_getThroughputPost and call ssh_getThroughputPost.main()
# with the name of a directory that you want to check as an argument in main()
#
#   Or use the command line (in an environment with paramiko) and send in the dirname you want to get stats from: 'python ssh_getThroughputPost dirname'

import paramiko
import sys

def main(arg1):

    dirname=str(arg1)

    # SSH into OSG
    host = "login05.osgconnect.net"
    username = "marcus_adair"
    password = "12345"
    ssh_client = paramiko.client.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, username=username, password=password)

    # Call the script to get time stats on the running FakeQuakes
    cmmd = "sh getThroughputPost_v2_4_to_txt.sh " + dirname
    stdin, stdout, stderr = ssh_client.exec_command(cmmd)

    # Decode the output and any errors
    #print(f'STDOUT: {stdout.read().decode("utf8")}')

    output = f'{stdout.read().decode("utf8")}'
    #print(output)
    file_to_trans = output.replace('The output was writen to ','')

    # remove new line
    file_to_trans = file_to_trans.replace('\n', '')
    print('Transferring the file: ' + file_to_trans)

    # open  a client to transfer the output txt file to the local machine
    sftp_client=ssh_client.open_sftp()

    # set up the paths
    remotepath = '/home/marcus_adair/' + file_to_trans
    localpath = './' + file_to_trans

    # do the transfer
    sftp_client.get(remotepath, localpath)
    sftp_client.close()


    # close the file objects
    stdin.close()
    stdout.close()
    stderr.close()

    # close the connection
    ssh_client.close()

if __name__== "__main__":
    main(sys.argv[1])
