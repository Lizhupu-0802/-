from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes

@web_routes.post('/action/plant/add')
async def action_plant_add(request):
    params = await request.post()
    param_fields = ['cou_sn', 'semester', 'week', 'class_time', 'class_position']
    param_values = {field: params.get(field) for field in param_fields}

    for field, value in param_values.items():
        if value is None:
            return web.HTTPBadRequest(text=f"{field} must be required")

    try:
        param_values['cou_sn'] = int(param_values['cou_sn'])
    except ValueError:
        return web.HTTPBadRequest(text="cou_sn invalid value")

    try:
        with db_block() as db:
            db.execute("""
            INSERT INTO plant (cou_sn, semester, week, class_time, class_position) 
            VALUES ( %(cou_sn)s, %(semester)s, %(week)s, %(class_time)s, %(class_position)s)
            """, param_values)
    except psycopg2.errors.ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此课程: {ex}")

    return web.HTTPFound(location="/plant")


@web_routes.post('/action/plant/edit/{sn}')
async def edit_plant_action(request):
    sn = request.match_info.get("sn")
    if sn is None:
        return web.HTTPBadRequest(text="sn, must be required")

    params = await request.post()
    param_fields = ['cou_sn', 'semester', 'week', 'class_time', 'class_position']
    param_values = {field: params.get(field) for field in param_fields}

    for field, value in param_values.items():
        if value is None:
            return web.HTTPBadRequest(text=f"{field} must be required")
    try:
        param_values['sn'] = int(sn)
        param_values['cou_sn'] = int(param_values['cou_sn'])
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    try:
        with db_block() as db:
            db.execute("""
            UPDATE plant SET cou_sn=%(cou_sn)s, semester=%(semester)s, week=%(week)s, class_time=%(class_time)s, class_position=%(class_position)s
            WHERE sn = %(sn)s 
            """, param_values)
    except psycopg2.errors.ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此课程计划: {ex}")
    return web.HTTPFound(location="/plant")


@web_routes.post('/action/plant/delete/{sn}')
def delete_plant_action(request):
    sn = request.match_info.get("sn")
    if sn is None:
        return web.HTTPBadRequest(text="sn must be required")

    with db_block() as db:
        db.execute("""
        DELETE FROM plant 
            WHERE sn = %(sn)s
        """, dict(sn=sn))

    return web.HTTPFound(location="/plant")
