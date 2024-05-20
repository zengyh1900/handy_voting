import os
import os.path
import random

from flask import abort, jsonify, make_response, render_template, request, session
from omegaconf import OmegaConf

from . import app, db
from .models import Model, ModelRole, User


config = OmegaConf.load("./config.yaml")

root_path = os.path.dirname(__file__)

IMG_LIST = sorted(os.listdir(os.path.join(root_path, config.APP_SETTINGS.DATA_DIR, config.models[0].name)))


@app.route("/")
def display():
    assert config.title is not None, "set the title of your user study in the config.yml"
    assert config.guideline is not None, "set the guideline of your user study in the config.yml"

    html_file = config.APP_SETTINGS.DATA_TYPE + ".html"
    # if config.metrics is not None and len(config.metrics) > 1:
    #     response = render_template(html_file, title=config.title, guideline=config.guideline, metrics=config.metrics)
    # else:
    response = render_template(html_file, title=config.title, guideline=config.guideline)
    response = make_response(response)
    response.headers["Content-Type"] = "text/html"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/getimages")
def getimages():
    img_filename = random.choice(IMG_LIST)
    selected_models = choose_models()
    session["models"] = [m.id for m in selected_models]
    res = [
        {
            "id": i,
            "img": os.path.join(config.APP_SETTINGS["DATA_DIR"], m.name, img_filename),
            "isreference": m.type == ModelRole.reference,
        }
        for i, m in enumerate(selected_models)
    ]
    metrics = [{"id": i, "name": name} for i, name in enumerate(config.metrics)]
    return jsonify(
        {
            "imgs": res,
            "metrics": metrics,
        }
    )


@app.route("/vote", methods=["POST"])
def vote():
    choices = 0
    try:
        choices = list(request.json["choice"])
    except ValueError:
        abort(400)

    selected_models = session["models"]
    # if choices >= len(selected_models):
    #     abort(400)

    for i, c in enumerate(choices):
        c = int(c)
        choice = selected_models[c]
        model = Model.query.get(choice)
        print(i, c, config.metrics[i], model.name)
        if model.type == ModelRole.reference:
            abort(400)

        # update the vote count and shown count
        value = model.vote_count
        value[config.metrics[i]] += 1
        model.vote_count = value
        db.session.add(model)
        for id in selected_models:
            model = Model.query.get(id)
            value = model.shown_count
            value[config.metrics[i]] += 1
            model.shown_count = value
            db.session.add(model)
        db.session.commit()
        # print(model.shown_count, model.vote_count)

    # update the users
    user_id = request.remote_addr
    try:
        user = User.query.filter_by(userid=user_id).first()
        if user:
            user.votes += 1
        else:
            user = User(userid=user_id, votes=1)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)

    return jsonify({"status": "ok"}), 200


@app.route("/admin")
def admin():
    all_models = Model.query.all()
    voted_users = User.query.all()
    return render_template("admin.html", models=all_models, metrics=config.metrics, voted_users=len(voted_users))


def choose_models():
    reference_models = Model.reference_models()
    target_models = Model.target_models()
    baseline_models = Model.baseline_models()
    random.shuffle(baseline_models)
    selected_models = target_models + baseline_models[: config.APP_SETTINGS["NUM_MODELS"]]
    random.shuffle(selected_models)
    return reference_models + selected_models
