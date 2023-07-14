from IOC.IOC_crall import ioc_crawll
from IOC.ircclient.irc_client import Irc_bot
from flask import Flask
import json, asyncio
from flask import request

app = Flask(__name__)
IOC = ioc_crawll(
    host="localhost",
    port="5432",
    user="postgres",
    password="mysecretpassword",
)
# TODO handel the following
#      handel links, keywords resources
#      creeate the basic search features for keywords


async def ircRunner():
    pass


@app.route("/irc/run")
def run():
    bot1 = Irc_bot("192.168.56.107", 6667, "#general")


@app.route("/irc/register")
def irc_add():
    pass


@app.route("/")
def root():
    return "running..."


@app.route("/site/list")
def list_keywords():
    IOC.cur.execute("SELECT * FROM website")
    return json.dumps(IOC.cur.fetchall())


@app.route("/keywords/list")
def list_keyword():
    IOC.cur.execute("SELECT * FROM keywords")
    return json.dumps(IOC.cur.fetchall())


# url, dir
@app.route("/site/register", methods=["POST"])
def siteRegister():
    print("reg site----")
    print(request.form)
    dir = "NULL"
    if "url" not in request.form:
        return json.dumps({"message": "no url was supplied"})
    if "dir" in request.form:
        dir = request.form["dir"]
    url = request.form["url"]
    query = "insert into website(url,dir) values(%s,%s)"
    try:
        IOC.cur.execute(query, (url, dir))
        return json.dumps({"message": "DONE"})
    except:
        return json.dumps({"message": "runtime exception"})


@app.route("/keywords/register", methods=["POST"])
def registerKeyword():
    query = "INSERT INTO keywords(word) values(%s)"
    if "keyword" not in request.form:
        return json.dumps({"message": "No keyword was passed"})
    IOC.cur.execute(query, (request.form["keyword"],))
    return json.dumps({"message": "Sucessfull"})


def main():
    app.run()
    # list = OCI.search(query="card")
    # print(list)
    # del OCI


if __name__ == "__main__":
    main()
    pass
