from plugin import Plugin
import requests


class DummyApiPlugin(Plugin):

    def __init__(self, username: str, password: str, base_url='https://dummyjson.com/auth') -> None:
        self.username = username
        self.password = password
        self.base_url = base_url
        self.token = None   # To be initialized only after executing connectivity test for the first time
        self.user_id = None
        self.evidences = {}     # Where the collected evidences will be stored

    def connectivity_test(self):
        """
        In order to test the connection, we simply need to check
        whether the API has been accessed by trying to authenticate

        :return: the REST API response to an authentication
        """
        print("Performing connectivity test...")

        # URL for the DummyJSON login endpoint
        url = self.base_url + "/login"
        headers = {'Content-Type': 'application/json'}
        credentials = {
            'username': self.username,
            'password': self.password,
        }

        try:
            response = requests.post(url, headers=headers, json=credentials)
            response.raise_for_status()
            self.token = response.json().get('token')
            self.user_id = response.json().get('id')
            print("Connectivity and authentication successful.")
            return response.json()
        except requests.exceptions.HTTPError as error:
            print(f"Connectivity failed with HTTP error - {error}.")
            return None
        except requests.exceptions.ConnectionError as connection_error:
            print(f"Connectivity failed, Please check you internet connection - {connection_error}.")
            return None
        except requests.exceptions.RequestException as other_error:
            print(f"API connectivity test failed with status code {other_error}.")
            return None

    def collect(self) -> None:
        """
        collect 3 pieces of evidence from https://dummyjson.com endpoints, which simulates a REST API service
        """
        # Validating that connectivity test done
        if self.token is None:
            print("Please perform connectivity test before attempting to collect")
            return
        # Collecting evidences sequentially
        print("Attempting to collect evidences...")
        collect_methods = [self.collect_by_user_details, self.collect_posts, self.collect_posts_comments]
        datas = ['carts', 'posts', 'posts with comments']
        for method, data in zip(collect_methods, datas):
            self.evidences[data] = method()

    def collect_by_user_details(self):
        """
        Arbitrarily chosen as single evidence with the current authenticated user details,
        collecting user's carts from DummyJSON
        :return: List of the user's carts
        """
        url = self.base_url + f'/users/6/carts'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            # Successful collection
            print("User's carts evidence collected successfully")
            return response.json()['carts']
        except requests.exceptions.RequestException as error:
            # Error occurred
            print(f"Collection failed with - {error}.")
            return None

    def collect_posts(self, posts=60):
        """
        Collect a single evidence with a list of posts in the system.
        :param posts: The amount of posts to be collected
        :return: List of posts
        """
        url = self.base_url + f"/posts?limit={posts}"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            print("Posts evidence collected successfully")
            return response.json()['posts']  # Return the list of posts

        except requests.exceptions.RequestException as error:
            # Error occurred
            print(f"Collection failed with - {error}.")
            return None

    def collect_posts_comments(self, posts=60):
        """
        Collect a single evidence with a list of 60 posts, including each post’s comments
        :return: List of posts, including each post's comments
        """
        posts_with_comments = self.collect_posts(posts)
        if posts_with_comments is not None:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'}
            for post in posts_with_comments:
                url = self.base_url + f"/comments/post/{post['id']}"
                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    post['comments'] = response.json()['comments']
                except requests.exceptions.RequestException as error:
                    print(f"Collection failed with  - {error}.")
                    return None

            print("Comments collected successfully and were added to the posts just collected")
            return posts_with_comments

        else:
            return None

    def view_plugins_evidences(self):
        """
        Method for visualizing the evidences collected by this plugin
        """
        for data_type, evidence in self.evidences.items():
            print(f"{data_type} collected -->")
            for item in evidence:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key} : {value}")
                    print("--------------------------------------")
                else:
                    for item in evidence:
                        print(f" - {item}")
            print("=====================================================")

    def run(self):
        """
        Calling this method will run the plugin
        :return:
        """
        super().run()
        if self.token is not None:
            ans = input("Would you like to review the evidences collected? YES|NO").strip()
            if ans == 'YES':
                self.view_plugins_evidences()







