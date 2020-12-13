from aiohttp import web
from .config import db_block, web_routes, render_html


@web_routes.get("/grade")
async def view_list_grades(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS stu_sn, name as stu_name FROM student ORDER BY name
        """)
        students = list(db)

        db.execute("""
        SELECT 
            p.sn AS pla_sn,
            p.semester AS pla_semester, 
            c.name as cou_name,
            c.no as cou_no
        FROM plant as p
        INNER JOIN course as c ON p.cou_sn = c.sn
        ORDER BY semester
        """)
        plants = list(db)

        db.execute("""
        SELECT g.stu_sn, g.pla_sn, 
            s.name as stu_name, 
            p.cou_name as cou_name,
            p.semester as pla_semester, 
            g.grade 
        FROM plant_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN (SELECT p1.sn as sn, c.name as cou_name, p1.semester as semester FROM plant as p1 INNER JOIN course as c on c.sn = p1.cou_sn) as p ON g.pla_sn = p.sn
        ORDER BY stu_sn, pla_sn;
        """)

        items = list(db)

    return render_html(request, 'grade_list.html',
                       students=students,
                       plants=plants,
                       items=items)


@web_routes.get('/grade/edit/{stu_sn}/{pla_sn}')
def view_grade_editor(request):
    stu_sn = request.match_info.get("stu_sn")
    pla_sn = request.match_info.get("pla_sn")
    if stu_sn is None or pla_sn is None:
        return web.HTTPBadRequest(text="stu_sn, pla_sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT grade FROM plant_grade
            WHERE stu_sn = %(stu_sn)s AND pla_sn = %(pla_sn)s;
        """, dict(stu_sn=stu_sn, pla_sn=pla_sn))

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such grade: stu_sn={stu_sn}, pla_sn={pla_sn}")

    return render_html(request, "grade_edit.html",
                       stu_sn=stu_sn,
                       pla_sn=pla_sn,
                       grade=record.grade)


@web_routes.get("/grade/delete/{stu_sn}/{pla_sn}")
def grade_deletion_dialog(request):
    stu_sn = request.match_info.get("stu_sn")
    pla_sn = request.match_info.get("pla_sn")
    if stu_sn is None or pla_sn is None:
        return web.HTTPBadRequest(text="stu_sn, pla_sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT g.stu_sn, g.pla_sn,
            s.name as stu_name, 
            p.cou_name as cou_name, 
            p.semester as pla_semester,
            g.grade 
        FROM plant_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN (SELECT p1.sn as sn, c.name as cou_name, p1.semester as semester FROM plant as p1 INNER JOIN course as c on c.sn = p1.cou_sn) as p ON g.pla_sn = p.sn
        WHERE stu_sn = %(stu_sn)s AND pla_sn = %(pla_sn)s;
        """, dict(stu_sn=stu_sn, pla_sn=pla_sn))

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such grade: stu_sn={stu_sn}, pla_sn={pla_sn}")

    return render_html(request, 'grade_dialog_deletion.html', record=record)
