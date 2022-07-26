import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

# Must match the paths defined in `update.sh` and `delete.sh`
TEMP_DIR = os.path.join(PROJECT_ROOT, 'tmp')
UFW_STATUS_FILE = os.path.join(TEMP_DIR, 'ufw-status.txt')
CLOUDFLARE_IPS_FILE = os.path.join(TEMP_DIR, 'cloudflare-ips.txt')
UPDATE_UFW_RULES_SCRIPT = os.path.join(TEMP_DIR, 'update_ufw_rules.sh')
DELETE_UFW_RULES_SCRIPT = os.path.join(TEMP_DIR, 'delete_ufw_rules.sh')

# Allowed actions
ACTION_UPDATE = 'update'
ACTION_DELETE = 'delete'

# Comments used to recognize which ufw rules are automatically generated
RAW_COMMENT = 'cloudflare'  # comment to used for setting ufw with `ufw allow`
UFW_COMMENT = '# ' + RAW_COMMENT  # comment section in `ufw status` lines (e.g. "# cloudflare")

# Script templates
UFW_BIN = 'ufw'
UFW_ALLOW_RULE_TEMPLATE = 'allow from {subnet} to any port 80,443 proto tcp'
UFW_ADD_RULE_TEMPLATE = 'echo "Adding IP subnet {subnet}..."\n' \
                        + UFW_BIN + ' ' + UFW_ALLOW_RULE_TEMPLATE + ' comment "{comment}"'
UFW_DELETE_RULE_TEMPLATE = 'echo "Deleting IP subnet {subnet}..."\n' \
                           + UFW_BIN + ' delete ' + UFW_ALLOW_RULE_TEMPLATE


def get_existing_cloudflare_ip_subnets_from_ufw_rules():
    with open(UFW_STATUS_FILE, 'r') as file:
        lines = file.read().splitlines()
        subnets = []
    for line in lines:
        if UFW_COMMENT not in line:
            continue
        segments = line.split()
        # In the current implementation of `ufw status`, the 3rd column of the results is the
        # subnets; this might be subject to change in future versions of ufw.
        subnets.append(segments[2])
    return subnets


def get_latest_cloudflare_ip_subnets():
    with open(CLOUDFLARE_IPS_FILE, 'r') as file:
        return file.read().splitlines()


def compute_subnets_to_delete(existing, new):
    new_set = set(new)
    to_delete = []
    for subnet in existing:
        if subnet not in new_set:
            to_delete.append(subnet)
    return to_delete


def compute_subnets_to_add(existing, new):
    existing_set = set(existing)
    to_add = []
    for subnet in new:
        if subnet not in existing_set:
            to_add.append(subnet)
    return to_add


def generate_delete_commands(subnets_to_delete):
    commands = []
    for subnet in subnets_to_delete:
        commands.append(UFW_DELETE_RULE_TEMPLATE.format(subnet=subnet))
    return commands


def generate_add_commands(subnets_to_add):
    commands = []
    for subnet in subnets_to_add:
        commands.append(UFW_ADD_RULE_TEMPLATE.format(subnet=subnet, comment=RAW_COMMENT))
    return commands


def write_commands_to_file(path, commands):
    with open(path, 'w+') as file:
        file.write('\n'.join(commands))
        file.write('\n')


def generate_update_script():
    existing_subnets = get_existing_cloudflare_ip_subnets_from_ufw_rules()
    new_subnets = get_latest_cloudflare_ip_subnets()
    to_delete = compute_subnets_to_delete(existing_subnets, new_subnets)
    to_add = compute_subnets_to_add(existing_subnets, new_subnets)
    commands = []
    commands.extend(generate_delete_commands(to_delete))
    commands.extend(generate_add_commands(to_add))
    write_commands_to_file(UPDATE_UFW_RULES_SCRIPT, commands)


def generate_delete_script():
    existing_subnets = get_existing_cloudflare_ip_subnets_from_ufw_rules()
    commands = generate_delete_commands(existing_subnets)
    write_commands_to_file(DELETE_UFW_RULES_SCRIPT, commands)


def main(action):
    """
    Generate the bash script for the specified action.
    :param action: Can be either `ACTION_UPDATE` or `ACTION_DELETE`
    """
    if action == ACTION_UPDATE:
        generate_update_script()
    elif action == ACTION_DELETE:
        generate_delete_script()
    else:
        raise ValueError('Unrecognized action: ' + action)


if __name__ == '__main__':
    main(sys.argv[1])
