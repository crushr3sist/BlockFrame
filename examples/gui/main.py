from flask import Flask, request, redirect, url_for
import BlockFrame
from flaskwebgui import FlaskUI


app = Flask(__name__)
block_frame = BlockFrame.BlockFrame(config="config.json", option="generic")


@app.route("/chunk", methods=["GET", "POST"])
def chunk():
    if request.method == "POST":
        data = bytes(f"{request.files['data'].read()}", "utf-8")
        block_frame.chunker.target(
            file_name=request.files["data"].filename, file_bytes=data, size=10
        )
        block_frame.chunker.generic_chunking()
        return redirect(url_for("index"))


@app.route("/fetch", methods=["GET", "POST"])
def fetch():
    if request.method == "POST":
        file_name = request.form["data"]
        block_frame.fetcher.target(file_name)
        block_frame.fetcher.fetch()
        return "fetching Done"


@app.route("/", methods=["GET", "POST"])
def index():
    # write html for index page for /fetch and /chunk
    return """
    <h1>BlockFrame</h1>
    <h2>Chunk</h2>
    <form action="/chunk" method="POST" enctype="multipart/form-data">
        <input type="file" name="data" placeholder="Data to chunk">
        <input type="submit" value="Submit">
    </form>
    
    <h2>Fetch</h2>
    <form action="/fetch" method="POST" enctype="multipart/form-data">
        <input type="text" name="data" placeholder="Data to fetch">
        <input type="submit" value="Submit">
    </form>
    """


if __name__ == "__main__":
    FlaskUI(app=app, server="flask").run()
