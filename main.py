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


def convert(user_session_file_path: str, output_path=None, private_ras_key_path=None):
    session_ary = parse_windterm_config(user_session_file_path)
    out = ssh_config_format(session_ary, private_ras_key_path)
    if output_path is None:
        print(out)
    else:
        with open(output_path, "w") as f:
            f.write(out)
            f.flush()


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2], sys.argv[3])

