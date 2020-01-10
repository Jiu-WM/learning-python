

```python
class person:
    def set_name(self, name):
        self.name = name
        
    def get_name(self):
        return self.name
    
    def greet(self):
        print ("hello, I'm {}.".format(self.name))

zs= person()
zs.set_name('zhang san')
zs.greet()
```

    hello, I'm zhang san.
    


```python
class person:
    count=0
    
    def __init__(self, name=None):
        self.name = name
        person.count +=1
        print('total number of person: {}'.format(person.count))
        
    def set_name(self, name):
        self.name = name
        
    def get_name(self):
        return self.name
    
    def greet(self):
        print ("hello, I'm {}.".format(self.name))


zs = person ('zhang san')
zs.greet()

```

    total number of person: 1
    hello, I'm zhang san.
    


```python
# 不想把类的一些信息暴露在外面时，可以
class person:
    count=0
    
    def __init__(self, name=None):
       # set_name (name)
        self.__name = name    #加下划线隐藏name
        person.count +=1
        print('total number of person: {}'.format(person.count))
        
    def set_name(self, name):
        
        # assert (isinstance (name, str))    #强制字符串
        if isinstance (name, str):
            self.__name = name
        else:
            print ('not a valid name')
        
    def get_name(self):
        return self.__name
    
    def greet(self):
        print ("hello, I'm {}.".format(self.__name))
        
ls= person()
ls.set_name (1)
```

    total number of person: 1
    not a valid name
    


```python
# doc string, type hint 起注释作用的
class person:
    '''this class can be used to represent a person ''' 
    

    
    def __init__(self, name:str=None):
       # set_name (name)
        self.__name = name    #加下划线隐藏name
      
   
        
    def set_name(self, name:str):
        '''set the name of person, name must be a str.'''
        
        # assert (isinstance (name, str))    #强制字符串
        if isinstance (name, str):
            self.__name = name
        else:
            print ('not a valid name')
        
    def get_name(self):
        return self.__name
    
    def greet(self):
        print ("hello, I'm {}.".format(self.__name))
        

```


```python

```


```python
help(person())
```

    total number of person: 4
    Help on person in module __main__ object:
    
    class person(builtins.object)
     |  person(name=None)
     |  
     |  Methods defined here:
     |  
     |  __init__(self, name=None)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  get_name(self)
     |  
     |  greet(self)
     |  
     |  set_name(self, name)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  count = 4
    
    


```python
1 +2 
```




    3




```python
'a'+'b'
```




    'ab'




```python
# 多态的
print ('hello'.count('e'))
```

    1
    


```python
print([1,2,3,'e','e',4].count('e'))
```

    2
    


```python
my_list = ['hello',[1,2,3,'e','e',4]]
for item in my_list:
    print(item.count ('e'))
```

    1
    2
    


```python
class cat:
    def meow(self):
        print ('meow...')
        
class dog:
    def wang(self):
        print('wang,wang...')
        
pets = list()
pets.append (cat())
pets.append(dog())

for item in pets:
    if isinstance (item, cat):
        item.meow()
    elif isinstance(item, dog):
        item.wang()
    else :
        pass
```

    meow...
    wang,wang...
    


```python
# 面向对象的多态：用同一个接口解决不同的问题，比如阿猫阿狗吃饭，阿猫阿狗叫
class cat:
    def talk(self):
        print ('meow...')
        
class dog:
    def talk(self):
        print('wang,wang...')
        
pets = [cat(),dog(),cat()]


for item in pets:
    item.talk()
   
```

    meow...
    wang,wang...
    meow...
    


```python
# 简单的操作符的多态
def add(a,b):
    return a+b

a=1
b=2
print(add (a,b))
x,y = 'a','b'
print(add(x,y))
```

    3
    ab
    


```python
# 继承---student 是person的子类，它可以调用父类的函数
class student (person):
    
    def __init__(self,name=None):
        person.__greet(self,name)
        self.__score = 60
    def set_score(self,  score):
        self.__score= score
        
    def get_score(self):
        return self.__score
    
    def show_score (self):
        print ('my score is :{}'.format(self.__score))
        
    def greet (self):
        person.greet(self)   # 调用person类里面的greet
        self.show_score()
        
zs= student()
zs.set_name('zhang san')
zs.set_score(100)
zs.greet()
zs.show_score()
```

    total number of person: 6
    hello, I'm zhang san.
    my score is :100
    


```python
people = list()
zs= person('zhang san')
ls= student ('li si')
ls.set_score(100)
people.append(zs)
people.append(ls)

for p in people:
    p.greet()
```

    total number of person: 7
    total number of person: 8
    hello, I'm zhang san.
    hello, I'm li si.
    


```python
#子类的对象一定是父类的对象
isinstance (ls, student)
```




    True




```python
isinstance(zs, person)
```




    True




```python
isinstance(zs, student)
```




    False




```python
# 过滤器
class Filter:
    def __init__(self):
        self.blocked = []
        
    def filter(self , sequence):
        return [ x for x in sequence if x not in self.blocked]
    
class spamfilter(Filter):
    def __init__(self):
        self.blocked = ['spam']
        
f = Filter()
f.filter([1,2,3])
```




    [1, 2, 3]




```python
sf= spamfilter()
sf.filter(['spam','spam','bacon','eggs','sausage','spam'])
```




    ['bacon', 'eggs', 'sausage']




```python
# 继承两个父类，但是结构比较糟糕

class caculator:
    def caculate (self, expression):
        self.value = eval(expression)
        
class talker:
    def talk(self):
        print ('my value is:',self.value)
        
class talkingcaculator(caculator,talker):
    pass

tc = talkingcaculator()
tc.caculate('1+2+3')
tc.talk()
```

    my value is: 6
    


```python
class caculator:
    def caculate (self, expression):
        return eval(expression)
        
class talker:
    def talk(self,value):
        print ('my value is:',value)
        
class talkingcaculator(caculator,talker):
    pass

tc = talkingcaculator()
result= tc.caculate('1+2+3')
tc.talk (result)
```

    my value is: 6
    


```python
class caculator:
    def caculate (self, expression):
        return eval(expression)
        
class talker:
    def talk(self,value):
        print ('my value is:',value)
        
class talkingcaculator:
    def __init__(self):
        self.__caculator =caculator()
        self.__talker = talker()
        self.__value= None
        
    def caculate(self, expression):
        self.__value = self.__cacultor.caculate(expression)
        
    def talk(self):
        self.__talker.talk(self.__value)

tc = talkingcaculator()
tc.caculate ('1+2+3')
tc.talk()
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-71-3876c4edad63> in <module>
         20 
         21 tc = talkingcaculator()
    ---> 22 tc.caculate ('1+2+3')
         23 tc.talk()
    

    <ipython-input-71-3876c4edad63> in caculate(self, expression)
         14 
         15     def caculate(self, expression):
    ---> 16         self.__value = self.__cacultor.caculate(expression)
         17 
         18     def talk(self):
    

    AttributeError: 'talkingcaculator' object has no attribute '_talkingcaculator__cacultor'
    
    
    class Calculator:
    def calculate(self, expression):
        return eval(expression)

```python        
class Talker:
    def talk(self, value):
        print('My value is:', value)
        
class TalkingCalculator:
    def __init__(self):
        self.__calculator = Calculator()
        self.__talker = Talker()
        self.__value = None
        
    def calculate(self, expression):
        self.__value = self.__calculator.calculate(expression)
    
    def talk(self):
        self.__talker.talk(self.__value)
    

tc = TalkingCalculator()
tc.calculate('1 + 2 + 3')
tc.talk()

```
