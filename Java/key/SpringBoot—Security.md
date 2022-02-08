# SpringBoot—Security

## 1. 前言

Spring Security是一个功能强大且高度可定制的身份验证和访问控制框架，提供了完善的认证机制和方法级的授权功能，是一款非常优秀的权限管理框架。它的核心是一组过滤器链，不同的功能经由不同的过滤器。这篇文章就是想通过一个小案例将Spring Security整合到SpringBoot中去。要实现的功能就是在认证服务器上登录，然后获取Token，再访问资源服务器中的资源。

## 2. 基本概念

### 2.1 单点登录

单点登录就是在一个多应用系统中，在其中一个系统上登录之后，需要在其它系统上登录才能访问其他内容。举个例子，京东那么复杂的系统肯定不会是单体结构，必然是微服务架构，比如订单功能是一个系统，交易是一个系统…那么我在下订单的时候登录了，付钱难道则不需要再登录一次。实现的流程就是我在下单的时候系统发现我没登录就让我登录，登录完了之后系统返回给我一个*Token*，就类似于身份证的东西；然后我想去付钱的时候就把Token再传到交易系统中，然后交易系统验证一下Token就知道是谁了，就不需要再登录一次。

### 2.2 JWT（JSON Web Token）

上面提到的Token就是**JWT(JSON Web Token)**，是一种用于通信双方之间传递安全信息的简洁的、URL安全的表述性声明规范。一个JWT实际上就是一个字符串，它由三部分组成：头部（header）、载荷（payload）与签名（signature）。

```
最终生成的JWT令牌就是下面这样，有三部分，用 . 分隔。

base64UrlEncode(JWT 头)+"."+base64UrlEncode(载荷)+"."+HMACSHA256(base64UrlEncode(JWT 头) + “.” + base64UrlEncode(有效载荷),密钥)

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
```

### 2.3 RSA

JWT在加密解密的时候都用到了同一个密钥 “ **robod666** ”，这将会带来一个弊端，如果被黑客知道了密钥的内容，那么他就可以去伪造Token了。所以为了安全，我们可以使用非对称加密算法**RSA**。

RSA的基本原理有两点：

- 私钥加密，持有私钥或公钥才可以解密
- 公钥加密，持有私钥才可解密

## 3. 实现

