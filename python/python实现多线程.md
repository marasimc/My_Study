# python实现多线程的方法

## 1. 创建线程：

方法1 通过threading.Thread进行创建多线程：

```python
import threading
import time

def target():
    ### 待执行的程序代码
    print('hh')
    time.sleep(5)
    

if __name__=='__main__':
    all_thread = []
    for i in range(3):
        t = threading.Thread(target=target)
        all_thread.append(t)
        t.start()

    # 若主程序不需要等待所有子线程结束，则到这里就Ok了

    # 若想要让主程序等待所有线程结束，则再加上下面的代码
    for t in all_thread:
        t.join()   # join是阻塞当前线程(此处的当前线程时主线程) 主线程直到所有线程结束之后才运行后面的代码
        
    print('ok')
```

方法2 继承threading.Thread定义子类创建多线程：

```python
import threading
import time

class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):     
        # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        time.sleep(5)
        print("Exiting " + self.name)


if __name__=='__main__':
    # 创建新线程
    all_thread = []
    for i in range(3):
        t = myThread("Thread-" + str(i))
        all_thread.append(t)
        t.start()

    # 若主程序不需要等待所有子线程结束，则到这里就Ok了

    # 若想要让主程序等待所有线程结束，则再加上下面的代码
    for t in all_thread:
        t.join()   # join是阻塞当前线程(此处的当前线程时主线程) 主线程直到Thread-1结束之后才结束
        
    print('ok')
```

## 2. 线程间同步

线程间同步的方式：锁机制，信号量，条件判断，同步队列

### 2.1 锁机制

```python
import threading
import time

threadLock = threading.Lock()

def target(name):
    # 获得锁，成功获得锁定后返回True
    # 可选的timeout参数不填时将一直阻塞直到获得锁定
    # 否则超时后将返回False
    threadLock.acquire(timeout=4)
    
    ### 待执行的程序代码
    print('start:', name)
    time.sleep(5)
    
    # 释放锁
    threadLock.release()
    
    

if __name__=='__main__':
    all_thread = []
    for i in range(3):
        t = threading.Thread(target=target, args=('name'+str(i),))
        all_thread.append(t)
        t.start()

    # 若主程序不需要等待所有子线程结束，则到这里就Ok了

    # 若想要让主程序等待所有线程结束，则再加上下面的代码
    for t in all_thread:
        t.join()   # join是阻塞当前线程(此处的当前线程时主线程) 主线程直到所有线程结束之后才运行后面的代码
        
    print('ok')
```

### 2.2 信号量

```python

```

### 2.3 条件判断

```python

```

### 2.4 同步队列

```html
Python的queue模块中提供了同步的、线程安全的队列类，包括FIFO（先入先出)队列Queue，LIFO（后入先出）队列LifoQueue，和优先级队列PriorityQueue。这些队列都实现了锁原语，能够在多线程中直接使用。可以使用队列来实现线程间的同步。

queue模块中的常用方法:

queue.qsize() 返回队列的大小
queue.empty() 如果队列为空，返回True,反之False
queue.full() 如果队列满了，返回True,反之False
queue.full 与 maxsize 大小对应
queue.get([block[, timeout]])获取队列，timeout等待时间
queue.get_nowait() 相当Queue.get(False)
queue.put(item) 写入队列，timeout等待时间
queue.put_nowait(item) 相当Queue.put(item, False)
queue.task_done() 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
queue.join() 实际上意味着等到队列为空，再执行别的操作
```



```python
''' 例子1. 先往队列中添加任务，然后由线程取出任务并进行处理 '''
import threading
import time
import queue


def target(name):
    #循环，保证接着跑下一个任务
    while True:
        # 队列为空则退出线程
        if queue.empty():
            break
        
        # 获取一个队列数据
        foo = queue.get()
        
         ### 待执行的程序代码
        print('start:', name, 'task:', foo)
        time.sleep(5)
        
        # 任务完成
        queue.task_done()
            
    

if __name__=='__main__':
    # 队列
    queue = queue.Queue()
    # 加入100个任务队列
    for i in range(10):
        queue.put(i)
        
    # 开3个线程
    for i in range(3):
        t = threading.Thread(target=target, args=('name'+str(i),))
        t.start()

        
    # 所有线程执行完毕后关闭，相当于等所有线程执行完毕后再执行后面的操作
    queue.join()
        
    print('ok')
```

```python
''' 例子2. 借助线程锁动态往队列添加任务与取出任务'''
import threading
import time
import queue

exitFlag = 0
queueLock = threading.Lock()

def target(name):
    #循环，保证接着跑下一个任务
    while not exitFlag:
        queueLock.acquire()
        # 队列为空则退出线程
        if queue.empty():
            queueLock.release()
        else:
            # 获取一个队列数据
            foo = queue.get()
            queueLock.release()
            
            ### 待执行的程序代码
            print('start:', name, 'task:', foo)
            time.sleep(1)
            
            # # 任务完成
            # queue.task_done()
        
        time.sleep(1)      # 等待1s，产生任务
            


if __name__=='__main__':
    # 队列
    queue = queue.Queue(maxsize=10)
    # 加入10个任务队列
    queueLock.acquire()
    for i in range(10):
        queue.put(i)
    queueLock.release()
        
    # 开3个线程
    all_thread = []
    for i in range(5):
        t = threading.Thread(target=target, args=('name'+str(i),))
        all_thread.append(t)
        t.start()

    # 再加入10个任务队列
    queueLock.acquire()
    for i in range(10):
        while True:
            if not queue.full():
                break
            else:
                queueLock.release()
                time.sleep(1)
                queueLock.acquire()
        queue.put(i)
    queueLock.release()
    
    # 等待队列清空
    while not queue.empty():
        pass

    exitFlag = 1    # 通知线程已经把所有任务添加完毕
    
    # 所有线程执行完毕后关闭，相当于等所有线程执行完毕后再执行后面的操作
    for t in all_thread:
        t.join()
        
    print('ok')
```

## 3. 线程池

 一个线程的运行时间可以分为3部分：线程的启动时间、线程体的运行时间和线程的销毁时间

如果提交给线程的任务是执行时间较短，而且执行次数极其频繁，那么服务器将处于不停的创建线程，销毁线程的状态 --------- 解决方案—— 线程池

```python
import queue
import threading
import time

# 声明线程池管理类
class WorkManager(object):
    def __init__(self, work_num=1000, thread_num=2):
        self.work_queue = queue.Queue()  # 任务队列
        self.threads = []  # 线程池
        self.__init_work_queue(work_num)  # 初始化任务队列，添加任务
        self.__init_thread_pool(thread_num) # 初始化线程池，创建线程

    """
        初始化线程池
    """
    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            # 创建工作线程(线程池中的对象)
            self.threads.append(Work(self.work_queue))


    """
        初始化工作队列
    """
    def __init_work_queue(self, jobs_num):
        for i in range(jobs_num):
            self.add_job(do_job, i)

    """
        添加一项工作入队
    """
    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))  # 任务入队，Queue内部实现了同步机制

    """
        等待所有线程运行完毕
    """
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive(): item.join()



class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        # 死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                do, args = self.work_queue.get(block=False)  # 任务异步出队，Queue内部实现了同步机制
                do(args)
                self.work_queue.task_done()  # 通知系统任务完成
            except:
                break

# 具体要做的任务
def do_job(args):
    time.sleep(0.1)  # 模拟处理时间
    print(threading.current_thread())
    print(list(args))


if __name__ == '__main__':
    start = time.time()
    work_manager = WorkManager(100, 10)  # 或者work_manager =  WorkManager(10000, 20)
    work_manager.wait_allcomplete()
    end = time.time()
    print("cost all time: %s" % (end - start))
```

## 4. 线程池生产者消费者模式

```python
from multiprocessing import Manager,Pool, cpu_count
import time

def print_error(value):
    print("线程池出错,出错原因为: ", value)

def put_into_pool(data, queue):
    '''
        往线程池中添加任务
    '''
    queue.put_nowait(data)
    

def get_from_pool(queue):
    '''
        往线程池中取出任务
    '''
    count=0
    while True:
        try:
            data = queue.get_nowait()
            
            print('get', data)
            # 一些业务处理代码
            queue.task_done()  # 标记该数据已从队列中取出
        except:
            print("queue is empty wait for a while")
            time.sleep(0.4)
            count+=1
            
        if count==2:
            break


if __name__=='__main__':
    #初始化队列以及线程池
    queue=Manager().Queue()
    put_thread_pool=Pool()
    get_thread_pool=Pool()
    
    for i in range(5):
        data = {'num': i}
        put_thread_pool.apply_async(put_into_pool, args=(data, queue,), error_callback=print_error)

    get_thread_pool.apply_async(get_from_pool, args=(queue,), error_callback=print_error)
    
    put_thread_pool.close()
    get_thread_pool.close()
    put_thread_pool.join()
    get_thread_pool.join()
```

## 5. 协程

```python
import threading
import asyncio

@asyncio.coroutine
def hello():
    print('Hello world! (%s)' % threading.currentThread())
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())

loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

'''
 @asyncio.coroutine把一个generator标记为coroutine类型，然后，我们就把这个coroutine扔到EventLoop中执行。 
 hello()会首先打印出Hello world!，然后，yield from语法可以让我们方便地调用另一个generator。由于asyncio.sleep()也是一个coroutine，所以线程不会等待asyncio.sleep()，而是直接中断并执行下一个消息循环。当asyncio.sleep()返回时，线程就可以从yield from拿到返回值（此处是None），然后接着执行下一行语句。

​ 把asyncio.sleep(1)看成是一个耗时1秒的IO操作，在此期间，主线程并未等待，而是去执行EventLoop中其他可以执行的coroutine了，因此可以实现并发执行。
'''
```

