# Mybatis-Plus （MP）查询分页

## 1. 简介：

MyBatis-Plus (opens new window)（简称 MP）是一个 MyBatis (opens new window)的增强工具，在 MyBatis 的基础上只做增强不做改变，为简化开发、提高效率而生。

## 2. 特征：

无侵入：只做增强不做改变，引入它不会对现有工程产生影响
损耗小：启动即会自动注入基本 CURD，性能基本无损耗，直接面向对象操作
强大的 CRUD 操作：内置通用 Mapper、通用 Service，仅仅通过少量配置即可实现单表大部分 CRUD 操作，更有强大的条件构造器，满足各类使用需求
支持 Lambda 形式调用：通过 Lambda 表达式，方便的编写各类查询条件，无需再担心字段写错
支持主键自动生成：支持多达 4 种主键策略（内含分布式唯一 ID 生成器 - Sequence），可自由配置，完美解决主键问题
支持 ActiveRecord 模式：支持 ActiveRecord 形式调用，实体类只需继承 Model 类即可进行强大的 CRUD 操作
支持自定义全局通用操作：支持全局通用方法注入（ Write once, use anywhere ）
内置代码生成器：采用代码或者 Maven 插件可快速生成 Mapper 、 Model 、 Service 、 Controller 层代码，支持模板引擎，支持自定义配置
内置分页插件：基于 MyBatis 物理分页，开发者无需关心具体操作，配置好插件之后，写分页等同于普通 List 查询
分页插件支持多种数据库：支持 MySQL、MariaDB、Oracle、DB2、H2、HSQL、SQLite、Postgre、SQLServer 等多种数据库
内置性能分析插件：可输出 SQL 语句以及其执行时间，建议开发测试时启用该功能，能快速揪出慢查询
内置全局拦截插件：提供全表 delete 、 update 操作智能分析阻断，也可自定义拦截规则，预防误操作

## 3. LambdaQueryWrapper

有一张banner_item表，现需要通过banner_id查出所有数据(查询List)

实体：

```java
@Data
public class BannerItem {
    private Long id;
    private String name;
    private String img;
    private String keyword;
    private Integer type;
    private Long bannerId;
}
```

① QueryWrapper：

```java
/* 最基础的查询方式 */
// 查询条件构造器
QueryWrapper<BannerItem> wrapper = new QueryWrapper<>();
wrapper.eq("banner_id", id);
// 查询操作
List<BannerItem> bannerItems = bannerItemMapper.selectList(wrapper);


/* 引入lambda，避免我们在代码中写类似的于banner_id的硬编码 */
QueryWrapper<BannerItem> wrapper = new QueryWrapper<>();
wrapper.lambda().eq(BannerItem::getBannerId, id);
List<BannerItem> bannerItems = bannerItemMapper.selectList(wrapper);
```

② LambdaQueryWrapper：

```java
/* 为了简化lambda的使用，我们可以改写成LambdaQueryWrapper构造器 */
LambdaQueryWrapper<BannerItem> wrapper = new QueryWrapper<BannerItem>().lambda();
wrapper.eq(BannerItem::getBannerId, id);
List<BannerItem> bannerItems = bannerItemMapper.selectList(wrapper);

/* 再次将QueryWrapper.lambda()简化 */
LambdaQueryWrapper<BannerItem> wrapper = new LambdaQueryWrapper<>();
wrapper.eq(BannerItem::getBannerId, id);
List<BannerItem> bannerItems = bannerItemMapper.selectList(wrapper);
```

LambdaQueryWrapper链式查询

```java
List<BannerItem> bannerItems = new LambdaQueryChainWrapper<>(bannerItemMapper)
                        .eq(BannerItem::getBannerId, id)
                        .list();

/* 如果只想查询一条记录，例如通过id查询某条记录的详情，使用.one()即可，例如 */
BannerItem bannerItem = new LambdaQueryChainWrapper<>(bannerItemMapper)
                        .eq(BannerItem::getId, id)
                        .one();
```



| setSqlSelect | SELECT 查询字段                   | 举例                                                         |
| ------------ | --------------------------------- | ------------------------------------------------------------ |
| where        | WHERE 语句，拼接 + WHERE 条件     |                                                              |
| and          | AND 语句，拼接 + AND 字段=值      |                                                              |
| andNew       | AND 语句，拼接 + AND (字段=值)    |                                                              |
| or           | OR 语句，拼接 + OR 字段=值        | .eq(" name “,” 木 子 “). or ( ). eq (” id ", 1 ) => name=“木子” or id=1 注意事项：主动调用or表示下一个方法不是and连接，不调用默认为使用and连接 |
| orNew        | OR 语句，拼接 + OR (字段=值)      |                                                              |
| eq           | 等于=                             | .eq(“name”,“木子”) => name=“木子”                            |
| allEq        | 基于 map 内容等于=                |                                                              |
| ne           | 不等于<>                          |                                                              |
| gt           | 大于>                             |                                                              |
| ge           | 大于等于>=                        |                                                              |
| lt           | 小于<                             |                                                              |
| le           | 小于等于<=                        |                                                              |
| like         | 模糊查询 LIKE                     | .like(“name”,“木子”) => name like ‘%木子%’                   |
| notLike      | NOT LIKE模糊查询                  |                                                              |
| in           | IN 查询                           | .in(“age”,{1,2,3}) => age in (1,2,3)                         |
| notIn        | NOT IN 查询                       |                                                              |
| isNull       | NULL 值查询                       |                                                              |
| isNotNull    | IS NOT NULL                       |                                                              |
| groupBy      | 分组 GROUP BY                     |                                                              |
| having       | HAVING 关键词                     |                                                              |
| orderBy      | 排序 ORDER BY                     |                                                              |
| orderAsc     | Asc 排序 ORDER BY                 |                                                              |
| orderDesc    | DESC 排序 ORDER BY                |                                                              |
| exists       | EXISTS 条件语句                   |                                                              |
| notExists    | NOT EXISTS 条件语句               |                                                              |
| between      | BETWEEN 条件语句                  | .between (“age”,1,2) => age between 1 and 2                  |
| notBetween   | NOT BETWEEN 条件语句              |                                                              |
| addFilter    | 自由拼接 SQL                      |                                                              |
| last         | 拼接在最后，例如：last(“LIMIT 1”) |                                                              |

## 4. BaseMapper

### 4.1 Insert

```java
// 插入一条记录
int insert(T entity);
```

### 4.2 Delete

```java
// 根据 entity 条件，删除记录
int delete(@Param(Constants.WRAPPER) Wrapper<T> wrapper);
// 删除（根据ID 批量删除）
int deleteBatchIds(@Param(Constants.COLLECTION) Collection<? extends Serializable> idList);
// 根据 ID 删除
int deleteById(Serializable id);
// 根据 columnMap 条件，删除记录
int deleteByMap(@Param(Constants.COLUMN_MAP) Map<String, Object> columnMap);
```

### 4.3 Update

```java
// 根据 whereEntity 条件，更新记录
int update(@Param(Constants.ENTITY) T entity, @Param(Constants.WRAPPER) Wrapper<T> updateWrapper);
// 根据 ID 修改
int updateById(@Param(Constants.ENTITY) T entity);
```

### 4.4 Select

```java
// 根据 ID 查询
T selectById(Serializable id);
// 根据 entity 条件，查询一条记录
T selectOne(@Param(Constants.WRAPPER) Wrapper<T> queryWrapper);

// 查询（根据ID 批量查询）
List<T> selectBatchIds(@Param(Constants.COLLECTION) Collection<? extends Serializable> idList);
// 根据 entity 条件，查询全部记录
List<T> selectList(@Param(Constants.WRAPPER) Wrapper<T> queryWrapper);
// 查询（根据 columnMap 条件）
List<T> selectByMap(@Param(Constants.COLUMN_MAP) Map<String, Object> columnMap);
// 根据 Wrapper 条件，查询全部记录
List<Map<String, Object>> selectMaps(@Param(Constants.WRAPPER) Wrapper<T> queryWrapper);
// 根据 Wrapper 条件，查询全部记录。注意： 只返回第一个字段的值
List<Object> selectObjs(@Param(Constants.WRAPPER) Wrapper<T> queryWrapper);

// 根据 entity 条件，查询全部记录（并翻页）
IPage<T> selectPage(IPage<T> page, @Param(Constants.WRAPPER) Wrapper<T> queryWrapper);
// 根据 Wrapper 条件，查询全部记录（并翻页）
IPage<Map<String, Object>> selectMapsPage(IPage<T> page, @Param(Constants.WRAPPER) Wrapper<T> queryWrapper);
// 根据 Wrapper 条件，查询总记录数
Integer selectCount(@Param(Constants.WRAPPER) Wrapper<T> queryWrapper);
```

## 5. MetaObjectHandler

MetaObjectHandler接口是mybatisPlus为我们提供的的一个扩展接口，我们可以利用这个接口在我们插入或者更新数据的时候，为一些字段指定默认值。实现这个需求的方法不止一种，在sql层面也可以做到，在建表的时候也可以指定默认值。

## 6. 示例：

① 实体类：

```java
package com.lifan.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import java.io.Serializable;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

/**
 *
 * @author lifan
 * @since 2021-07-09
 */
@Data
@EqualsAndHashCode(callSuper = false)
@Accessors(chain = true)
public class AcUser implements Serializable {
    private static final long serialVersionUID = 1L;
    @TableId(value = "id", type = IdType.ID_WORKER_STR)
    private Integer id;
    private String name;
    private String type;
}
```

② Mapper 接口：

```java
package com.lifan.mapper;

import com.lifan.entity.AcUser;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;

/**
 * <p>
 *  Mapper 接口
 * </p>
 *
 * @author lifan
 * @since 2021-07-09
 */
@Mapper
public interface AcUserMapper extends BaseMapper<AcUser> {


}
```

③ service接口：

```java
package com.lifan.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.lifan.entity.AcUser;
import com.baomidou.mybatisplus.extension.service.IService;
import com.lifan.request.AcUserReq;
import com.lifan.response.AcUserResp;

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author lifan
 * @since 2021-07-09
 */
// 服务层的接口需要继承 IService<实体类> ，定义分页查询方法，其返回值类型是 IPage<实体类> .
public interface AcUserService extends IService<AcUser> {

    IPage<AcUserResp> listPage(AcUserReq req);

}
```

  AcUserServiceImpl 实现类：

```java
package com.lifan.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.lifan.entity.AcUser;
import com.lifan.mapper.AcUserMapper;
import com.lifan.request.AcUserReq;
import com.lifan.response.AcUserResp;
import com.lifan.service.AcUserService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.List;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author lifan
 * @since 2021-07-09
 */
@Service
// 服务的实现类要继承 ServiceImpl< Mapper接口类，实体类 > ，重写分页查询方法.
public class AcUserServiceImpl extends ServiceImpl<AcUserMapper, AcUser> implements AcUserService {

    @Override
    public IPage<AcUserResp> listPage(AcUserReq req) {

        Page<AcUser> page = new Page<AcUser>(req.getPage(),req.getPageSize());
        LambdaQueryWrapper<AcUser> lambdaQueryWrapper = new LambdaQueryWrapper();

        //如果传了 name 属性，可根据 name 进行模糊匹配
        if(req.getName() != null){
            lambdaQueryWrapper.like(AcUser::getName,req.getName());
        }

        // Type 属性，Y为启用，  N为冻结 。 （相当于where条件过滤）
        if(req.getType() != null){
            lambdaQueryWrapper.eq(AcUser::getType,req.getType());
        }

        IPage<AcUser> iPage = this.page(page,lambdaQueryWrapper);

        List<AcUserResp> list = new ArrayList<>();

        for (AcUser acUser : iPage.getRecords ()) {
            AcUserResp resp = new AcUserResp ();
            BeanUtils.copyProperties (acUser,resp);
            list.add (resp);
        }

        System.out.println(list);
        IPage<AcUserResp> respIPage = new Page<> ();
        BeanUtils.copyProperties (iPage,respIPage);
        respIPage.setRecords (list);
        
        return respIPage;
    }
}
```

④ controller：

```java
package com.lifan.controller;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.lifan.request.AcUserReq;
import com.lifan.response.AcUserResp;
import com.lifan.service.AcUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author lifan
 * @since 2021-07-09
 */
@RestController
public class AcUserController {

    @Autowired
    private AcUserService acUserService;

    @PostMapping("/Query")
    public IPage<AcUserResp> SspFxProChannelQuery(@RequestBody AcUserReq req) {

        return acUserService.listPage(req);
    }
}
```



⑤ AcUserReq 接受请求类：

```java
package com.lifan.request;

import lombok.Data;

/**
 *
 * @author lifan
 * @since 2021-07-09
 */
@Data
public class AcUserReq {

    private String name;

    private String type;

    private int page;

    private int pageSize;

}
```

AcUserResp 请求返回类：

```java
package com.lifan.response;

import lombok.Data;

/**
 * @author lifan
 * @since 2021-07-09
 */
@Data
public class AcUserResp{

    private Integer id;

    private String name;

    private String type;

}
```

