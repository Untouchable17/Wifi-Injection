import subprocess
from typing import Union, List


class WifiInject:

    @classmethod
    def send_system_command(cls) -> Union[str, List[str]]:
        """ Sending command to get SSID list """
        
        try:
            sys_process = subprocess.check_output(
                ["netsh", "wlan", "show", "profiles"]
            ).decode("UTF-8", errors="backslashreplace").split('\n')
        except subprocess.CalledProcessError:
            return f"Wireless AutoConfig Service (wlansvc) is not running"

        return sys_process

    @classmethod
    def parse_system_data(cls) -> List[str]:
        """ Parses the result and returns everything in an array """

        profiles = [
            data.split(":")[1][1:-1]
            for data in cls.send_system_command()
            if "All User Profile" in data
        ]

        return profiles

    @classmethod
    def show_result(cls) -> str:
        """ Prints the result to the console """

        for data in cls.parse_system_data():
            try:
                results = subprocess.check_output(
                    ["netsh", "wlan", "show", "profile", data, "key=clear"]
                ).decode("UTF-8", errors="backslashreplace").split('\n')
                results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                try:
                    return "{:<30}|  {:<}".format(data, results[0])
                except IndexError:
                    return "{:<30}|  {:<}".format(data, "")
            except subprocess.CalledProcessError:
                return "{:<30}|  {:<}".format(data, "ENCODING ERROR")


def main():
    wifi = WifiInject()
    print(wifi.show_result())


if __name__ == "__main__":
    main()
