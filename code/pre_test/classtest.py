from character import Student,Teacher,getClazz


t1 = Teacher("T1",None,0.1,10)
t2 = Teacher("T2",None,0.1,10)
t3 = Teacher("T3",None,0.1,10)
t4 = Teacher("T4",None,0.1,10)

s1 = Student("S1",None,0.1,10)
s2 = Student("S2",None,0.1,10)

c = getClazz()

c["T1"].self_intro()
c["T2"].self_intro()