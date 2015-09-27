from server import PrintServer

def main():
    print_server = PrintServer()
    print_server.load_users('valid_users.txt')
    print_server.run()

if __name__ == '__main__':
    main()