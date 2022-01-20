# 1. 传统DAO层开发方式

在传统 web 开发中，我们首先需要定义 Dao 接口，然后定义 DaoIImpl 类实现接口。

```java
/** 定义 UserDao 接口 **/
public interface UserDao {
    // 1、 根据用户ID查询用户信息
    public User findUserById(int id) throws IOException;

    // 2、 根据用户ID和用户名称查询用户信息
    public User findByUserIdAndName(User user) throws IOException;
}


/** 定义 UserDao 接口的实现类 UserDaoImpl **/
public class UserDaoImpl implements UserDao {
    // 依赖注入，将工程在外面创建
    private SqlSessionFactory sqlSessionFactory;
    
    public UserDaoImpl(SqlSessionFactory sqlSessionFactory) {//将外面创建的工厂传递进来（以后spring）
        this.sqlSessionFactory = sqlSessionFactory;
    }

    @Override
    public User findUserById(int id) throws IOException {
        // 创建SqlSession
        SqlSession sqlSession = sqlSessionFactory.openSession();
        // 调用SqlSession的增删改查方法
        User user = sqlSession.selectOne("userMapper.findByUserId", id);
        System.out.println(user);
        // 关闭资源
        sqlSession.close();
        return user;
    }

    @Override
    public User findByUserIdAndName(User user)  throws IOException {
        // 创建SqlSession
        SqlSession sqlSession = sqlSessionFactory.openSession();
        // 调用SqlSession的增删改查方法
        User user= sqlSession.selectOne("userMapper.findByIdAndName", user);
        System.out.println(user);
        // 关闭资源
        sqlSession.close();
        return list;
    }
}


/** 模拟业务层调用 **/
public static void main(String [] args) throws Exception {
   InputStream inputStream = Resources.getResourceAsStream(resource);
   // 创建SqlSessionFactory
   SqlSessionFactory  sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
   UserDao dao = new UserDaoImpl(sqlSessionFactory);
   User user = dao.findUserById(1);
   System.out.println(user);
}
```



# 2. 代理DAO层开发方式

分析第一种方式的代码会发现有大量的重复的模板代码。为了简化开发，[Mybatis](https://so.csdn.net/so/search?q=Mybatis&spm=1001.2101.3001.7020) 提供了一种代理开发的方式，这种方式是项目开发中 Mybatis 实现 Dao 层的主流。

**代理开发方式只需要程序员编写Mapper 接口（相当于Dao 接口），然后由 Mybatis 框架根据接口定义创建接口的动态代理对象，代理对象的方法体同上边Dao接口实现类方法。** 代理开发方式使用的是动态代理的 JDK 代码实现的。

Mapper 接口需要遵循以下规范：

- 映射文件中的`mapper`标签的`namespace`属性与 mapper 接口的全限定名相同
- 映射文件中的每条映射语句中`id`的属性值与 mapper 接口中方法名相同
- 映射文件中的每条映射语句的`parameterType`属性与 mapper 接口中方法的形参相同
- 映射文件中的每条映射语句的`resultType`属性与 mapper 接口中方法的返回值类型相同



如果 Mapper 接口已经遵循上述规范，那么不需要创建 Dao 层的实现类了，可以直接进行使用：

```java
public static void main(String [] args) throws Exception {
   InputStream inputStream = Resources.getResourceAsStream("SqlMapConfig.xml");
   // 创建SqlSessionFactory
   SqlSessionFactory  sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
   // 创建SqlSession
   SqlSession sqlSession = sqlSessionFactory.openSession();
   UserDao dao = sqlSession.getMapper(UserDao.class);
   User user = dao.findByUserId(1);
   System.out.println(user);
}
```

## 2.1 ***mybatis的xml的映射配置文件***

在mapper包中，定义接口和xml映射配置，接口要和xml映射配置文件名字一样，一 一对应。

在mybatis的xml配置中，分别有<insert></insert>、<delete></delete>、<update></update>、<select></select>四组标签对应增删改查的操作，然后在标签中写sql语句。这些标签都有id属性，这个属性对应的是接口中的方法名。

### 2.1.1 ***新增（insert）***

在执行操作完成之后，返回受影响的条数。

① 接口方法：（ @Param("u")就是给参数取别名，在xml映射配置中我们才能方便去使用这个参数，使用方法就是： 别名.属性）

```java
//@Param("u") 给参数定义个别名
int addUserBean(@Param("u") UserBean user);
```

② xml映射配置：

```xml
<!-- id就是接口的那些方法，实现哪个方法，id就是这个方法的方法名-->
<!-- useGeneratedKeys表示是否去获取自增id  可不写（仅对 insert 和 update 有用）-->
<!-- keyProperty表示获取的自增id保存在哪里 可不写（仅对 insert 和 update 有用）-->
<!-- parameterType表示如果传入的参数只有一个时，那么用它来指定传入参数的类型，
如果在传入参数中加入@Param()注解， 可不写-->
<insert id="addUserBean" useGeneratedKeys="true" keyProperty="u.id"
	parameterType="UserBean">
	insert into
	t_user(login_name,user_name,user_pwd,age,gender,birthday,create_time)
	values
	(#{u.loginName},#{u.userName},#{u.password},#{u.age},#{u.gender},#{u.birthday},now());
</insert>
<!-- #{ }的作用就是取值的意思，传入对象就用#{别名.属性名}；像对象这种层层结构的，
比如Map就有这种结构，就可以这样去取值；如果没有这种结构，比如字符串这种单一类型，直接用#{别名} -->
<!-- #{ }和${ }的作用都是取值，区别就是#{ }要进行预编译，而${ }直接编译-->
```

### 2.1.2 ***修改和删除（update、delete）***

修改和删除最常用的属性也就是：id和parameterType，但是parameterType一般情况下不用指定，只要在接口方法的参数上加上@Param()注解就可以了，多个参数多个注解区分就是了。

### 2.1.3 ***查询（select）***

查询与前面的增删改操作略有不同。

① 接口方法：（ @Param("pwd")就是给参数取别名，在xml映射配置中我们才能方便去使用这个参数，使用方法就是： 别名.属性）

```java
UserBean findUserBeanByLoginNameAndPwd(@Param("loginName")String loginName,@Param("pwd")String pwd);
```

② xml映射配置：

```xml
<!-- <resultMap>标签，定义结果集中数据列与对象中的属性之间的映射关系 orm -->
<!-- <resultMap>标签的id属性是查询标签<select>的resultMap属性要用的，type是要映射的对象类型-->
<!-- <id>标签用来指定对象的id和表的id的映射，<result>标签就是对象其他属性与表中其他列的映射；
property指的是对象的属性，column指的是对应的表的列名，javaType指的是对象属性的类型-->
<resultMap type="UserBean" id="userMap">
	<id property="id" column="id" javaType="java.lang.Integer" />
	<result property="loginName" column="login_name" javaType="java.lang.String" />
	<result property="userName" column="user_name" javaType="java.lang.String" />
	<result property="password" column="user_pwd" javaType="string" />
	<result property="age" column="age" javaType="int" />
	<result property="gender" column="gender" javaType="int" />
	<result property="birthday" column="birthday" javaType="java.util.Date" />
	<result property="createTime" column="create_time" javaType="java.util.Date" />
</resultMap>
 
<!-- 定义结果查询方法，有两种接收结果方式：resultMap和resultType-->
<!-- 使用resultMap="userMap"就要用到上面的映射关系；如果用的是resultType的话，
传入的如果是对象，那么就要给sql语句的每列就要用as取别名，和对象的属性名保持一致；如果是Map，
取别名就以别名为键，不取别名默认以列名作为键名；如果是其他数据类型，比如本数据类型这些，那么查询的返回结果必须也是与之对应的单一结果，也就是一个结果-->
<select id="findUserBeanByLoginNameAndPwd" resultType="UserBean">
		select
		id,login_name as loginName,user_name as userName,age,gender,user_pwd
		as password,birthday,create_time as createTime from t_user
		where login_name = #{loginName} and user_pwd = #{pwd}
</select>
```

### 2.1.4 结果集映射

<resultMap>标签，定义结果集中数据列与对象中的属性之间的映射关系 orm
<resultMap>标签的id属性是查询标签<select>的resultMap属性要用的，type是要和表要映射的对象类型
<id>标签用来指定对象的id和表的id的映射，<result>标签就是对象其他属性与表中其他列的映射
property指的是对象的属性，column指的是对应的标的列名，javaType指的是对象属性的类型

### 2.1.5 查询标签

"<select>"标签用于结果查询，查询了结果之后，我们总得有东西来装结果吧。select标签提供了两种接收结果方式：resultMap和resultType

1、resultMap接受结果，就要定义结果映射，把查询的列也就是from前面需查询的列和对象的属性对应起来，就要用到上面的结果集映射关系。比如：resultMap="userMap"，就要用<resultMap>标签写结果集映射关系。

2、如果用的是resultType的话，传入的如果是对象，那么就要给sql语句的每列就要用as取别名，和对象的属性名保持一致；如果是Map，为列取了别名的就以别名为键，没取别名默认以列名作为键名。resultType可以是对象、Map、基本数据类型，引用数据类型。如果是后面两种的数据类型，把么查询结果返回只能是一个值，才能接收到。比如，只有一个数值返回，那么可以用int这些；只有一个字符串返回，可以用String；只有一个时间返回，可以用Data，最好写出类型的全路径，有些类型可以省略全路径，但是写上都不会报错。

### 2.1.5 示例

AddressMapper

```java
package com.xq.tmall.dao;

import com.xq.tmall.entity.Address;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface AddressMapper {
    Integer insertOne(@Param("address") Address address);
    Integer updateOne(@Param("address") Address address);

    List<Address> select(@Param("address_name") String address_name, @Param("address_regionId") String address_regionId);
    Address selectOne(@Param("address_areaId") String address_areaId);
    List<Address> selectRoot();
}
```

AddressMapper.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "mybatis-3-mapper.dtd">
<mapper namespace="com.xq.tmall.dao.AddressMapper">
    <resultMap id="address" type="com.xq.tmall.entity.Address">
        <id property="address_areaId" column="address_areaId"/>
        <result property="address_name" column="address_name"/>
        <association property="address_regionId" javaType="com.xq.tmall.entity.Address">
            <id property="address_areaId" column="address_regionId"/>
        </association>
    </resultMap>
    <insert id="insertOne" parameterType="address">
        INSERT address(address_areaId,address_name,address_regionId)
            VALUES (
            #{address.address_areaId},
            #{address.address_name},
            #{address.address_regionId})
    </insert>
    <update id="updateOne" parameterType="address">
        UPDATE address
        <set>
            <if test="address.address_name != null">address_name = #{address.address_name}</if>
        </set>
        <where>
            address_areaId = #{address.address_areaId}
        </where>
    </update>

    <select id="select" resultMap="address">
        SELECT address_areaId,address_name,address_regionId FROM address
        <where>
            <if test="address_name != null">
                address_name LIKE concat('%',#{address_name},'%')
            </if>
            <if test="address_regionId != null">
                and address_regionId = #{address_regionId} and address_areaId != address_regionId
            </if>
        </where>
    </select>
    <select id="selectOne" resultMap="address" parameterType="string">
        SELECT address_areaId,address_name,address_regionId FROM address
        <where>
            address_areaId = #{address_areaId}
        </where>
    </select>
    <select id="selectRoot" resultMap="address">
        SELECT address_areaId,address_name,address_regionId FROM address
        <where>
            address_areaId = address_regionId
        </where>
    </select>
</mapper>
```

