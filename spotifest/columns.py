from spotifest import db


class Festival(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    date = db.Column(db.String(64), index=True)
    venue = db.Column(db.String(64), index=True)
    country = db.Column(db.String(64), index=True)

    def __repr__(self):
        return f"{self.name} {self.date}"


class Band(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

    def __repr__(self):
        return f"{self.name}"


class FestivalBand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO: ASK TEACHER IF THIS IS THE RIGHT WAY TO DO THIS
    festival_id = db.Column(db.Integer, db.ForeignKey('festival.id'))
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))

    def __repr__(self):
        return f"{self.band_id} plays at {self.festival_id}"
