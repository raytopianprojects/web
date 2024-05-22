import cgi
import os
from http.cookies import SimpleCookie
import sqlite3
import html
import ast


def Cookie():
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

    def update(self, name, value, where):
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        cur.execute(f"UPDATE {self.name} SET ? = ? WHERE ?", (name, value, where))
        con.commit()
        con.close()

    def delete(self):
        ...

    def create(self):
        ...

    def select(self, *args):
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        res = con.execute

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
    def AUTH_TYPE(self):
        return os.getenv("AUTH_TYPE")

    @property
    def CONTENT_LENGTH(self):
        return os.getenv("CONTENT_LENGTH")

    @property
    def DOCUMENT_ROOT(self):
        return os.getenv("DOCUMENT_ROOT")

    @property
    def DOCUMENT_NAME(self):
        return os.getenv("DOCUMENT_NAME")

    @property
    def DATE_GMT(self):
        return os.getenv("DATE_GMT")

    @property
    def DATE_LOCAL(self):
        return os.getenv("DATE_LOCAL")

    @property
    def DOCUMENT_NAME(self):
        return os.getenv("DOCUMENT_NAME")

    @property
    def DATE_GMT(self):
        return os.getenv("DATE_GMT")

    @property
    def DATE_LOCAL(self):
        return os.getenv("DATE_LOCAL")

    @property
    def DOCUMENT_URI(self):
        return os.getenv("DOCUMENT_URI")

    @property
    def GATEWAY_INTERFACE(self):
        return os.getenv("GATEWAY_INTERFACE")

    @property
    def LAST_MODIFIED(self):
        return os.getenv("LAST_MODIFIED")

    @property
    def PATH(self):
        return os.getenv("PATH")

    @property
    def PATH_INFO(self):
        return os.getenv("PATH_INFO")

    @property
    def PATH_TRANSLATED(self):
        return os.getenv("PATH_TRANSLATED")

    @property
    def REMOTE_ADDR(self):
        return os.getenv("REMOTE_ADDR")

    @property
    def REMOTE_HOST(self):
        return os.getenv("REMOTE_HOST")

    @property
    def REMOTE_IDENT(self):
        return os.getenv("REMOTE_IDENT")

    @property
    def REMOTE_USER(self):
        return os.getenv("REMOTE_USER")

    @property
    def REQUEST_METHOD(self):
        return os.getenv("REQUEST_METHOD")

    @property
    def SCRIPT_NAME(self):
        return os.getenv("SCRIPT_NAME")

    @property
    def SERVER_NAME(self):
        return os.getenv("SERVER_NAME")

    @property
    def SERVER_PORT(self):
        return os.getenv("SERVER_PORT")

    @property
    def SERVER_PROTOCOL(self):
        return os.getenv("SERVER_PROTOCOL")

    @property
    def SERVER_ROOT(self):
        return os.getenv("SERVER_ROOT")

    @property
    def SERVER_SOFTWARE(self):
        return os.getenv("SERVER_SOFTWARE")

    @property
    def HTTP_ACCEPT(self):
        return os.getenv("HTTP_ACCEPT")

    @property
    def HTTP_CONNECTION(self):
        return os.getenv("HTTP_CONNECTION")

    @property
    def HTTP_HOST(self):
        return os.getenv("HTTP_HOST")

    @property
    def HTTP_PRAGMA(self):
        return os.getenv("HTTP_PRAGMA")

    @property
    def HTTP_REFERER(self):
        return os.getenv("HTTP_REFERER")

    @property
    def HTTP_USER_AGENT(self):
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
        _print(f"<{self.name} {self.params}>")

    def __exit__(self, exc_type, exc_val, exc_tb):
        _print(f"</{self.name}>")


class form:
    def __init__(self, action):
        self.action = action

    def __enter__(self):
        _print(f"<form method='post' action='cgi-bin/{self.action}'>")

    def __exit__(self, exc_type, exc_val, exc_tb):
        _print(f"</form>")


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
