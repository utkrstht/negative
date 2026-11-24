from utils import get_operating_system, get_system_architecture

def evalute_rules(rules: list) -> bool:
    allow = False

    sys_os = get_operating_system()
    sys_arch = get_system_architecture()

    for rule in rules:
        action = rule.get('action')
        rule_info = rule.get('os')
        rule_os = None
        rule_arch = None

        if rule_info:
            rule_os = rule_info.get('name')
            rule_arch = rule_info.get('arch')

        # Allow all
        if action == "allow" and not rule_os and not rule_arch:
            allow = True

        # Allow our operating system
        if action == "allow" and rule_os == sys_os:
            allow = True

        # Allow our system architecture
        if action == "allow" and rule_arch == sys_arch:
            allow = True

        # Disallow all
        if action == "disallow" and not rule_os and not rule_arch:
            allow = False

        # Disallow our operating system
        if action == "disallow" and rule_os == sys_os:
            allow = False

        # Disallow our system architecture
        if action == "disallow" and rule_arch == sys_arch:
            allow = False

    return allow