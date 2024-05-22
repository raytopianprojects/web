"""MIT License

Copyright (c) 2024 Raytopia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import cgi
import os
from http.cookies import SimpleCookie
import sqlite3
import html
import ast


def cookie():
    return SimpleCookie(os.getenv("HTTP_COOKIE"))


print("Content-Type: text/html")
print("<!DOCTYPE html>")
print("Content-type: text/html\n\n")


def adapt_dict(dictonary):
    return str(dictonary)


def convert_dict(s):
    return ast.literal_eval(s)


def adapt_list(l):
    return str(l)


def convert_list(s):
    return ast.literal_eval(s)


def adapt_tuple(t):
    return str(t)


def convert_tuple(t):
    return ast.literal_eval(t)


def adapt_set(s):
    return str(s)


def convert_set(s):
    return ast.literal_eval(s)


# Register the adapter and converter
sqlite3.register_adapter(dict, adapt_dict)
sqlite3.register_converter("dict", convert_dict)
sqlite3.register_adapter(list, adapt_list)
sqlite3.register_converter("list", convert_list)
sqlite3.register_adapter(tuple, adapt_tuple)
sqlite3.register_converter("tuple", convert_tuple)
sqlite3.register_adapter(set, adapt_set)
sqlite3.register_converter("set", convert_set)


class Table:
    def __init__(self, name, database="default.database"):
        self.name = name
        self.database = database

        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(f"create table if not exists {self.name}(key, value)")
        con.commit()
        con.close()

    def __getitem__(self, key):
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        results = cur.execute(f"SELECT value FROM {self.name} WHERE key=?", (key,))
        data = results.fetchone()
        if data:
            data = data[0]
        con.commit()
        con.close()
        return data

    def __setitem__(self, key, value):
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        cur.execute(f"INSERT OR IGNORE INTO {self.name}(key, value) VALUES(?, ?)", (key, value))
        cur.execute(f"UPDATE {self.name} SET value=? WHERE key=?", (value, key))
        con.commit()
        con.close()

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(key)

        con = sqlite3.connect(self.database)
        cur = con.cursor()
        cur.execute(f"DELETE FROM {self.name} WHERE key=?", (key,))
        con.commit()
        con.close()

    def __contains__(self, key):
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM {self.name} WHERE key=?", (key,)).fetchone()
        con.commit()
        con.close()
        if result:
            return True
        else:
            return False


class Settings:
    @property
    def cookie(self):
        return os.getenv("HTTP_COOKIE")

    @property
    def query_string(self):
        return os.getenv("QUERY_STRING")

    @property
    def content_type(self):
        return os.getenv("CONTENT_TYPE")

    @property
    def request_method(self):
        return os.getenv("REQUEST_METHOD")

    @property
    def script_name(self):
        return os.getenv("SCRIPT_NAME")

    @property
    def auth_type(self):
        return os.getenv("AUTH_TYPE")

    @property
    def content_length(self):
        return os.getenv("CONTENT_LENGTH")

    @property
    def document_root(self):
        return os.getenv("DOCUMENT_ROOT")

    @property
    def document_name(self):
        return os.getenv("DOCUMENT_NAME")

    @property
    def date_gmt(self):
        return os.getenv("DATE_GMT")

    @property
    def data_local(self):
        return os.getenv("DATE_LOCAL")

    @property
    def document_uri(self):
        return os.getenv("DOCUMENT_URI")

    @property
    def gateway_interface(self):
        return os.getenv("GATEWAY_INTERFACE")

    @property
    def last_modified(self):
        return os.getenv("LAST_MODIFIED")

    @property
    def path(self):
        return os.getenv("PATH")

    @property
    def path_info(self):
        return os.getenv("PATH_INFO")

    @property
    def path_translated(self):
        return os.getenv("PATH_TRANSLATED")

    @property
    def remote_addr(self):
        return os.getenv("REMOTE_ADDR")

    @property
    def remote_host(self):
        return os.getenv("REMOTE_HOST")

    @property
    def remote_ident(self):
        return os.getenv("REMOTE_IDENT")

    @property
    def remote_user(self):
        return os.getenv("REMOTE_USER")

    @property
    def request_method(self):
        return os.getenv("REQUEST_METHOD")

    @property
    def script_name(self):
        return os.getenv("SCRIPT_NAME")

    @property
    def server_name(self):
        return os.getenv("SERVER_NAME")

    @property
    def server_port(self):
        return os.getenv("SERVER_PORT")

    @property
    def server_protocol(self):
        return os.getenv("SERVER_PROTOCOL")

    @property
    def server_root(self):
        return os.getenv("SERVER_ROOT")

    @property
    def server_software(self):
        return os.getenv("SERVER_SOFTWARE")

    @property
    def http_accept(self):
        return os.getenv("HTTP_ACCEPT")

    @property
    def http_connection(self):
        return os.getenv("HTTP_CONNECTION")

    @property
    def HTTP_HOST(self):
        return os.getenv("HTTP_HOST")

    @property
    def http_pragma(self):
        return os.getenv("HTTP_PRAGMA")

    @property
    def http_referer(self):
        return os.getenv("HTTP_REFERER")

    @property
    def http_user_agent(self):
        return os.getenv("HTTP_USER_AGENT")


settings = Settings()


class Input:
    def __init__(self):
        self.form = cgi.FieldStorage()

    def __getitem__(self, key):
        return self.form.getvalue(key)


input = Input()


class tag:
    def __init__(self, name, params=""):
        self.params = params
        self.name = name

    def __enter__(self):
        print(f"<{self.name} {self.params}>")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"</{self.name}>")


class form:
    def __init__(self, action, params=""):
        self.action = action
        self.params = params

    def __enter__(self):
        print(f"<form method='post' action='cgi-bin/{self.action}' {self.params}>")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"</form>")


def start():
    from http import server

    server.CGIHTTPRequestHandler.cgi_directories = ['/cgi-bin']

    s = server.HTTPServer(('', 8000), server.CGIHTTPRequestHandler)
    print("Serving at http://127.0.0.1:8000")

    s.serve_forever()


_print = print


def print(string):
    _print(html.escape(string))


if __name__ == "__main__":
    t = Table("new", )
    t["no"] = "bob"
    print(t["no"])
    with tag("h1"):
        print("DEMO")
    start()
