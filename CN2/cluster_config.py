LOCAL_NODE = "CN2"

NODES = {
    "CN1": "http://26.41.51.255:8000/sql",
    "CN2": "http://26.201.116.10:8000/sql",
    "CN3": "http://26.105.5.3:8000/sql",
}

BRANCH_BY_NODE = {
    "CN1": 1,
    "CN2": 2,
    "CN3": 3,
}

NODE_BY_BRANCH = {
    1: "CN1",
    2: "CN2",
    3: "CN3",
}

NEXT_NODE = {
    "CN1": "CN2",
    "CN2": "CN3",
    "CN3": "CN1",
}

USER = "root"
PASSWORD = "root"
NAMESPACE = "ddbs"
DATABASE = "plant_paradise"

LOCAL_ENDPOINT = "http://127.0.0.1:8000/sql"
