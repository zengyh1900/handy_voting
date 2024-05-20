from omegaconf import OmegaConf

from server import Model, app, db
from server.models.model import ModelRole


config = OmegaConf.load("./config.yaml")
template = {}
for m in config.metrics:
    template[m] = 0

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()

    for model in config.models:
        m = Model(name=model.name, type=ModelRole[model.type], vote_count=template, shown_count=template)
        db.session.add(m)

    db.session.commit()
