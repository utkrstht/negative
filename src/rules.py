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

        matches = (
            (not rule_os or rule_os == sys_os)
            and
            (not rule_arch or rule_arch == sys_arch)
        )

        if matches:
            # If the rules os/arch match with ours, check if it's allowed or not
            allow = action == "allow"

    return allow