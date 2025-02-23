class A:
   def __init__(self):
      self.type = "letter"

   def get_classname(self):
      return type(self).__name__

class B(A):
  def __init__(self):
    self.name = "B"

aa = A()
bb = B()
print(aa.get_classname()=="AA")
print(bb.get_classname()=="A")