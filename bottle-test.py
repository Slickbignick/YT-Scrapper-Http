from bottle import run, route, request
import sqlite3 as sql

conn = sql.connect("../webdrivers/views.db")
cur = conn.cursor()


@route("/channel/<channel>")
def data(channel):
    title = request.query.title
    orderby = request.query.orderby.lower()
    ascdesc = request.query.ascdesc.lower()
    views_greater_than = request.query.views_greater_than
    views_less_than = request.query.views_less_than
    offset = request.query.offset
    limit = request.query.limit

    if orderby not in ["views", "title", "id", "length"]:
        orderby = "id"
    if ascdesc not in ["asc", "desc"]:
        ascdesc = "asc"
    if offset == "":
        offset = 0
    if limit == "" or int(limit) <= 0:
        limit = 10
    elif int(limit) > 100:
        limit = 100

    if title is not None or isinstance(title, str):
        query_statement = f"""SELECT * FROM {channel} where title like '%{title}%' or title like '{title}%'
         order by {orderby} {ascdesc} limit {limit} offset {offset};"""
    if title is None:
        query_statement = f"SELECT * FROM {channel} order by {orderby} {ascdesc} limit {limit} offset {offset};"

    try:
        query_results = cur.execute(query_statement)
        result = f"""<head><style> a {{color: white; text-decoration: none;}} a:visited, a:link {{color inherit; text-decoration: inherit;}} </style><link rel="help" href="/help"></head><body style="background-color: black">
        <table border="1" cellspacing="0" cellpadding="10" style="color: white;border:1px solid gray;margin-left:auto;margin-right:auto;">
        <thead><tr><th colspan="4">{str(channel).title()}</th></tr><tr><th>id</th><th>Videos</th><th>Length</th><th>Views</th></tr></thead><tbody>"""

        for i in query_results:
            i = list(i)
            id_ = i[0]

            title = i[1]

            length =  int(i[2])
            div = divmod(length,3600)
            if div[0] > 0:
                minutes = divmod(div[1], 60)

                minute = str(minutes[0])
                if len(minute) == 1:
                   minute = minute.zfill(2) 

                second = str(minutes[1])
                if len(second) == 1:
                   second = second.zfill(2) 

                length = f'{div[0]}:{minute}:{second}'

            else:
                minutes = divmod(div[1], 60)

                minute = str(minutes[0])
                if len(minute) == 1:
                   minute = minute.zfill(2) 

                second = str(minutes[1])
                if len(second) == 1:
                   second = second.zfill(2) 

                length = f'{minute}:{second}'
                
            views = int(i[3])
            if len(str(views)) >= 7:
                views = str(round(views / 1000000, 1)) + "M"
            elif 7 > len(str(views)) >= 4:
                views = str(round(views / 1000, 1)) + "K"
            else:
                pass
            
            link = i[4]

            result += f"<tr><td>{id_}</td><td><a target='_blank' href='{link}'>{title}</a></td><td>{length}</td><td>{views}</td></tr>"
        result += "</tbody></table></body>" 
        return result

    except sql.OperationalError:

        query_results = cur.execute("SELECT * FROM sqlite_sequence").fetchall()

        result = "<h1>Error!</h1><h3>The following channels are valid</h3><ul>"

        for i in query_results:
            result += f"<li><a href='/{i[0]}'>{i[0]}</a></li>"
        result += "</ul>"

        return result


@route("/help")
def help():
    return "<body><table><thead><tr><th>Queries</th><th>Parameters</th></tr></thead><tbody><tr><td></tr></tbody></table></body>"


if __name__ == "__main__":
    run(debug=True, reloader=True)
