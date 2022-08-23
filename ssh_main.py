from datetime import datetime
import string
import secrets

import paramiko

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(secrets.choice(chars) for _ in range(size))

def call_api(*args):
    username = "user"
    password = "Ab123456"
    hostname = "172.31.5.109"
    port = 22

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username, password)

        time_now = datetime.now()
        date_time = time_now.strftime("%Y%m%d%H%M%S")
        random_id = id_generator()

        session_name = f"storageIDConverterSession_{date_time}_{random_id}"
        storageIDs = ""
        for id in args:
            if isinstance(id, int):
                storageIDs += f"{str(id)} "
            elif isinstance(id, str):
                if id.isdecimal():
                    storageIDs += f"{id} "
                else:
                    print(f"id {id} is not a valid str format storageID, skip.")
                    continue
            elif isinstance(id, list):
                for subID in id:
                    if isinstance(subID, int):
                        storageIDs += f"{str(subID)} "
                    elif isinstance(subID, str):
                        if subID.isdecimal():
                            storageIDs += f"{subID} "
                        else:
                            print(f"id {subID} is not a valid str format storageID, skip.")
                            continue
            else:
                print(f"id {id} is not in str/int/list format, skip.")
                continue

        stdin, stdout, stderr = client.exec_command(f"tmux new -d -s {session_name}; \
                                                    tmux send-keys -t {session_name}.0 'echo 'Hello World''                                  ENTER; \
                                                    tmux send-keys -t {session_name}.0 'cd AIC/datatool/20210924_DicomPrimaryProcessing/'    ENTER; \
                                                    tmux send-keys -t {session_name}.0 'source ~/miniconda3/etc/profile.d/conda.sh'          ENTER; \
                                                    tmux send-keys -t {session_name}.0 'conda activate chiang'                               ENTER; \
                                                    tmux send-keys -t {session_name}.0 'python studyListPacker_main.py {storageIDs}'         ENTER; \
                                                    tmux send-keys -t {session_name}.0 'conda deactivate'                                    ENTER; \
                                                    tmux send-keys -t {session_name}.0 'exit'                                                ENTER")
        # print("stdout readlines:")
        # result = stdout.readlines()
        # for row in result:
        #     print(row, end="")
        # print("")

        # print("stderr readlines:")
        # result = stderr.readlines()
        # for row in result:
        #     print(row, end="")
        # print("")

        stdin.close()   
        client.close()

    except Exception:
        print ('Exception!!')
        raise

if __name__ == '__main__':
    call_api(29891, '1564', [1, 2, '456'])