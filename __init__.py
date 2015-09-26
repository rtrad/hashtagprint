import config
from server import PrintServer

def main():
    print_server = PrintServer()
    print_server.run()

if __name__ == '__main__':
    main()