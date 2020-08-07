## OpenAPI简介
OpenAPI基于流行的SwaggerUI，用于快速生成项目的API前端展示系统，
方便程序开发人员与部分体验成员使用。

## 本API结构
本API目前只包含一个独立的应用，即`user`，已经包含了如下功能：
- 用户注册（基于用户名、密码、昵称、权限参数）
- 用户登录（基于用户名、密码，得到token，然后基于token）
- 用户查看自己的信息（基于token，默认权限`user:read`）
- 用户修改自己的信息（基于token，默认权限`user:write`（注册时需要手动添加））
- 用户删除自己的信息（基于token，默认权限`user:delete`（后台已做限制））

## OpenAPI使用说明
### 1. 游客注册
点击`用户注册`，点击`Try it out`，修改输入框中的一些信息，
然后点击`Executive`。
[register](assetopenapi-register.png)

### 2. 使用用户名与密码进行登录
点击`用户登录`，其他同上，然后复制获得的`token`。
[login](assetopenapi-login.png)

### 3. 测试使用token进行用户访问
点击`用户查看`，将`token`复制到`authorization-`中，其他同上。

（注意，标准的请求头字段应该是`Authorization`，
这里主要是因为Swagger的一些系统原因，不得不改成一个别名，
详情参考：https/github.cotiangolfastapissue612）
[read](assetopenapi-read.png)

### 4. 测试使用token进行用户修改
点击`用户修改`，其他同上。
由于我在系统中对用户修改的api加入了`user:write`字段检验，
而注册时默认没有加入该字段，因此会返回权限不够的结果。

如果想让这个接口可以使用，重新注册一个账户，
并且在注册信息`scopes`字段中加入`user:write`。
[write](assetopenapi-write.png)

### 5. 测试使用token进行用户注销
点击`用户注销`，其他同上。返回结果如下，原因已经解释了。

综上，基于jwt、OAuth2、前端和后端，
可以实现非常复杂的鉴权系统，满足不同种业务的需求。
[delete](assets/openapi-delete.png)