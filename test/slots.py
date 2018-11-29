from types import MethodType
class Student(object):
    pass

s=Student()
s.name='Micheal'
print(s.name)

def set_age(self,age):
    self.age=age
s.set_age=MethodType(set_age,s)
s.set_age(25)
print(s.age)

s2=Student()

def set_score(self,score):
    self.score=score
Student.set_score=set_score
s.set_score(100)
s2.set_score(120)
print(s.score)
print(s2.score)
