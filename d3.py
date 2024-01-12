import ephem
import datetime
import math

class Day():
	
	s60=["甲乙丙丁戊己庚辛壬癸","子丑寅卯辰巳午未申酉戌亥"]
	s28="虚危室壁奎婁胃昴畢觜参井鬼柳星張翼軫角亢氐房心尾箕斗牛女"
	s12="建除満平定執破危成納開閉"
	s24=["立春","雨水","啓蟄","春分","清明","穀雨","立夏","小満","芒種","夏至","小暑","大暑",
			"立秋","処暑","白露","秋分","寒露","霜降","立冬","小雪","大雪","冬至","小寒","大寒"]
	s7="日月火水木金土"
	s6=["先勝","友引","先負","仏滅","大安",'赤口']
	s9=["一白","二黒","三碧","四緑","五黄",'六白','七赤','八白','九紫']
	d = 0
	list=[]
	def __init__(self, year, month, day):
		self.d=Day.dd3(year, month, day)
		self.list=[f"{Day.s7[self.weekday()]}曜日"]
		wk24 = ""
		if self.ind24()[0]:
			wk24 = f"【{Day.s24[self.ind24()[1]] }】"
		self.list.append(f"{wk24} {Day.s60[0][self.ind10()]}{Day.s60[1][self.ind10(12)]} {Day.s9[self.ind9()]}")
		self.list.append(f"旧暦 {self.oldMonth()[1]}月{self.oldDay()}日")
		self.list.append(f"{Day.s6[self.ind6()]} {Day.s12[self.ind12()]} {Day.s28[self.ind28()]}")
	def year(self):
		return self.d.year
	def month(self):
		return self.d.month
	def day(self):
		return self.d.day
	def weekday(self):
		return (self.d.isoweekday()%7)
	def dd3(year=0, month=0, day=0):
		return datetime.datetime(year, month, day)
	def dd2(ephemday):
		y,m,d,h,n,s=ephemday.tuple()
		return datetime.datetime(y,m,d,h,n,int(s))
	def dd1(d):
		return datetime.datetime(d.year,d.month,d.day)
	def _slon(d0, hours=0):
		d=d0+datetime.timedelta(hours=hours)
		s=ephem.Sun(d)
		eq=ephem.Equatorial(s.ra, s.dec, epoch=d)
		e=ephem.Ecliptic(eq)
		return e.lon*180/math.pi

	def dayslon(d, deg=45):
		s0=Day._slon(d, -9)
		s1=Day._slon(d, 15)
		return (s0%deg)>(s1%deg), int(s1//deg)

	def ind24(self):
		j, i = Day.dayslon(self.d, 15)
		return j, (i+3)%24

	def ind(self, n=10):
		index = self.d.toordinal()+14
		return index%n

	def ind10(self, n=10):
		return self.ind(n)

	def ind60(self):
		return self.ind10(60)

	def ind28(self):
		return self.ind10(28)

	def oldDay(self):
		dy=self.d+datetime.timedelta(hours=15)
		day1 =  Day.dd1(Day.dd2(ephem.previous_new_moon(dy))+datetime.timedelta(hours=9))
		return 1 + (self.d - day1).days

	def oldMonth(self):
		dy=self.d+datetime.timedelta(hours=15)
		day1 =  Day.dd1(Day.dd2(ephem.previous_new_moon(dy))+datetime.timedelta(hours=9))
		day30 =  Day.dd1(Day.dd2(ephem.next_new_moon(dy))+datetime.timedelta(hours=9))
		deg=30
		s0=Day._slon(day1)
		s1=Day._slon(day30)
		return s0//deg==s1//deg, 1+(int(s1//deg)+1)%12

	def ind9(self):
		dy=self.d -datetime.timedelta(days=self.ind60())
		ss = Day.dayslon(dy, 90)
		for i in range(12) :
			dy1=dy -datetime.timedelta(days=30)
			ss1 = Day.dayslon(dy, 90)
			if ss[1] in [1,3] and ss1[1] == ss[1] and  i%2==0:
				break
			ss, dy=ss1, dy1
		dlt = (self.d - dy).days
		return (dlt % 9) if ss[1]==3 else (8 - (dlt % 9))

	def ind6(self):
		d=self.oldDay()-1
		m=self.oldMonth()[1]-1
		return (m%6+d)%6

	def ind12(self):
		s = int(self.ind24()[1] // 2)+2
		b=self.ind60()
		e=self.month()
		index= (b - e + 12)
		if self.month() >s :
			index=index%12+1
		return index%12
	def isHolly(dy):
		d=dy.d
		print(d.month)
		if d.month==1:
			if d.day==1:
				return "元日"
			if d.day==2 and d.isoweekday()==1:
				return "振替休日"
			if d.day > 7 and d.day < 15 and d.isoweekday()==1:
				return "成人の日"
		if d.month==2:
			if d.day==11:
				return "建国記念の日"
			if d.day==12 and d.isoweekday()==1:
				return "振替休日"
			if d.day==23:
				return "天皇誕生日"
			if d.day==24 and d.isoweekday()==1:
				return "振替休日"
		if d.month==4:
			if d.day==29:
				return "昭和の日"
			if d.day==30 and d.isoweekday()==1:
				return "振替休日"
		if d.month==5:
			if d.day==3:
				return "憲法記念日"
			if d.day==4:
				return "みどりの日"
			if d.day==5:
				return "こどもの日"
			if d.day==6 and d.isoweekday() in [1,2,3]:
				return "振替休日"
		if d.month==7:
			if d.day > 7*(3-1) and d.day <= 7*3 and d.isoweekday()==1:
				return "海の日"
		if d.month==8:
			if d.day==11:
				return "山の日"
			if d.day==12 and d.isoweekday()==1:
				return "振替休日"
		if d.month==9:
			if d.day > 7*(3-1) and d.day <= 7*3 and d.isoweekday()==1:
				return "敬老の日"
		if d.month==10:
			if d.day > 7*(2-1) and d.day <= 7*2 and d.isoweekday()==1:
				return "スポーツの日"
		if d.month==11:
			if d.day==3:
				return "文化の日"
			if d.day==4 and d.isoweekday()==1:
				return "振替休日"
			if d.day==23:
				return "勤労感謝の日"
			if d.day==24 and d.isoweekday()==1:
				return "振替休日"
		return ""
class ODay(Day):
	day=0
	list=[]
	def __init__(self, d):
		self.list=[]
		self.day=d
		self.check('節分')
		self.check('八十八夜', -80)
		self.check('二百十日', -210)
		self.check('二百廿日', -220)
		self.check('半夏生', -11,[9])
		self.check('彼岸入', 3,[3,15])
		self.check('彼岸明', -3,[3,15])
		self.check('土用入', 18,[0,6,12,18])
		self.check('土用明', 1,[0,6,12,18])
		self.checkd('盂蘭盆会', 7,15)
		self.checkd('盂蘭盆会', 8,15)
		self.checkd('夏越の祓', 6,30)
		self.checkd('年越の祓', 12,31)
		self.check126('初午')
		self.check104('春の社日')
		self.check104('秋の社日', [15])
		self.check('入梅', 0, [4], 80)
		pass
	def check(self, str, d=1, i24 = [0], deg=15):
		dd=self.day.d+datetime.timedelta(days=d)
		ss=Day.dayslon(dd, deg)
		if ss[0] and ss[1] in [(i+21)%24 for i in i24]:
			self.list.append(str)
	def checkd(self, str, m=1, d=1):
		if self.day.month()==m :
			if self.day.day()==d :
				self.list.append(str)
	def check126(self, str):
		if self.day.ind(12)==6 :
			if self.day.month()==2 :
				if self.day.day()<12 :
					self.list.append(str)
	def check104(self, str, r=[3]):
		if self.day.ind(10)==4 :
			d1=self.day.d+datetime.timedelta(days=5)
			if Day.dayslon(d1, 15)[1] in [(i+21)%24 for i in r]:
				d0=self.day.d+datetime.timedelta(days=-5)
				if not Day.dayslon(d0, 15)[1] in [(i+21)%24 for i in r]:
					self.list.append(str)

class SDay(Day):
	day=0
	ind = -1
	index24 = -1
	list=[]
	def __init__(self, d):
		self.list=[]
		self.day=d
		self.ind = d.ind(60)
		_, self.index24 = d.ind24()
		self.check()
		self.check('乙巳日', (6,))
		self.check('庚申日', (57,))
		self.check('大犯土', (7,))
		self.check('小犯土', (15,))
		self.check('十方暮入り', (21,))
		self.check('天上天一入り', (30,))
		self.check('十方暮終わり', (30,))
		self.check('八専入り', (49,))
		self.check('八専終わり', (60,))
		self.checkT()
		self.check3()
		self.check3c()
		self.check10000()
		self.checkN()
	def check(self, str="甲子日", r=(1,)):
		r0= [r[0]] if r[0] == r[-1] else  list(range(r[0],r[-1]))
		if self.ind in [i-1 for i in r0]:
			self.list.append(str)
	def checkT(self, str="天赦日"):
		i=(int(((self.day.ind24()[1]+21)%24)//6)+1)%4 #4立のいずれか
		index = i*15+ (1 if i % 2 == 0 else 0) #戌寅()、甲午()、戊申()、甲子(1)
		self.check(str, (index,))
	def check3(self, str="三隣亡"):
		if self.ind%12 == [11,2,6][(self.index24//2)%3]:
			self.list.append(str)
	def check3c(self, str="三伏"):
		if self.ind%10==6:
			_,s1=Day.dayslon(self.day.d)
			if s1==3:
				_,s0=Day.dayslon(self.day.d+datetime.timedelta(days=-9))
				if s0==2:
					self.list.append(f"末{str[1]}")
			elif s1==2:
				_,s0=Day.dayslon(self.day.d+datetime.timedelta(days=-29))
				_,s1=Day.dayslon(self.day.d+datetime.timedelta(days=-20))
				if s0==1 and s1==2:
					self.list.append(f"初{str[1]}")
				_,s0=Day.dayslon(self.day.d+datetime.timedelta(days=-39))
				_,s1=Day.dayslon(self.day.d+datetime.timedelta(days=-30))
				if s0==1 and s1==2:
					self.list.append(f"中{str[1]}")
	def check10000(self, str="一粒万倍日"):
		m = (self.index24//2+1)%12
		if self.ind%12 == m or self.ind%12 == (3+m*3) % 12:
			self.list.append(str)
	def checkN(self, str="不成就日"):
		m = (self.day.oldMonth()[1]-1)%6
		if self.day.oldDay() in range([3,2,1,4,5,6][m],32, 8):
			self.list.append(str)

def info(nw=datetime.datetime.today()):
	str=[]
	d=Day(nw.year,nw.month,nw.day)
	str.append(f"本日は{nw.year}年{nw.month}月{nw.day}日 {Day.s7[d.weekday()]}曜日です")
	str.append(f"24節気では{Day.s24[d.ind24()[1]]}")
	str.append(f"干支で換算すると{Day.s60[0][d.ind10()]}{Day.s60[1][d.ind10(12)]}")
	str.append(f"旧暦では{d.oldMonth()[1]}月{d.oldDay()}日にあたります")
	str.append(f"九星は{Day.s9[d.ind9()]}")
	str.append(f"六曜は{Day.s6[d.ind6()]}です")
	str.append(f"12直は{Day.s12[d.ind12()]}")
	str.append(f"28宿は{Day.s28[d.ind28()]}です")

	od=ODay(d)
	if len(od.list)>0:
		str += od.list
	sd=SDay(d)
	if len(sd.list)>0:
		str.append("そのほか雑歴では，")
		str += sd.list
		str.append("にあたります．")
	return ",".join(str)		
	

if __name__=='__main__':
	d=Day(2023,3,21)
	print(d.year())
	print(d.d)
	print(Day.s7[d.weekday()]	)
	print(Day.s24[d.ind24()[1]])
	print(f"{Day.s60[0][d.ind10()]}{Day.s60[1][d.ind10(12)]}")
	print(f"{d.oldMonth()[1]}月{d.oldDay()}日")
	print(f"{Day.s9[d.ind9()]}")
	print(f"{Day.s6[d.ind6()]}")
	print(f"{Day.s12[d.ind12()]}")
	print(f"{Day.s28[d.ind28()]}")

	od=ODay(d)
	print(od.list)

	sd=SDay(d)
	print(sd.list)
