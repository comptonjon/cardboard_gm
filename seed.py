from models import User, Card, TradeRequest, RequestCard, db
from app import app

db.drop_all()
db.create_all()

jcom = User.register(username="jcompton", password="qqqqqqqq", first_name="Jon", last_name="Compton", email="j@c.com", has_img=True)
klew = User.register(username="klew", password="qqqqqqqq", first_name="Kyle", last_name="Lewis", email="k@l.com", has_img=True)
mgon = User.register(username="mgonzales", password="qqqqqqqq", first_name="Marco", last_name="Gonzales", email="m@g.com")
u4 = User.register(username="kseager", password="qqqqqqqq", first_name="Kyle", last_name="Seager", email="k@s.com", has_img=True)
u5 = User.register(username="tfrance", password="qqqqqqqq", first_name="Ty", last_name="France", email="t@f.com")
u6 = User.register(username="slong", password="qqqqqqqq", first_name="Shed", last_name="Long", email="s@l.com", has_img=True)
u7 = User.register(username="jcrawford", password="qqqqqqqq", first_name="J.P.", last_name="Crawford", email="jp@c.com", has_img=True)
u8 = User.register(username="dmoore", password="qqqqqqqq", first_name="Dylan", last_name="Moore", email="d@m.com", has_img=True)
u9 = User.register(username="pervin", password="qqqqqqqq", first_name="Phil", last_name="Ervin", email="p@e.com", has_img=True)
u10 = User.register(username="jsheffield", password="qqqqqqqq", first_name="Justus", last_name="Sheffield", email="j@s.com", has_img=True)
u11 = User.register(username="jdunn", password="qqqqqqqq", first_name="Justin", last_name="Dunn", email="j@d.com", has_img=True)
u12 = User.register(username="ykikuchi", password="qqqqqqqq", first_name="Yusei", last_name="Kikuchi", email="y@k.com", has_img=True)
u13 = User.register(username="kgraveman", password="qqqqqqqq", first_name="Kendall", last_name="Graveman", email="k@g.com", has_img=True)
u14 = User.register(username="jodom", password="qqqqqqqq", first_name="Joe", last_name="Odom", email="j@o.com", has_img=True)
u15 = User.register(username="ltorrens", password="qqqqqqqq", first_name="Luis", last_name="Torrens", email="l@t.com", has_img=True)
u16 = User.register(username="jmarmo", password="qqqqqqqq", first_name="Jose", last_name="Marmolejos", email="j@m.com", has_img=True)
u17 = User.register(username="ttrammell", password="qqqqqqqq", first_name="Taylor", last_name="Trammell", email="t@t.com", has_img=True)
u18 = User.register(username="jkelenic", password="qqqqqqqq", first_name="Jarred", last_name="Kelenic", email="j@k.com", has_img=True)
u19 = User.register(username="jgerber", password="qqqqqqqq", first_name="Joey", last_name="Gerber", email="j@g.com", has_img=True)
u20 = User.register(username="ewhite", password="qqqqqqqq", first_name="Evan", last_name="White", email="e@w.com", has_img=True)
u21 = User.register(username="yhirano", password="qqqqqqqq", first_name="Yosahiso", last_name="Hirano", email="y@h.com", has_img=True)
u22 = User.register(username="twalker", password="qqqqqqqq", first_name="Taijuan", last_name="Walker", email="t@w.com", has_img=True)
u23 = User.register(username="anola", password="qqqqqqqq", first_name="Austin", last_name="Nola", email="a@n.com", has_img=True)
u24 = User.register(username="dgordon", password="qqqqqqqq", first_name="Dee", last_name="Gordon", email="d@g.com", has_img=True)
u25 = User.register(username="nmargevicius", password="qqqqqqqq", first_name="Nick", last_name="Margevicius", email="n@g.com", has_img=True)

db.session.add_all([jcom, klew, mgon, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15, u16, u17, u18, u19, u20, u21, u22, u23, u24, u25])
db.session.commit()

acuna = Card.create(owner_id=jcom.id, player="Ronald Acuna Jr", year="2018", set_name="Topps Series 2", number="698", desc="PSA 10", has_img=True)
tatis = Card.create(owner_id=jcom.id, player="Fernando Tatis Jr", year="2019", set_name="Topps Seris 2", number="410", desc="PSA 10", has_img=True)

griffeyUD = Card.create(owner_id=klew.id, player="Ken Griffey Jr", year="1989", set_name="Upper Deck", number="1", desc="PSA 9", has_img=True)
griffeyDon = Card.create(owner_id=klew.id, player="Ken Griffey Jr", year="1989", set_name="Donruss", number="33", desc="PSA 10", has_img=True)

mantle56 = Card.create(owner_id=mgon.id, player="Mickey Mantle", year="1956", set_name="Topps", number="135", desc="PSA 5.5", has_img=True)
mantle52 = Card.create(owner_id=mgon.id, player="Mickey Mantle", year="1952", set_name="Topps", number="311", desc="Authentic", has_img=True)

mays52t = Card.create(owner_id=mgon.id, player="Willie Mays", year="1952", set_name="Topps", number="261", desc="PSA 4", has_img=True)
mays53t = Card.create(owner_id=mgon.id, player="Willie Mays", year="1953", set_name="Topps", number="244", desc="Very Good", has_img=True)
mays54b = Card.create(owner_id=mgon.id, player="Willie Mays", year="1954", set_name="Bowman", number="89", desc="Near Mint", has_img=True)
aaron54t = Card.create(owner_id=mgon.id, player="Hank Aaron", year="1954", set_name="Topps", number="128", desc="PSA 7", has_img=True)
clemente55t = Card.create(owner_id=mgon.id, player="Roberto Clemente", year="1955", set_name="Topps", number="164", desc="BVG 4", has_img=True)
koufax55t = Card.create(owner_id=mgon.id, player="Sandy Koufax", year="1955", set_name="Topps", number="123", desc="PSA 6.5", has_img=True)
mays55t = Card.create(owner_id=mgon.id, player="Willie Mays", year="1955", set_name="Topps", number="194", desc="VG-EX", has_img=True)
ted56t = Card.create(owner_id=mgon.id, player="Ted Williams", year="1956", set_name="Topps", number="5", desc="PSA 6", has_img=True)
ted57t = Card.create(owner_id=mgon.id, player="Ted Williams", year="1957", set_name="Topps", number="1", desc="PSA 7", has_img=True)
ted58t = Card.create(owner_id=mgon.id, player="Ted Williams", year="1958", set_name="Topps", number="1", desc="PSA 8.5", has_img=True)
musial48b = Card.create(owner_id=mgon.id, player="Stan Musial", year="1948", set_name="Bowman", number="36", desc="PSA 4", has_img=True)
berra48b = Card.create(owner_id=mgon.id, player="Yogi Berra", year="1948", set_name="Bowman", number="6", desc="PSA 1 Poor", has_img=True)
paige49b = Card.create(owner_id=mgon.id, player="Satchel Paige", year="1949", set_name="Bowman", number="224", desc="PSA 6 EX-MT", has_img=True)
mays51b = Card.create(owner_id=mgon.id, player="Willie Mays", year="1951", set_name="Bowman", number="305", desc="PSA 4", has_img=True)
mantle53b = Card.create(owner_id=mgon.id, player="Mickey Mantle", year="1953", set_name="Bowman", number="59", desc="PSA 5 EX", has_img=True)
nolan68t = Card.create(owner_id=mgon.id, player="Nolan Ryan", year="1968", set_name="Topps", number="177", desc="PSA 7.5 NM+", has_img=True)
munson70t = Card.create(owner_id=mgon.id, player="Thurman Munson", year="1970", set_name="Topps", number="189", desc="PSA 5", has_img=True)
clem71t = Card.create(owner_id=mgon.id, player="Roberto Clemente", year="1971", set_name="Topps", number="630", desc="PSA 8", has_img=True)
brock62t = Card.create(owner_id=mgon.id, player="Lou Brock", year="1962", set_name="Topps", number="387", desc="Excellent", has_img=True)
yaz60t = Card.create(owner_id=mgon.id, player="Carl Yastrzemski", year="1960", set_name="Topps", number="148", desc="BVG 6", has_img=True)

db.session.add_all([acuna, tatis, griffeyUD, griffeyDon, mantle52, mantle56, mays52t, mays53t, mays54b, aaron54t, clemente55t, koufax55t, mays55t, ted56t, ted57t, ted58t, musial48b, berra48b, paige49b, mays51b, mantle53b, nolan68t, munson70t, clem71t, brock62t, yaz60t])
db.session.commit()

req1 = TradeRequest(from_id=1, to_id=2)
req2 = TradeRequest(from_id=2, to_id=1)
req3 = TradeRequest(from_id=2, to_id=3)
req4 = TradeRequest(from_id=2, to_id=3)
req5 = TradeRequest(from_id=3, to_id=1)
req6 = TradeRequest(from_id=3, to_id=2)

db.session.add_all([req1, req2, req3, req4, req5, req6])
db.session.commit()

rc1 = RequestCard(request_id=1, card_id=2, requested=False)
rc2 = RequestCard(request_id=1, card_id=3, requested=True)
rc3 = RequestCard(request_id=2, card_id=3, requested=False)
rc4 = RequestCard(request_id=2, card_id=4, requested=False)
rc5 = RequestCard(request_id=2, card_id=1, requested=True)
rc6 = RequestCard(request_id=3, card_id=3, requested=False)
rc7 = RequestCard(request_id=3, card_id=4, requested=False)
rc8 = RequestCard(request_id=3, card_id=5, requested=True)
rc9 = RequestCard(request_id=4, card_id=4, requested=False)
rc10 = RequestCard(request_id=4, card_id=6, requested=True)
rc11 = RequestCard(request_id=5, card_id=5, requested=False)
rc12 = RequestCard(request_id=5, card_id=1, requested=True)
rc13 = RequestCard(request_id=6, card_id=5, requested=False)
rc14 = RequestCard(request_id=6, card_id=3, requested=True)
rc15 = RequestCard(request_id=6, card_id=4, requested=True)

db.session.add_all([rc1, rc2, rc3, rc4, rc5, rc6, rc7, rc8, rc9, rc10, rc11, rc12, rc13, rc14, rc15])
db.session.commit()
