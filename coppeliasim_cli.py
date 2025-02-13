import argparse
import ipaddress
from tqdm import tqdm
import time
from colorama import Fore, init
import requests
import json


def aesthetic():
    print(Fore.WHITE + """

                                ____                       _ _       ____  _           
                                / ___|___  _ __  _ __   ___| (_) __ _/ ___|(_)_ __ ___  
                                | |   / _ \| '_ \| '_ \ / _ \ | |/ _` \___ \| | '_ ` _ \ 
                                | |__| (_) | |_) | |_) |  __/ | | (_| |___) | | | | | | |
                                \____\___/| .__/| .__/ \___|_|_|\__,_|____/|_|_| |_| |_|
                                        |_|   |_|                                     

                                """)
    print(Fore.RED + 'Connecting to robot')
    init(autoreset=True)
    for _ in tqdm(range(100)):
        time.sleep(0.01)
    print(Fore.GREEN + 'Success: Robot is active')


def ipcheck(ip_address):
    url = f"http://{ip_address}:{ip_port}/verify"  # Example API
    response = requests.get(url)
    print(response.status_code)
    try:
        res=response.json()
        
        if(res["message"]=="InteractiveRobotics"):
            print("Connected to robot")
        else:
            print("1 Invalid IP address! Please enter a valid IP address.")
            ipget()
    except Exception as e:
        print(e)
        print("Invalid IP address! Please enter a valid IP address.")
        ipget()


def ipget():
    global ip_address
    global ip_port
    ip_address = input("Enter the IP address of the robot: ").strip()
    ip_port=input("Enter the port: ").strip()
    ipcheck(ip_address)

def jsonconverter(args):
    return json.dumps(vars(args))


def send_request(endpoint, args):
    try:
        """Send a POST request to the given endpoint with JSON data."""
        url = f"http://{ip_address}:{ip_port}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        data=jsonconverter(args)
        response = requests.post(url, data , headers=headers)
        print(f"Response: {response.status_code}")
        print(jsonconverter(args))
        print(data)
        print(url)
        print(response)
        print(type(data))
    except Exception as e:
        print(e)





def pickup(args):
    print(f"Picking up {args.object} at {args.coordinate}...")
    send_request("pickup", args)


def drop(args):
    print("Dropping the object...")
    send_request("drop", args)


def stack(args):
    print("Stacking the object...")
    send_request("stack", args)


def move(args):
    print(args)
    print(f"Moving {args.direction} with step size {args.magnitude}...")
    send_request("move", args)


def revolute(args,joint):
    print(f"Rotating {args.joint} by {args.degree} degrees...")
    send_request(joint , args)

def moveline(args):
    print(f"Moving {args.moveline}...")
    send_request("movebypath", args)

def multistack(args):
    print("Stacking the object...")
    send_request("stacktheobjects", args)


def main():
    try:
        global ip_address
        parser = argparse.ArgumentParser(description="CLI for CoppeliaSim Robot Control",exit_on_error=False)

        # Subcommands
        subparsers = parser.add_subparsers(dest="cmd")

        # Pick
        parser_pick = subparsers.add_parser("pick", help="Pick an object",exit_on_error=False)
        parser_pick.add_argument("-o", "--object", choices=["Cuboid", "Cylinder", "Prism"], required=True, help="Object to pick")
        parser_pick.add_argument("-coord", "--coordinate", nargs=3, type=float, required=False, help="Pick-up coordinates")

        # Drop
        parser_drop = subparsers.add_parser("drop", help="Drop an object",exit_on_error=False)

        # Stack
        parser_stack = subparsers.add_parser("stack", help="Stack an object",exit_on_error=False)
        parser_stack.add_argument("-o", "--object", choices=["Cuboid", "Cylinder", "Prism"], required=True, help="Object to stack")

        # Move
        parser_move = subparsers.add_parser("move", help="Move the robot",exit_on_error=False)
        parser_move.add_argument("-m", "--direction",type=str, choices=["F", "B", "R", "L"], required=True, help="Direction in which the bot will move")
        parser_move.add_argument("-mag", "--magnitude", type=float, required=True, help="Step size")

        # Revolute
        parser_joint = subparsers.add_parser("revolute", help="Rotate a joint",exit_on_error=False)
        parser_joint.add_argument("-j", "--joint", choices=[f"joint{i}" for i in range(1, 7)], required=True, help="Joint to rotate")
        parser_joint.add_argument("-deg", "--degree", type=float, required=True, help="Rotation angle")

        #linemovment
        parser_line = subparsers.add_parser("path", help="Move the robot in a diffrerent curve",exit_on_error=False)
        parser_line.add_argument("-ml", "--moveline", choices=["circle","square","heart","hexagon"], required=True, help="Direction")

        parser_multistack = subparsers.add_parser("multistack", help="Stack multiple objects , Enter multiple object to stack at once",exit_on_error=False)
        parser_multistack.add_argument("-o", "--objects", nargs='+', choices=["Cuboid", "Cylinder", "Prism"], required=True, help="Object to stack")



    except Exception as e:
            print(e)
    while True:
        try:
            # Get user input and parse
            user_input = input("\n>>>").strip().split()
            if not user_input:
                continue
            if user_input[0].lower() == "exit":
                print("Exiting...","robot is going back to sleep....zzzzz")
                break

            args = parser.parse_args(user_input)



            # Call corresponding function
            if args.cmd == "pick":
                pickup(args)
            elif args.cmd == "drop":
                drop(args)
            elif args.cmd == "stack":
                stack(args)
            elif args.cmd == "move":
                move(args)
            elif args.cmd == "revolute":
                revolute(args,args.joint)
            elif args.cmd=="line":
                moveline(args)
            elif args.cmd=="multistack":
                multistack(args)

            else:
                print("Invalid command! Type '-h' for help.")
            

        except Exception as e:
            print(e)
            # Prevent argparse from exiting the loop
            continue


# Run the setup
aesthetic()
ipget()


# Start the interactive loop
if __name__ == "__main__":
    main()
