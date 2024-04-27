import http.server
import os
import shutil
from http import HTTPStatus
import sys
import io


class RequestHandlerImpl(http.server.BaseHTTPRequestHandler):
    def write_static_file(self, file_path, is_img):
        f = open(file_path, 'rb')
        fs = os.fstat(f.fileno())
        if is_img:
            self.send_header("Content-Type", "image/jpeg")
        else:
            self.send_header("Content-Type", "text/javascript")
        self.send_header("Content-Length", str(fs[6]))
        self.end_headers()

        try:
            shutil.copyfileobj(f, self.wfile)
        finally:
            f.close()

    def do_GET(self):
        print(self.path)
        self.send_response(HTTPStatus.OK)
        if self.path.endswith(".js"):
            self.write_static_file(self.path[1:], False)
            return

        paths = self.path.split('/')
        if len(paths) < 3:
            self.send_error(HTTPStatus.NOT_FOUND, self.path)
            return
        vol = paths[1]
        page = paths[2]
        if self.path.endswith(".jpg"):
            page = page[:-4]
            file_path = "JXZ/{vol}/劲小子{vol} ({page}).jpg".format(vol=vol, page=page)
            self.write_static_file(file_path, True)
            return

        next_page = "{page}".format(vol=vol, page=str(int(page) + 1))
        next_file = "JXZ/{vol}/劲小子{vol} ({page}).jpg".format(vol=vol, page=next_page)
        if not os.path.exists(next_file):
            next_page = "../{vol}/1".format(vol=str(int(vol) + 1))
        img_name = "{page}.jpg".format(page=page)

        r = ['<html><head><meta http-equiv="Content-Type" content="text/html">',
             '<body><div style="text-align:center"><a href="%s">' % next_page,
             '<img src="%s" height="1505" width="1000"></img></a></div>' % img_name,
             '<script src="/static/redirect.js"></script>',
             '<div style="text-align:center;bottom:0">'
             '<nobr> VOLUME: </nobr><select onchange="s_click(this)" name="vol">',
             ]
        for i in range(1, 24):
            if i == int(vol):
                r.append('<option value="{vol}" selected="selected">{vol}</option>'.format(vol=str(i)))
            else:
                r.append('<option value="{vol}">{vol}</option>'.format(vol=str(i)))
        r.append('</select><nobr> PAGE: </nobr><select onchange="s_click(this)" name="page">')
        for i in range(1, 200):
            if i == int(page):
                r.append('<option value="{page}" selected="selected">{page}</option>'.format(page=str(i)))
            else:
                r.append('<option value="{page}">{page}</option>'.format(page=str(i)))
        r.append('</select>')
        r.append('<button onclick=jump()>Jump</button>')
        r.append('</div></body></html>')

        enc = sys.getfilesystemencoding()
        encoded = '\n'.join(r).encode(enc, 'err')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)


server_address = ("", 8000)
httpd = http.server.HTTPServer(server_address, RequestHandlerImpl)
httpd.serve_forever()

