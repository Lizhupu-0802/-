from aiohttp import web
from .config import db_block, web_routes, render_html


@web_routes.get("/course")
async def view_list_course(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS cou_sn, no as cou_no, name as cou_name, score as cou_score, attr as cou_attr 
        FROM course ORDER BY name
        """)
        items = list(db)
    return render_html(request, 'course_list.html', items=items)


@web_routes.get('/course/edit/{sn}')
def view_course_editor(request):
    sn = request.match_info.get("sn")
    if sn is None:
        return web.HTTPBadRequest(text="sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT sn AS cou_sn, no as cou_no, name as cou_name, score as cou_score, attr as cou_attr 
        FROM course WHERE sn= %(sn)s ;
        """, dict(sn=sn))

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such course: sn={sn}")

    return render_html(request, "course_edit.html",
                       record=record)


@web_routes.get("/course/delete/{sn}")
def course_deletion_dialog(request):
    sn = request.match_info.get("sn")
    if sn is None:
        return web.HTTPBadRequest(text="sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT  sn, no, name
        FROM course
        WHERE sn = %(sn)s;
        """, dict(sn=sn))

        record = db.fetch_first()
    if record is None:
        return web.HTTPNotFound(text=f"no such course: sn={sn}")

    return render_html(request, 'course_dialog_deletion.html', record=record)
