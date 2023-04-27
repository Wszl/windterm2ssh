import json
import os
import sys


def parse_windterm_config(user_session_file_path: str):
    if not os.path.exists(user_session_file_path):
        raise RuntimeError("user.sessions file not found in path.{}"
                           .format(user_session_file_path))
    ssh_conf_ary = []
    with open(user_session_file_path, "r") as f:
        us_json = json.load(f)
        for item in us_json:
            ssh_conf = {}
            ssh_conf['wt_group'] = item.get("session.group")
            ssh_conf['wt_label'] = item.get("session.label")
            ssh_conf['wt_port'] = item.get("session.port")
            ssh_conf['wt_target'] = item.get("session.target")
            ssh_conf['wt_protocol'] = item.get("session.protocol")
            ssh_conf_ary.append(ssh_conf)
    return ssh_conf_ary


def ssh_config_format(ssh_conf_list: list, private_ras_key_path=None):
    out = ""
    for i in ssh_conf_list:
        out += f"Host\t{i['wt_group']}#{i['wt_label']}\n"
        out += f"\tHostname  \t{i['wt_target']}\n"
        if i.get('user') is not None:
            out += f"\tUser\t{i['wt_user']}\n"
        else:
            out += "\tUser\troot\n"
        if private_ras_key_path is not None:
            out += f"\tIdentityFile\t{private_ras_key_path}\n"
        out += "\n"

    return out


"""
nextterminal csv example format:
name,ssh,127.0.0.1,22,username,password,privateKey,passphrase,description,tag1|tag2|tag3
"""
def nexttermial_ssh_config_format(data: list):
    if data is None:
        raise Exception("covert data must be required.")
    out = ""
    for i in data:
        info_ary = []
        name = i['wt_group']+"-"+i['wt_label']
        info_ary.append(name)
        protocol = i['wt_protocol']
        info_ary.append(protocol.lower())
        host = i.get("wt_target")
        info_ary.append(host)
        port = i.get("wt_port")
        if port is not None:
            info_ary.append(str(port))
        else:
            info_ary.append("22")
        user = i.get("user")
        if user is not None:
            info_ary.append(user)
        else:
            info_ary.append("root")
        pwd = ""
        info_ary.append(pwd)
        private_key = ""
        info_ary.append(private_key)
        passphrase = ""
        info_ary.append(passphrase)
        desc = ""
        info_ary.append(desc)
        tag1 = i['wt_group']
        info_ary.append(tag1)
        tag2 = i['wt_label']
        info_ary.append(tag2)
        tag3 = ""
        info_ary.append(tag3)
        out += ",".join(info_ary)
        out += "\n"
    return out


def convert(user_session_file_path: str, type="ssh", output_path=None, private_ras_key_path=None):
    session_ary = parse_windterm_config(user_session_file_path)
    if type == "ssh":
        out = ssh_config_format(session_ary, private_ras_key_path)
    elif type == "nextterminal":
        out = nexttermial_ssh_config_format(session_ary)
    else:
        raise Exception("not supported type " + type)
    if output_path is None:
        print(out)
    else:
        with open(output_path, "w") as f:
            f.write(out)
            f.flush()


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

