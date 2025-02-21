from fastapi import HTTPException

import mchat.data.group as d_group
import mchat.data.user_group as d_user_group
from mchat.helper import db_connect
from mchat.model import GroupIn, SuccessHandler, User, UserGroupIn


@db_connect
def add_group(curs, user: User, in_group: GroupIn):
    db_group = d_group.get_by_owner_and_name(curs, user.id, in_group.name)
    if db_group:
        raise HTTPException(status_code=400, detail="group already exists")
    db_group = d_group.add(curs, user.id, in_group.name)
    user_group = UserGroupIn(user_id=user.id, group_id=db_group["id"], role=2)
    return SuccessHandler(detail="group created successfully", data=db_group)


@db_connect
def add_user_group(curs, user: User, in_user_group: UserGroupIn):
    db_group = d_group.get(curs, in_user_group.group_id)
    if not db_group:
        raise HTTPException(status_code=400, detail="group does not exists")
    db_user_group = d_user_group.get_by_group_and_user(
        curs, db_group.id, in_user_group.user_id
    )
    if db_user_group:
        raise HTTPException(status_code=400, detail="user in group already exists")
    if db_group.owner_id != user.id:
        db_current_user_group = d_user_group.get_by_group_and_user(
            curs, db_group.id, user.id
        )
        if db_current_user_group["role"] == 0:
            raise HTTPException(status_code=403, detail="unauthorized access")
    d_user_group.add(curs, in_user_group)
    return SuccessHandler(detail="user in group add successfully")


# @db_connect
# def get_all(curs, user: User):
# return d_chat.get_all_by_user_id(curs, user.id)
# pass
