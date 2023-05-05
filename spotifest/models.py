from spotifest import db


class Festival(db.Model):
    # TODO: Need to vi som gillar 90-talet
    name = db.Column(db.String(64), primary_key=True, index=True, unique=True)
    date = db.Column(db.String(64), index=True)
    venue = db.Column(db.String(64), index=True)
    country = db.Column(db.String(64), index=True)

    def __repr__(self):
        return f"{self.name} {self.date}"


class Band(db.Model):
    name = db.Column(db.String(64), primary_key=True, index=True, unique=True)

    def __repr__(self):
        return f"{self.name}"


class FestivalBand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO: ASK TEACHER IF THIS IS THE RIGHT WAY TO DO THIS
    festival_name = db.Column(db.ForeignKey('festival.name'))
    band_name = db.Column(db.ForeignKey('band.name'))

    def __repr__(self):
        return f"{self.band_name} plays at {self.festival_name}"


