 spring中，@Resource和@Autowired都是做bean的注入时使用。使用过程中，有时候@Resource 和 @Autowired可以替换使用；有时，则不可以。

    共同点：
     @Resource和@Autowired都可以作为注入属性的修饰，在接口仅有单一实现类时，两个注解的修饰效果相同，可以互相替换，不影响使用。
    
    不同点：
     @Resource是Java自己的注解，@Resource有两个属性是比较重要的，分是name和type；Spring将@Resource注解的name属性解析为bean的名字，而type属性则解析为bean的类型。所以如果使用name属性，则使用byName的自动注入策略，而使用type属性时则使用byType自动注入策略。如果既不指定name也不指定type属性，这时将通过反射机制使用byName自动注入策略。
    @Autowired是spring的注解，是spring2.5版本引入的，Autowired只根据type进行注入，不会去匹配name。如果涉及到type无法辨别注入对象时，那需要依赖@Qualifier或@Primary注解一起来修饰。


 **例子：**

```java
package com.example.annotation.service;
 
/**
 * service接口定义
 * @author Administrator
 */
public interface Human {
	
	/**
	 * 跑马拉松
	 * @return
	 */
	String runMarathon();
}
 

package com.example.annotation.service.impl;
 
import com.example.annotation.service.Human;
import org.springframework.stereotype.Service;
 
/**
 * service接口第一实现类
 * @author Administrator
 */
@Service
public class Man implements Human {
 
	public String runMarathon() {
		return "A man run marathon";
	}
}
 

package com.example.annotation.controller;
 
import javax.annotation.Resource;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.example.annotation.service.Human;
 
/**
 * controller层实现类
 * @author Administrator
 */
@RestController
@RequestMapping("/an")
public class HumanController {
 
	@Resource
	private Human human;
	
	@RequestMapping("/run")
	public String runMarathon() {
		return human.runMarathon();
	}
}
```

1. 改动一：

将HumanController.java 类中的注解替换为@Autowired，再次启动，可以正常访问。



2. 改动二：

再增加一个实现类Woman.java：

```java
package com.example.annotation.service.impl;
 
import com.example.annotation.service.Human;
import org.springframework.stereotype.Service;
 
/**
 * service接口第二实现类
 * @author Administrator
 */
@Service
public class Woman implements Human {
 
	public String runMarathon() {
		return "An woman run marathon";
	}
}
```

启动springboot，控制台会报错（expected single matching bean but found 2: man,woman，被期望的单一结果被匹配到两个结果man和woman）-> 我们需要借助*@Resource注解的name属性或@Qualifier来确定一个合格的实现类* 。需要将代码修改为如下：

```java
@Resource(name="woman")
private Human human;

//或

@Resource
@Qualifier("woman")
private Human human;
```

3. 改动三：

在改动二的基础上，将注解替换为@Autowired，启动报错。

解决方案：使用@Primary注解，在有多个实现bean时告诉spring首先@Primary修饰的那个；或者使用@Qualifier来标注需要注入的类。

@Qualifier修改方式与改动二的相同，依然是修改HumanController.java 中间注入的Human上面，这里不再复述

@Primary是修饰实现类的，告诉spring，如果有多个实现类时，优先注入被@Primary注解修饰的那个。这里，我们希望注入Man.java ，那么修改Man.java为

```java
package com.example.annotation.service.impl;
 
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Service;
import com.example.annotation.service.Human;
 
/**
 * service接口第一实现类
 * @author Administrator
 */
@Service
@Primary
public class Man implements Human {
 
	public String runMarathon() {
		return "A man run marathon";
	}
}
```





***reference：**https://blog.csdn.net/magi1201/article/details/82590106*