# String vs StringBuffer

java中有三个类可以对字符进行操作：

1. Character 是进行单个字符操作的类。
2. String 对一串字符进行操作的不可变类。
3. StringBuffer 也是对一串字符进行操作，但是可变类。



## 1. String与StringBuffer类的区别

```
StringBuffer对象的内容可以修改；而String对象一旦产生后就不可以被修改，重新赋值，其实是两个对象。

String是对象，不是原始类型；为不可变对象，一旦被创建，就不能修改其值。

对于已经存在的String对象的修改，实际上是重新创建一个新的对象，然后把新的值保存进去。

String是final类，不能被继承。

StringBuffer是一个可变对象，当对它修改的时候，不会像String那样重新建立对象，它只能通过构造函数来建立。对象被创立后，会分配内存空间，并初始保存一个null。向StringBuffer中赋值的时候，可以通过它的append方法：obj.append("hello");

字符串连接操作中StringBuffer的效率比String高。

如果程序中需要对字符串进行频繁的修改连接操作的话，使用StringBuffer性能会更高。

在String类中，没有用来改变已有字符串中的某个字符的方法，由于不能改变一个java字符串中的某个单独字符，所以在JDK文档中称String类的对象是不可改变的。

然而，不可变的字符串具有一个很大的优点：编译器可以把字符串设置为共享的。

StringBuffer是线程安全的，在多线程程序中也可以很方便的进行使用，但是程序执行效率相对来说就要稍微慢一些。

StringBuffer类中的方法偏重于对字符串的变化，例如追加、插入和删除等，这个也是StringBuffer和String类的主要区别。
```

## 2. String与StringBuffer连接字符串比较

```
String str = new String("Hello World");str += "hello world"; 

此字符串连接的处理过程：
（1）建立一个StringBuffer；
（2）调用append()方法；
（3）最后StringBuffer调用toString()给String重新赋值
（4）这样看来，String的连接操作，比StringBuffer多了一些操作，效率上就会打折扣。
（5）并且，由于String是不可变对象，每次重新赋值都会重新创建新的对象，那么原来的对象就没用了，就要被垃圾回收，也影响性能。

StringBuffer类属于一种辅助类，可预先分配指定长度的内存块建立一个字符串缓冲区。这样使用StringBuffer类的append方法追加字符，比String使用“+”操作符添加字符到一个已经存在的字符串后面有效率的多。

使用“+”操作符每一次将字符添加到一个字符串中去时，字符串对象都需要寻找一个新的内存空间来容纳更大的字符串，这无疑是一个非常消耗时间的操作。添加多个字符就意味着要一次又一次的的对字符串重新分配内存。使用StringBuffer就避免了这个问题。
```

