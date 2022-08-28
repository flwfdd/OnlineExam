# OnlineExam

因为网安周马上就要来了，要搞一个网安知识竞赛。以前都是用乐学但是手机体验不好。试了试问卷星随机抽题功能要会员太贵了（￥128/周），金数据的试卷又不支持批量导入，那就自己做一个呗。用差不多一天的时间糊了整个东西出来，刚好在上小学期，小学期的Web开发基础这门课的作业恰好也是类似的（不过这门课用逆天的ASP+IIS，什么考古发现，真是气死我了），就直接拿来主义把CSS什么的搞过来了，故也没有用前端框架，用了CDN引入的Vue2，就一个[index.html](https://github.com/flwfdd/OnlineExam/blob/master/code/index.html)。后端是Python+Flask，全部放在阿里云函数计算上，数据库也是之前几块钱嫖的阿里云RDS。现在Serverless生态一整套搞下来已经十分方便了，但细节上还是有缺陷（例如git还得手动清理安装的python包）。

本来是想做一点管理员的部分的，比如前端编辑试卷、多张试卷管理什么的，一开始设计数据库也考虑了一点，但是做着做着就没心情了，最后就只做了答题的部分，其他的就硬搞数据库得了。时间紧任务重，总的来说源码就是惨不忍睹，但是也有优点——能跑！！

# start-flask 帮助文档

<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-flask&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=start-flask" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-flask&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=start-flask" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-flask&type=packageDownload">
  </a>
</p>

<description>

Flask是一个使用 Python 编写的轻量级 Web 应用框架。其 WSGI 工具箱采用 Werkzeug ，模板引擎则使用 Jinja2 。Flask使用 BSD 授权

</description>

<table>

## 前期准备
使用该项目，推荐您拥有以下的产品权限 / 策略：

| 服务/业务 | 函数计算 |     
| --- |  --- |   
| 权限/策略 | AliyunFCFullAccess |  

</table>

<codepre id="codepre">

# 代码 & 预览

- [ :smiley_cat:  源代码](https://github.com/devsapp/start-web-framework/blob/master/web-framework/python/flask)

</codepre>

<deploy>

## 部署 & 体验

<appcenter>

-  :fire:  通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=start-flask) ，
[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=start-flask)  该应用。 

</appcenter>

- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
    - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://www.serverless-devs.com/fc/config) ；
    - 初始化项目：`s init start-flask -d start-flask`   
    - 进入项目，并进行项目部署：`cd start-flask && s deploy -y`

</deploy>

<appdetail id="flushContent">

# 应用详情


本项目是将 Python Web 框架中，非常受欢迎的 Flask 框架，部署到阿里云 Serverless 平台（函数计算 FC）。

> Flask是一个使用 Python 编写的轻量级 Web 应用框架。其 WSGI 工具箱采用 Werkzeug ，模板引擎则使用 Jinja2 。Flask使用 BSD 授权。

通过 Serverless Devs 开发者工具，您只需要几步，就可以体验 Serverless 架构，带来的降本提效的技术红利。

本案例应用是一个非常简单的 Hello World 案例，部署完成之后，您可以看到系统返回给您的案例地址，例如：

![图片alt](https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1644567788251_20220211082308412077.png)

此时，打开案例地址，就可以看到测试的应用详情：

![图片alt](https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1644567807662_20220211082327817140.png)



</appdetail>

<devgroup>

## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
|--- | --- | --- |
| <center>微信公众号：`serverless`</center> | <center>微信小助手：`xiaojiangwh`</center> | <center>钉钉交流群：`33947367`</center> | 

</p>

</devgroup>