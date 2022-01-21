from typing import Dict
import requests

API_ROOT_PATH = "https://www.bungie.net/Platform"


class BungieApi:
    __HEADERS: Dict[str, str]

    def __init__(self, api_key: str):
        self.__HEADERS = {"X-API-Key": api_key}
        pass

    def getProfile(self, membershipType, destinyMembershipId, components=[200]):
        params = {}
        if components is not None: params["components"] = components

        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Profile/{destinyMembershipId}', headers=self.__HEADERS, params=params)

        return (api_call.json())['Response']

    def getAccountStats(self, membershipType, destinyMembershipId):
        params = {}

        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Account/{destinyMembershipId}/Stats', headers=self.__HEADERS, params=params)

        return (api_call.json())['Response']

    def getActivities(self, membershipType, destinyMembershipId, characterId, page=0, count=250, mode=None):
        params = {}
        if page is not None: params["page"] = page
        if count is not None: params["count"] = count
        if mode is not None: params["mode"] = mode

        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/', headers=self.__HEADERS, params=params)
        json_ = (api_call.json())
        if ("Response" not in json_):
            print(json_)
        return json_['Response']

    def getPGCR(self, activityId):
        params = {}

        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/Stats/PostGameCarnageReport/{activityId}/', headers=self.__HEADERS, params=params)
        return (api_call.json())['Response']

    def getItem(self, itemReferenceId):
        pass

    def login(username, password, api_key):
        ################################################
        BUNGIE_SIGNIN_URI = "https://www.bungie.net/en/User/SignIn/Steam"
        PSN_OAUTH_URI = "https://auth.api.sonyentertainmentnetwork.com/login.do"

        request1 = requests.get(BUNGIE_SIGNIN_URI, allow_redirects=True)
        jsessionid0 = request1.history[1].cookies["JSESSIONID"]
        params = urlparse(request1.url).query
        params64 = b64encode(params)
        # Post credentials and pass the JSESSIONID cookie.
        # We get a new JSESSIONID cookie.
        # Note: It doesn't appear to matter what the value of `params` is, but
        # we'll pass in the appropriate value just to be safe.
        post = requests.post(
            PSN_OAUTH_URI,
            data={"j_username": username, "j_password": password, "params": params64},
            cookies={"JSESSIONID": jsessionid0},
            params={"redirect_uri": BUNGIE_SIGNIN_URI},
            allow_redirects=False
        )

        if "authentication_error" in post.headers["location"]:
            print("Invalid credentials")

        jsessionid1 = post.cookies["JSESSIONID"]

        session = requests.Session()

        # Follow the redirect from the previous request passing in the new
        # JSESSIONID cookie. This gets us the Bungie cookies.
        session.get(
            post.headers["location"],
            allow_redirects=True,
            cookies={"JSESSIONID": jsessionid1}
        )

        # Add the API key to the current session
        session.headers["X-API-Key"] = api_key
        session.headers["x-csrf"] = session.cookies["bungled"]

        ####################################################################################

        return session