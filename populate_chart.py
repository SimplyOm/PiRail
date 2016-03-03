from app import db,models
from app.views import send_sms
u1 = models.Chart(name='Nitin',pnr=1409503636,mobile='8272859757',password='3636',seat=3)
#send_msg(u1.mobile,"Your password is "+u1.password+" - Indian Railways")
u2 = models.Chart(name='Aman',pnr=1409500404,mobile='8874671844',password='0404',seat=4)
send_sms(u2.mobile,"Your password is "+u2.password+" - Indian Railways")
u3 = models.Chart(name='Harsh',pnr=1409501818,mobile='7754812482',password='1818',seat=18)
u4 = models.Chart(name='Om',pnr=1409503737,mobile='7607986662',password='3737',seat=12)
db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.add(u4)
db.session.commit()