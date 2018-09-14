微信部署说明
===

## 公众号开发信息
* 进入`微信公众平台-开发-基础配置`，获取开发者ID(AppID)和开发者密码(AppSecret)
* 确保上述信息已填写到服务器的supervisor配置中，详细参考部署服务文档

## IP白名单
* 进入`微信公众平台-开发-基础配置`
* 将服务器IP填写到IP白名单中

## 服务器配置
* 进入`微信公众平台-开发-基础配置`
* 在服务器配置栏中点击修改配置
* URL填写http://DOMAIN/wx/，DOMAIN为服务器域名
* Token填写experiment
* 消息加解密方式为明文方式
* 保存

## 网页授权域名配置
* 进入`微信公众平台-设置-公众号设置`的功能设置页面
* 点击 网页授权域名 右边的设置
* 按照说明下载.txt文件，放到服务器的~/sites/syms/react/dist目录下
* 填写域名，保存

## 自定义菜单配置
* 这里使用office_accounts_menu.py脚本配置自定义菜单
* 需要执行脚本计算机的公网IP添加到IP白名单中
* 运行前须在环境变量写入APP_ID和APP_SECRET，或者修改脚本56行，在app_id和app_secret后直接填入相关字符串
* 执行`python office_accounts_menu.py`