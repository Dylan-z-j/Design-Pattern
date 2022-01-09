import threading
import time

#这里使用方法__new__来实现单例模式

"""抽象单例"""
class Singleton(object):
    """
    这里要区分 __new__ 和 __init__  -> https://www.jianshu.com/p/08d7956601de
                                   -> https://blog.csdn.net/claroja/article/details/107056407
    __new__ 是类方法，返回一个实例；实例调用 __init__ 方法初始化这个实例的相关参数
    __new__ 方法主要是当你继承一些不可变的 class 时(比如int, str, tuple)， 提供给你一个自
    定义这些类的实例化过程的途径。还有就是实现自定义的 metaclass。
    """
    def __new__(cls, *args, **kw):
        
        # 下面的意思是如果的类没有 _instance 属性，我们才会用__new__新建一个实例
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            # 这样对这个类就新建了 _instance 属性，是一个实例
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance
    
"""总线"""
class Bus(Singleton):
    lock = threading.RLock()
    def sendData(self,data):
        # -> https://blog.csdn.net/cumtb2002/article/details/107796460
        # -> https://blog.csdn.net/XiaoYi_Eric/article/details/82153925
        # -> https://www.jianshu.com/p/c1015f5ffa74
        self.lock.acquire() 
        time.sleep(3)
        print("Sending Signal Data...", data)
        self.lock.release()
        
"""线程对象，为更加说明单例的含义，这里将Bus对象实例化写在了run里"""
class VisitEntity(threading.Thread):
    my_bus = ""
    name = ""
    def getName(self):
        return self.name
    def setName(self, name):
        self.name = name
    def run(self):
        self.my_bus=Bus()
        self.my_bus.sendData(self.name)

if  __name__=="__main__":
    for i in range(3):
        print("Entity %d begin to run..." % i)
        my_entity=VisitEntity()
        my_entity.setName("Entity_" + str(i))
        my_entity.start()
