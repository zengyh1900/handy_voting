import os
import os.path
import random

from flask import abort, jsonify, render_template, request, session
from omegaconf import OmegaConf

from . import app, config, db
from .models import Model
from .models.model import ModelRole


config = OmegaConf.load("./config.yaml")

root_path = os.path.dirname(__file__)

IMG_LIST = sorted(os.listdir(os.path.join(root_path, config.APP_SETTINGS.IMG_DATA_DIR, config.models[0].name)))


@app.route("/")
def display():
    with open(os.path.join(root_path, "templates/display.html"), "r") as f:
        return f.read()
    # return render_template(os.path.join(root_path, 'templates/display.html'), title = config.name)


@app.route("/getimages")
def getimages():
    img_filename = random.choice(IMG_LIST)
    selected_models = choose_models()
    session["models"] = [m.id for m in selected_models]
    res = [
        {
            "id": i,
            "img": os.path.join(config.APP_SETTINGS["IMG_DATA_DIR"], m.name, img_filename),
            "isgroundtruth": m.type == ModelRole.groundtruth,
        }
        for i, m in enumerate(selected_models)
    ]
    return jsonify({"imgs": res})


@app.route("/vote", methods=["POST"])
def vote():
    choice = 0
    try:
        choice = int(request.json["choice"])
    except ValueError:
        abort(400)
    selected_models = session["models"]
    if choice >= len(selected_models):
        abort(400)
    choice = selected_models[choice]
    model = Model.query.get(choice)
    if model.type == ModelRole.groundtruth:
        abort(400)
    model.vote_count += 1
    db.session.add(model)
    for id in selected_models:
        model = Model.query.get(id)
        model.shown_count += 1
        db.session.add(model)
    db.session.commit()
    return jsonify({"status": "ok"}), 200


@app.route("/admin")
def admin():
    all_models = Model.query.all()
    return render_template("admin.html", models=all_models)


def choose_models():
    groundtruth_models = Model.groundtruth_models()
    target_models = Model.target_models()
    baseline_models = Model.baseline_models()
    random.shuffle(baseline_models)
    selected_models = target_models + baseline_models[: config.APP_SETTINGS["NUM_MODELS"]]
    random.shuffle(selected_models)
    return groundtruth_models + selected_models