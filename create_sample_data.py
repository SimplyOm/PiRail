from app import db,models
import datetime
u1 = models.Chart.query.get(1)
u2 = models.Chart.query.get(2)
d1 = models.Discussion(topic='Requirement',message='I want water',timestamp=datetime.datetime.utcnow(), author=u1)
d2 = models.Discussion(topic='Health',message='I am having headache',timestamp=datetime.datetime.utcnow(), author=u1)
db.session.add(d1)
db.session.add(d2)
dm1 = models.Discuss(message='I have disprin plz tell ur seat no',timestamp=datetime.datetime.utcnow(),discussion=d2,sender=u2)
db.session.add(dm1)
dm2 = models.Discuss(message='my seat no is 3',timestamp=datetime.datetime.utcnow(),discussion=d2,sender=u1)
db.session.add(dm2)
db.session.commit()