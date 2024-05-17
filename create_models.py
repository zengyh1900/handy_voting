from omegaconf import OmegaConf

from server import Model, app, db
from server.models.model import ModelRole


config = OmegaConf.load("./config.yaml")


with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()

    for model in config.models:
        m = Model(name=model.name, type=ModelRole[model.type])
        db.session.add(m)

    db.session.commit()
