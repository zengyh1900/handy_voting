import enum

from .. import db


class ModelRole(enum.Enum):
    reference = 0
    target = 1
    baseline = 2


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    vote_count = db.Column(db.Integer, nullable=False, default=0)
    shown_count = db.Column(db.Integer, nullable=False, default=0)
    type = db.Column(db.Enum(ModelRole), nullable=False)

    @staticmethod
    def reference_models():
        return Model.query.filter_by(type=ModelRole.reference).order_by(Model.id.asc()).all()

    @staticmethod
    def target_models():
        return Model.query.filter_by(type=ModelRole.target).order_by(Model.id.asc()).all()

    @staticmethod
    def baseline_models():
        return Model.query.filter_by(type=ModelRole.baseline).order_by(Model.id.asc()).all()

    def __repr__(self):
        return "<Model #%d[%s], votes = %d, shown = %d>" % (self.id, self.name, self.vote_count, self.shown_count)
