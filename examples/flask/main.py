from flask import Flask, request

import BlockFrame

app = Flask(__name__)
block_frame = BlockFrame.BlockFrame(config="config.json", option="generic")


@app.route("/chunk", methods=["GET", "POST"])
def chunk():
    if request.method == "GET":
        return """
        <form action="/chunk" method="POST" enctype="multipart/form-data">
            <input type="file" name="data" placeholder="Data to chunk">
            <input type="submit" value="Submit">
        </form>
    """
    if request.method == "POST":
        data = bytes(f"{request.files['data'].read()}", "utf-8")
        block_frame.chunker.target(
            file_name=request.files["data"].filename, file_bytes=data, size=10
        )
        block_frame.chunker.generic_chunking()
        return "Chunking Done"


@app.route("/construct", methods=["GET", "POST"])
def construct():
    if request.method == "GET":
        ...

    if request.method == "POST":
        data = bytes(f"{request.files['data'].read()}", "utf-8")
        print(data)
        block_frame.chunker.target(file_bytes=data, size=10)
        block_frame.chunker.generic_chunking()
        return "Chunking Done"


if __name__ == "__main__":
    app.run(debug=True)
