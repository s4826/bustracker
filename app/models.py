
class Route(db.Model):
    __tablename__ = "Routes"
    id = db.Column(db.Integer, primary_key=True)
    mbta_id = db.Column(db.String(32), nullable=False, unique=True)
