# 1. SSM

SSM是Spring、SpringMVC、Mybatis的首字母缩写，通过SSM框架可以提高项目开发的效率。

## 1.1 Spring

Spring框架是从实际开发中抽取出来的框架，完成了大量开发中的通用步骤，提高了开发效率。Spring框架将项目中的各个模块代码进行解耦，便于开发过程中对模块进行调整、扩展等操作。

> Spring两大特性：IOC和AOP。

前置概念：Spring作为超级大工厂，负责创建、管理所有Java对象，这些对象称为Bean。

> 1.控制反转（Inverse of Control，IOC），是Spring框架中实现Bean间管理的方法，与依赖注入（Dependency Injection）是不同人提出的同一概念。Spring框架通过配置文件对Bean之间的关系进行管理，实现注入Bean依赖。

正常流程创建一个对象的过程：
①需要调用对象->
②构建对象(class)->
③构建变量(class.property)->初始化参数(get/set)->编写方法->
④使用调用对象。

控制反转方法创建对象的过程：
①需要调用对象->
②调用构造函数->
③构造函数将调用对象的相关参数、初始化、方法完成->注入调用对象的实例化对象中->
④使用调用对象。

正常流程中1-4的步骤在每一次调用对象时都需要重复编写代码，而控制反转只要在第一次配置好构建函数的相关参数，在每次调用相同类的对象时就可自动完成实例化对象，节省了大量的时间，从而提高项目开发效率。

从调用构造函数的角度说，是将依赖的构造函数内容注入到实例化对象中，称之为“依赖注入”。从调用对象的角度说，原先是项目需要什么->开发者去实现什么，变成开发者需要什么->框架反向提供实例化满足对象需求，从而称为“控制反转”。所以“依赖注入”和“控制反转”实际是对同一概念的不同表述。

> 2.面向切面编程（Aspect Orient Programming，AOP），专门用于处理系统中分布于各个模块（不同方法）中的交叉关注问题。AOP是面向对象开发的一种补充，允许开发人员在不改变原来模型的前提下满足新的需求。
> e.g.开发人员可以在不改变原来业务逻辑模型的基础上，进行动态地增加日志、安全或异常处理功能。

## 1.2 SpringMVC

SpringMVC是MVC模式的Web开发框架，MVC是Model、View、Controller的缩写。

通过Controller接收前端请求，Model为对应请求中的实体对象，处理后返回ModelAndView形式的返回值，交给前端显示视图View。在我的理解中SpringMVC是SSM框架中项目的主题部分，通过SpringMVC沟通前端页面与后端数据库等的交互。网上找到的很多SSM项目实例中以jsp文件编写前端页面，但由于SSM框架出现至今已经有一定的时间了，各种技术都有所进步，现在多使用Html5标准。

## 1.3 Mybatis

Mybatis框架用来连接数据库，通过配置文件指定与项目相连的数据库，并规定项目中各方法对应的SQL指令，使得项目能够调用方法执行对数据库内数据的增删改查等操作。

# 2. 项目结构

项目根目录下有src和target两个子目录，src中为项目的各个具体子文件；target是项目运行后自动生成的文件夹，保存项目编译、运行生成的一系列包和类（项目打包也会保存在这个文件夹下）。src目录下一般会有main和test两个子目录，main中为项目主要代码，test中存放测试用的相关代码。

main目录下包含三个部分：

① src/main/java存放的是项目的核心源码；

② src/main/resources存放项目的配置文件；

③ src/main/webapp存放项目WEB端的项目文件（如jsp/html文件等）。

## 2.1 src/main/java源码目录

<img src="Java/image/1.jpg" style="zoom:67%;" />

目录下的包文件里将代码分成了四个部分 ***controller、mapper、model、service***。在SSM框架中注解类发挥极大的作用，通过注解标注了各个部分的功能及依赖关系。

1）controller是框架中的控制类，接收来自前端的请求。

```java
@RequestMapping(value = "/listBooks", method = RequestMethod.GET)
@ResponseBody
public List<Book> getBooksList(HttpServletResponse request) {
    List<Book> list = bookService.list();
    return list;
}
```

注解@RequestMapping设置请求地址、请求的方式（GET/POST）。
注解@ResponseBody设置返回值以json形式响应前端。
关于http请求部分的细节，这又是新的知识点了。

2）service是提供服务层，用来处理前端发来的请求的具体操作。通过调用impl中的方法完成请求的具体内容。

```java
@Override
public List<Book> list() {
    // TODO Auto-generated method stub
    return bookMapper.list();
}
```

通过增加接口的方法将服务层与控制器分离，实现代码解耦。

3）mapper中存放与数据库交互的接口。

mapper.xml文件中保存着mapper接口中Java代码与SQL语言的转换。通过扫描mapper.xml对数据库进行SQL操作。

4）model实体类中与数据库中的表项一一对应，作为数据库表的实体。

```java
@Data
public class Book {
    private int id;
    private String name;
    private String author;
    private String category;
}
```

## 2.2 src/main/resources资源目录

<img src="Java/image/2.jpg" style="zoom:67%;" />

resources目录主要保存SSM框架的各个配置文件。SSM框架通过扫描这些配置文件获取框架的一些配置信息。一般来说会将配置信息放在一个xml文件中，上图将其细分成了多个。
applicationContext.xml为扫描的主要文件，包含了其他配置文件的位置信息，使得项目运行时能找到要扫描的其他配置。
spring-mvc配置了SpringMVC的相关配置。
spring-mybatis和mybatis-config中包含了配置数据库的相关信息。
jdbc.properties保存了数据库的信息，使得驱动能够连接项目与数据库。

## 2.3 src/main/webapp前端目录

webapp目录下有一个WEB-INF目录，其下保存了一个web.xml文件，文件内为网页前端的相关配置信息。其它前端文件也都保存在该目录下。



SSM工程还需要配置Tomcat服务器以启动WEB端服务，而在SpringBoot框架中已经将包含Tomcat在内很多依赖和工具封装在了项目结构里，大大降低了开发人员编写配置文件的繁琐工作，提高了工作效率。因此现在的开发工作舍弃了SSM的繁琐工作，大多以SpringBoot作为开发框架。

# 3. SpringBoot

SpringBoot基于SSM，封装了很多常用的工具和依赖，使得项目开发过程进一步简化。

新建SpringBoot项目可以通过IDEA进行配置然后下载依赖包，也可以从官网[http://start.spring.io](https://link.zhihu.com/?target=http%3A//start.spring.io)配置然后下载项目初始框架的压缩包。

<img src="Java/image/3.jpg" style="zoom:67%;" />

SpringBoot框架的项目目录与SSM框架基本相同，多出来的那些带有mvn字样的文件是用来匹配不同版本Maven的，可以暂时忽略。

src/main/java/{project_package}目录下的一个Application文件，在整个项目中属于项目的入口。当项目打包上传并运行起来后，会从这个指定入口开始运行。其余四个包与之前SSM框架中的四个包对应，通过提供接口的方式，将不同模块进行解耦，减少修改功能时频繁的关联变动。

src/main/resources目录下，使用application.yaml文件作为项目配置文件，与spring-mvc、mybatis相关的配置都存放在这个文件中（取代了原xml配置文件）。

同时在pom.xml文件中，原先又臭又长的大量依赖包被整合到了名为SpringBoot的依赖包中，省去了配置大量依赖的工作。而且SpringBoot中自带整合了Tomcat，无需自己手动下载和配置。

> Spring框架基本实现思路是这样的：
> ①创建数据库。
> ②创建实体类，与数据库中的表项一一对应。
> ③创建接口，同于连接数据库与项目功能。
> ④编写mapper.xml文件（Mybatis）定义关联SQL语言与接口操作。
> ⑤创建Service类，为控制层提供服务。可以单独创建接口实现解耦。
> ⑥创建Controller类，连接页面请求和服务层，处理前端发来的请求。
> ⑦前端页面调用，使用jsp或html标准编写前端页面显示。

实现思路从上往下进行，而实际运行的流程则是从下往上逐级访问各个部分。

通过@RestController注解，可以直接替代之前@Controller @RequestBody两个注解，说明以下部分为控制器并且以json形式返回值。

使用@RequestMapping，其中value设置访问路由值，method设置请求类型。HTTP请求主要以GET和POST两种方式发送请求，前者会将参数放在url中，这种实现方法简单但安全性低；后者将参数保存在请求体中，外界无法通过url直接看到参数内容，相对前者在信息安全性上有所提高，同时可发送的数据量得到了扩增，可以提交表单甚至上传文件。