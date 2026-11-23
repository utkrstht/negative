from typing import List
from utils import get_operating_system, get_system_architecture

def parse_jvm_arguments(data: dict) -> List:
    args = data['arguments']['jvm']

    parsed_args = []

    for arg in args:
        if isinstance(arg, str):
            parsed_args.append(arg)
            continue

        # TODO: i need to actually process these rules properly holy fucking shit
        if arg.get("rules"):
            action = arg["rules"][0]["action"]
            os = arg["rules"][0].get("os").get("name")

            # help i dont know what im doing
            if not os:
                os = arg["rules"][0].get("os").get("arch")
                if os == "x86" or not os == get_system_architecture():
                    continue

            # If the argument isn't meant for our operating system, skip it
            if not os == get_operating_system() and action == "allow" or os == get_operating_system() and action == "disallow":
                continue

            parsed_args.append(arg['value'])
            continue

    return parsed_args