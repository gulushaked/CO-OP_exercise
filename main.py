from dummy_api_plugin import DummyApiPlugin


def main():
    print("Hey! We are so glad for the opportunity to help you automating your data collection from DummyJSON!")
    print("Few technical details before we are on...")
    username = input("Please enter your DummyJSON's username:").strip()
    password = input("Please enter your DummyJSON's password:").strip()
    plugin = DummyApiPlugin(username, password)
    plugin.run()
    print("Thank you for using our plugin!")


if __name__ == '__main__':
    main()