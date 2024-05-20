import enum
import json

from .. import db


class ModelRole(enum.Enum):
    reference = 0
    target = 1
    baseline = 2


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.Enum(ModelRole), nullable=False)
    # vote_count = db.Column(db.PickleType, nullable=False, default=[0])
    # shown_count = db.Column(db.PickleType, nullable=False, default=[0])
    # 使用字符串类型存储序列化的整数列表
    vote_count_list = db.Column(db.String)
    shown_count_list = db.Column(db.String)

    @property
    def vote_count(self):
        # 反序列化列表
        return json.loads(self.vote_count_list)

    @vote_count.setter
    def vote_count(self, value):
        # 序列化列表
        self.vote_count_list = json.dumps(value)

    @property
    def shown_count(self):
        # 反序列化列表
        return json.loads(self.shown_count_list)

    @shown_count.setter
    def shown_count(self, value):
        # 序列化列表
        self.shown_count_list = json.dumps(value)

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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(80), unique=True, nullable=False)
    votes = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "<User #%d[%s], admin = %r>" % (self.id, self.userid, self.votes)
