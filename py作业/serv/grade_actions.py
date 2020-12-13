from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes

@web_routes.post('/action/grade/add')
async def action_grade_add(request):
    params = await request.post()
    stu_sn = params.get("stu_sn")
    pla_sn = params.get("pla_sn")
    grade = params.get("grade")

    if stu_sn is None or pla_sn is None or grade is None:
        return web.HTTPBadRequest(text="stu_sn, pla_sn, grade must be required")

    try:
        stu_sn = int(stu_sn)
        pla_sn = int(pla_sn)
        grade = float(grade)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    try:
        with db_block() as db:
            db.execute("""
            INSERT INTO plant_grade (stu_sn, pla_sn, grade) 
            VALUES ( %(stu_sn)s, %(pla_sn)s, %(grade)s)
            """, dict(stu_sn=stu_sn, pla_sn=pla_sn, grade=grade))
    except psycopg2.errors.UniqueViolation:
        query = urlencode({
            "message": "已经添加该学生的课程成绩",
            "return": "/grade"
        })
        return web.HTTPFound(location=f"/error?{query}")
    except psycopg2.errors.ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此学生或课程: {ex}")

    return web.HTTPFound(location="/grade")


@web_routes.post('/action/grade/edit/{stu_sn}/{pla_sn}')
async def edit_grade_action(request):
    stu_sn = request.match_info.get("stu_sn")
    pla_sn = request.match_info.get("pla_sn")
    if stu_sn is None or pla_sn is None:
        return web.HTTPBadRequest(text="stu_sn, pla_sn, must be required")

    params = await request.post()
    grade = params.get("grade")

    try:
        stu_sn = int(stu_sn)
        pla_sn = int(pla_sn)
        grade = float(grade)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    with db_block() as db:
        db.execute("""
        UPDATE plant_grade SET grade=%(grade)s
        WHERE stu_sn = %(stu_sn)s AND pla_sn = %(pla_sn)s
        """, dict(stu_sn=stu_sn, pla_sn=pla_sn, grade=grade))

    return web.HTTPFound(location="/grade")


@web_routes.post('/action/grade/delete/{stu_sn}/{pla_sn}')
def delete_grade_action(request):
    stu_sn = request.match_info.get("stu_sn")
    pla_sn = request.match_info.get("pla_sn")
    if stu_sn is None or pla_sn is None:
        return web.HTTPBadRequest(text="stu_sn, pla_sn, must be required")

    with db_block() as db:
        db.execute("""
        DELETE FROM plant_grade
            WHERE stu_sn = %(stu_sn)s AND pla_sn = %(pla_sn)s
        """, dict(stu_sn=stu_sn, pla_sn=pla_sn))

    return web.HTTPFound(location="/grade")
