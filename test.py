from dummy_api_plugin import DummyApiPlugin


def check_test_connectivity():
    # valid username & password
    plugin = DummyApiPlugin('emilys', 'emilyspass')
    res = plugin.connectivity_test()
    expected = 1
    if res['id'] == 1:
        print("Pass")
    else:
        print("Failed")

    #invalid username & password
    plugin = DummyApiPlugin('gal', 'shaked')
    res = plugin.connectivity_test()
    expected = None

    if res == expected:
        print("Pass")
    else:
        print("Failed")
    return

if __name__ == '__main__':
    check_test_connectivity()
