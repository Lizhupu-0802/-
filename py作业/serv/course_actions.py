from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes

@web_routes.post('/action/course/add')
async def action_course_add(request):
    params = await request.post()
    param_fields = ['no', 'name', 'score', 'attr', ]
    param_values = {field: params.get(field) for field in param_fields}

    for field, value in param_values.items():
        if value is None:
            return web.HTTPBadRequest(text=f"{field} must be required")

    try:
        with db_block() as db:
            db.execute("""
            INSERT INTO course (no, name, score, attr) 
            VALUES ( %(no)s, %(name)s, %(score)s, %(attr)s)
            """, param_values)
    except psycopg2.errors.UniqueViolation:
        query = urlencode({
            "message": "已经添加该课程号课程",
            "return": "/course"
        })
        return web.HTTPFound(location=f"/error?{query}")

    return web.HTTPFound(location="/course")


@web_routes.post('/action/course/edit/{sn}')
async def edit_course_action(request):
    sn = request.match_info.get("sn")
    if sn is None:
        return web.HTTPBadRequest(text="sn, must be required")

    params = await request.post()
    param_fields = ['no', 'name', 'score', 'attr', ]
    param_values = {field: params.get(field) for field in param_fields}

    for field, value in param_values.items():
        if value is None:
            return web.HTTPBadRequest(text=f"{field} must be required")
    try:
        param_values['sn'] = int(sn)
        param_values['score'] = int(param_values['score'])
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    with db_block() as db:
        db.execute("""
        UPDATE course SET no=%(no)s, name=%(name)s, score=%(score)s, attr=%(attr)s
        WHERE sn = %(sn)s 
        """, param_values)
    return web.HTTPFound(location="/course")


@web_routes.post('/action/course/delete/{sn}')
def delete_course_action(request):
    sn = request.match_info.get("sn")
    if sn is None:
        return web.HTTPBadRequest(text="sn must be required")

    with db_block() as db:
        db.execute("""
        DELETE FROM course 
            WHERE sn = %(sn)s
        """, dict(sn=sn))

    return web.HTTPFound(location="/course")
