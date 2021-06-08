def del_user(user_info):
    del_user = {
        "operation": "del",
        "user_info": user_info
    }
    return del_user


def add_user(user_info):
    add_user = {
        "operation": "add",
        "user_info": user_info
    }
    return add_user


def protocol_broadcast(msg, person):
    msg = {
        "operation": "broadcast",
        "from": person,
        "msg": msg
    }
    return msg
