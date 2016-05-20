# coding=utf-8

import flask

config = {
    "oauth_credentials": {
        "youdao": {
            "host": "https://note.youdao.com",
            "client_id": "d27ad4d7863fac1dc7a415e613483392",
            "client_secret": "4d0bd6cc6889f87145bc3b61c48a6505",
            "authorize_url": "https://note.youdao.com/oauth/authorize2",
            "access_token_url": "https://note.youdao.com/oauth/access2",
            "redirect_uri": "dev.maxthread.com",
            "oauth_token": ""
        }
    }
}

apis = {
    "authorize": {
        "url": config["oauth_credentials"]["youdao"]["host"] + "/oauth/authorize2",
        "params": {"client_id": config["oauth_credentials"]["youdao"]["client_id"],
                   "response_type": "code",
                   "redirect_uri": config["oauth_credentials"]["youdao"]["redirect_uri"],
                   "state": "state"
                   },
        "method": "GET"
    },
    "access_token": {
        "url": config["oauth_credentials"]["youdao"]["host"] + "/oauth/access2",
        "params": {"client_id": config["oauth_credentials"]["youdao"]["client_id"],
                   "client_secret": config["oauth_credentials"]["youdao"]["client_secret"],
                   "grant_type": "authorization_code",
                   "redirect_uri": config["oauth_credentials"]["youdao"]["redirect_uri"],
                   "state": "state",
                   "code": ""
                   },
        "method": "GET"
    },
    "get_user": {
        "url": config["oauth_credentials"]["youdao"]["host"] + "/yws/open/user/get.json",
        "params": {"client_id": config["oauth_credentials"]["youdao"]["client_id"],
                   "oauth_token": config["oauth_credentials"]["youdao"]["oauth_token"]},
        "method": "GET"
    },
    "get_notebooks": {
        "url": config["oauth_credentials"]["youdao"]["host"] + "/yws/open/notebook/all.json",
        "params": {"client_id": config["oauth_credentials"]["youdao"]["client_id"],
                   "oauth_token": config["oauth_credentials"]["youdao"]["oauth_token"]},
        "method": "POST"
    },
    "get_notes_path": {
        "url": config["oauth_credentials"]["youdao"]["host"] + "/yws/open/notebook/list.json",
        "params": {"client_id": config["oauth_credentials"]["youdao"]["client_id"],
                   "oauth_token": config["oauth_credentials"]["youdao"]["oauth_token"]},
        "method": "POST",
        "data": {"notebook": ""}
    },
    "get_note": {
        "url": config["oauth_credentials"]["youdao"]["host"] + "/yws/open/note/get.json",
        "params": {"client_id": config["oauth_credentials"]["youdao"]["client_id"],
                   "oauth_token": config["oauth_credentials"]["youdao"]["oauth_token"]},
        "method": "POST",
        "data": {"path": ""}
    },
    "get_image": {
        "url": config["oauth_credentials"]["youdao"]["host"] + "/yws/open/resource/download/",
        "params": {"client_id": config["oauth_credentials"]["youdao"]["client_id"],
                   "oauth_token": config["oauth_credentials"]["youdao"]["oauth_token"]},
        "method": "GET"
    }
}

if __name__ == '__main__':
    print config["oauth_credentials"]["youdao"]["host"]
