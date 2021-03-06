from . import serialization
import json
import os
from flask import Flask, request, make_response
from flask.helpers import send_file
from flask_cors import CORS
from .session import Session, SessionStage, SessionState
from .serialization.json import Encoder, Decoder
from . import settings

app = Flask(__name__)
CORS(app)


def notfound():
    return make_response("Not Found", 404)


def ok_string(text):
    return make_response(text, 200)


def ok_json(obj):
    return json.dumps(obj, cls=Encoder), 200, {"Content-Type": "application/json"}


def get_flag(data, name):
    if data.get(name):
        return True
    return False


@app.route('/api/session/all', methods=['GET'])
def get_all_session():
    sids = []
    for item in os.listdir(settings.DATA_PATH):
        path = os.path.join(settings.DATA_PATH, item)
        if os.path.isdir(path):
            sids.append(item)
    return ok_json(sids)


@app.route('/api/session', methods=['POST'])
def input_video():
    session = Session()
    file = request.files.get("file")
    if file:
        session.initialize()
        if session.input_video(file):
            return ok_string(session.id)
        else:
            session.clear()
            return notfound()
    return notfound()

@app.route('/api/session/<sid>/input', methods=['PUT'])
def work_input(sid):
    data = request.get_json()
    redo = get_flag(data, "redo")

    session = Session(sid)
    if session.work_input(redo=redo):
        return ok_string(session.id)
    return notfound()

@app.route('/api/session/<sid>/input', methods=['GET'])
def result_input(sid):
    session = Session(sid)
    result = session.result_input()
    if result:
        return ok_json(result.as_dict())
    else:
        return notfound()

@app.route('/api/session/<sid>/stage', methods=['GET'])
def get_stage(sid):
    session = Session(sid)
    return ok_string(str(session.stage().value))


@app.route('/api/session/<sid>/state', methods=['GET'])
def get_state(sid):
    session = Session(sid)
    return ok_string(str(session.state().value))


@app.route('/api/session/<sid>/video', methods=['GET'])
def get_video(sid):
    session = Session(sid)
    path = session.video_path()
    if path:
        return send_file(path, mimetype="video/mp4")
    return notfound()

# region frames


@app.route('/api/session/<sid>/frames', methods=['PUT'])
def work_frames(sid):
    data = request.get_json()
    redo = get_flag(data, "redo")

    session = Session(sid)
    if session.work_frames(redo=redo):
        return ok_string(session.id)
    return notfound()


@app.route('/api/session/<sid>/frames', methods=['GET'])
def result_frames(sid):
    session = Session(sid)
    result = session.result_frames()
    if result:
        return ok_json(result.as_dict())
    else:
        return notfound()


@app.route('/api/session/<sid>/frames/<name>', methods=['GET'])
def frame_image_path(sid, name):
    session = Session(sid)
    path = session.frame_image_path(name)
    if path:
        return send_file(path, mimetype="image/jpeg")
    return notfound()

# endregion

# region subtitles


@app.route('/api/session/<sid>/subtitles', methods=['PUT'])
def work_subtitles(sid):
    data = request.get_json()
    redo = get_flag(data, "redo")
    isZhcn = get_flag(data, "isZhcn")

    session = Session(sid)

    from .subtitles.generator import DefaultSubtitleGenerator
    worker = DefaultSubtitleGenerator(isZhcn)

    if session.work_subtitles(worker, redo=redo):
        return ok_string(session.id)
    return notfound()


@app.route('/api/session/<sid>/subtitles', methods=['GET'])
def result_subtitles(sid):
    session = Session(sid)
    result = session.result_subtitles()
    if result:
        return ok_json(result.as_dict())
    else:
        return notfound()


@app.route('/api/session/<sid>/subtitles/<name>', methods=['GET'])
def subtitle_audio_path(sid, name):
    session = Session(sid)
    path = session.subtitle_audio_path(name)
    if path:
        return send_file(path, mimetype="audio/wav")
    return notfound()

# endregion

# region styles


@app.route('/api/session/<sid>/styles', methods=['PUT'])
def work_styles(sid):
    data = request.get_json()
    redo = get_flag(data, "redo")

    session = Session(sid)
    if session.work_styles(redo=redo):
        return ok_string(session.id)
    return notfound()


@app.route('/api/session/<sid>/styles', methods=['GET'])
def result_styles(sid):
    session = Session(sid)
    result = session.result_styles()
    if result:
        return ok_json(result.as_dict())
    else:
        return notfound()


@app.route('/api/session/<sid>/styles/<name>', methods=['GET'])
def styled_image_path(sid, name):
    session = Session(sid)
    path = session.styled_image_path(name)
    if path:
        return send_file(path, mimetype="image/jpeg")
    return notfound()

# endregion


# region comics


@app.route('/api/session/<sid>/comics', methods=['PUT'])
def work_comics(sid):
    data = request.get_json()
    redo = get_flag(data, "redo")

    session = Session(sid)
    if session.work_comics(redo=redo):
        return ok_string(session.id)
    return notfound()


@app.route('/api/session/<sid>/comics', methods=['GET'])
def result_comics(sid):
    session = Session(sid)
    result = session.result_comics()
    if result:
        return ok_json(result.as_dict())
    else:
        return notfound()


@app.route('/api/session/<sid>/comics/<file>', methods=['GET'])
def comic_file_path(sid, file):
    session = Session(sid)
    path = session.comic_file_path(file)
    if path:
        return send_file(path, mimetype="image/jpeg")
    return notfound()

# endregion


@app.route('/api/session/<sid>', methods=['DELETE'])
def clear(sid):
    session = Session(sid)
    if session.state() is not SessionState.AfterCreate:
        session.clear()
        return ok_string(session.id)
    return notfound()
