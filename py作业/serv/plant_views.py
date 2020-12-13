from aiohttp import web
from .config import db_block, web_routes, render_html


@web_routes.get("/plant")
async def view_list_plants(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS cou_sn, name as cou_name FROM course ORDER BY name
        """)
        courses = list(db)

        db.execute("""
        SELECT 
            p.sn,
            c.no as cou_no,
            c.name as cou_name,
            c.attr as cou_attr,
            c.score as cou_score,
            p.semester,
            p.class_time,
            p.week,
            p.class_position
        FROM plant as p
            INNER JOIN course as c  ON p.cou_sn = c.sn
        ORDER BY cou_no;
        """)

        items = list(db)

    return render_html(request, 'plant_list.html',
                       courses=courses,
                       items=items)


@web_routes.get('/plant/edit/{sn}')
def view_plant_editor(request):
    sn = request.match_info.get("sn")
    if sn is None:
        return web.HTTPBadRequest(text="sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT sn, cou_sn, semester, week, class_time, class_position FROM plant
            WHERE sn= %(sn)s ;
        """, dict(sn=sn))

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such plant: sn={sn}")

    with db_block() as db:
        db.execute("""
        SELECT sn AS cou_sn, name as cou_name FROM course ORDER BY name
        """)
        courses = list(db)

    return render_html(request, "plant_edit.html",
                       courses=courses,
                       record=record)


@web_routes.get("/plant/delete/{sn}")
def grade_deletion_dialog(request):
    sn = request.match_info.get("sn")
    if sn is None:
        return web.HTTPBadRequest(text="sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT 
            p.semester,
            c.no as cou_no,
            c.name as cou_name
        FROM plant as p
            INNER JOIN course as c  ON p.cou_sn = c.sn
        WHERE p.sn = %(sn)s;
        """, dict(sn=sn))

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such plant: sn={sn}")

    return render_html(request, 'plant_dialog_deletion.html', record=record)
