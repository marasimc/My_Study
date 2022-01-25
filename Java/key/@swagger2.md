# @swagger2注解

## 1. 作用：

使用swagger2构建[restful](https://so.csdn.net/so/search?q=restful&spm=1001.2101.3001.7020)接口测试

## 2. 优点：

可以生成文档形式的api并提供给不同的团队

便于自测，也便于领导查阅任务量

无需过多冗余的word文档

## 3. 用法：

① 配置[swagger](https://so.csdn.net/so/search?q=swagger&spm=1001.2101.3001.7020)类

```java
package com.lpy;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import springfox.documentation.service.Contact;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;
 
/**
 * 通过java代码配置
 * @author Richard
 *
 *@Configuration表示是配置文件
 *@EnableSwagger2开启这个配置
 *
 */
@Configuration
@EnableSwagger2
public class Swagger2 {
	/**
	 * @Description:swagger2的配置文件，这里可以配置swagger2的一些基本的内容，比如扫描的包等等，注：让我们的swagger2扫描我们controller
	 */
	@Bean
	public Docket createRestApi() {		
		return new Docket(DocumentationType.SWAGGER_2).apiInfo(apiInfo()).select()
				.apis(RequestHandlerSelectors.basePackage("com.lpy.controller"))
				.paths(PathSelectors.any()).build();
	}
	/**
	 * @Description: 构建 api文档的信息
	 */
	private ApiInfo apiInfo() {
		return new ApiInfoBuilder()
				// 设置页面标题
				.title("使用swagger2构建短视频后端api接口文档")
				// 设置联系人
				.contact(new Contact("Richard", "http://www.lpy.com", "lpy@163.com"))
				// 描述
				.description("欢迎访问短视频接口文档，这里是描述信息")
				// 定义版本号
				.version("1.0").build();
	}
}
```

② 给接口写注解

```java
package com.lpy.controller;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import com.lpy.pojo.Users;
import com.lpy.service.UserService;
import com.lpy.utils.LpyJSONResult;
import com.lpy.utils.MD5Utils;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;

/**
 * @RestController表示以json格式进行传递
 * @RequestBody表示将json对象转换成对象
 * @author Richard
 */
@RestController
@Api(value="用户注册登陆的接口",tags= {"注册和登陆的controller"})
public class RegistLoginController {
	//注入service
	@Autowired
	private UserService userService;
	
	@ApiOperation(value="用户注册",notes="用户注册的接口")
	@PostMapping("/regist")
	public LpyJSONResult regist(@RequestBody Users user) throws Exception {
		//1、判断用户名和密码必须不为空
		if(StringUtils.isBlank(user.getUsername())||StringUtils.isBlank(user.getPassword())) {
			return LpyJSONResult.errorMsg("用户名和密码不能为空");
		}
		//2、判断用户名是否存在
		boolean usernameIsExist=userService.queryUsernameIsExist(user.getUsername());
		//3、保存用户，注册信息
		if(!usernameIsExist) {
			user.setNickname(user.getUsername());//昵称
			user.setPassword(MD5Utils.getMD5Str(user.getPassword()));//密码
			user.setFansCounts(0);//粉丝数
			user.setReceiveLikeCounts(0);//喜欢的数
			user.setFollowCounts(0);//追随数
			userService.saveUser(user);
		}else {
			return LpyJSONResult.errorMsg("用户名已经存在，请换一个再试");
		}	
		return LpyJSONResult.ok();
	}	
}
```

③ 给实体类写注解

```java
package com.lpy.pojo;
 
import javax.persistence.*;
 
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

@ApiModel(value="用户对象",description="这是用户对象")
public class Users {
	@ApiModelProperty(hidden=true)
    @Id
    private String id;
	
    @ApiModelProperty(value="用户名",name="username",example="lpyuser",required=true)
    private String username;
    
    @ApiModelProperty(value="密码",name="password",example="123456",required=true)
    private String password;
    
 
    /**
     * @return id
     */
    public String getId() {
        return id;
    }
 
    /**
     * @param id
     */
    public void setId(String id) {
        this.id = id;
    }
 
    /**
     * @return username
     */
    public String getUsername() {
        return username;
    }
 
}
```





*reference： [ 注解@swagger2的作用sunayn的博客-CSDN博客swagger2作用](https://blog.csdn.net/sunayn/article/details/98510807)*