from src.thingClass import Thing

class OfficeManager(Thing):
  def __init__(self, location=None):
    self.location = None
    self.hasMail = False
    
  def receiveItem(self, item):
    if isinstance(item, Mail):
      self.hasMail = True
    else:
      print("Cannot take item.")
      
  def __repr__(self):
        return f"{self.__class__.__name__}: {self.location}"

class ITStaff(Thing):
  def __init__(self, location=None):
    self.location = None
    self.hasDonuts = False
    
  def receiveItem(self, item):
    if isinstance(item, Donuts):
      self.hasDonuts = True
    else:
      print("Cannot take item.")

  def __repr__(self):
        return f"{self.__class__.__name__}: {self.location}"

class Student(Thing):
  def __init__(self, location=None):
    self.location = None
    self.hasPizza = False

  def receiveItem(self, item):
    if isinstance(item, Pizza):
      self.hasPizza = True
    else:
      print("Cannot take item.")
      
  def __repr__(self):
        return f"{self.__class__.__name__}: {self.location}"
    
  
class Mail(Thing):
  def __init__(self):
    active = True
  
class Donuts(Thing):
  def __init__(self):
    active = True
    
class Pizza(Thing):
  def __init__(self):
    active = True