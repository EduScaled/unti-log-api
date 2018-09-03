
from db import insert, all

async def fetch_logs(pool, query):
    logs = []
    for log in await all(pool, query):
        logs.append({
            'id': log[0],
            'user_id': log[1],
            'email': log[2],
            'type': log[3],
            'action': log[4],
            'url': log[5],
            'created_at': str(log[6])
        })
    return logs

async def insert_log(pool, log):
    query = "INSERT INTO log_data VALUES (NULL, {}, \"{}\", \"{}\", \"{}\", \"{}\", NOW());".format(
        log['user_id'], 
        log['email'],
        log['type'],
        log['action'],
        log['url'],
    )
    await insert(pool, query)

async def get_logs(pool, params):
    query_params = []
    if params.get("type", None):
        query_params.append("type = \"{}\"".format(params.get("type")))
    if params.get("user_id", None):
        query_params.append("user_id = {}".format(params.get("user_id")))
    if params.get("email", None):
        query_params.append("email = \"{}\"".format(params.get("email")))
    if params.get("date_gt", None):
        query_params.append("created_at >= \"{}\"".format(params.get("date_gt")))
    if params.get("date_lt", None):
        query_params.append("created_at <= \"{}\"".format(params.get("date_lt")))
    if params.get("action", None):
        query_params.append("LOWER(action) like \"%{}%\"".format(params.get("action")))

    query_template = "SELECT id, user_id, email, type, action, url, created_at FROM log_data"
    if query_params:
        query = "".join([query_template, " WHERE ", " AND ".join(query_params), ";"])
    else:
        query = "".join([query_template, ";"])

    return await fetch_logs(pool, query)