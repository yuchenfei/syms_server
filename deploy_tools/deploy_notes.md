部署服务
===

## 需要安装的包：

* Nginx
* Git
* Python3
* pip
* libmysqlclient-dev
* virtualenv
* Node.js

以Ubuntu为例，可以执行下面的命令安装：

    curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
    sudo apt update
	sudo apt install nginx git python3 python3-pip libmysqlclient-dev nodejs
	sudo pip3 install virtualenv

## 执行部署

* 确保本地python环境中已经安装fabric3
* 在deploy_tools目录下执行`fab deploy:host=syms`，注：syms 为ssh config里服务器的别名

## 前端部署

fab脚本只获取最新的前端源码，部署需要执行以下命令

* `npm install`安装所需node.js的包,首次部署执行即可
* `npm run build`打包项目
* 将react/dist/static中的文件复制到项目static目录下

## 配置Supervisor任务

* 参考config_template/gunicorn-supervisor.conf
* 把USERNAME替换为服务器的用户名，例如my_name
* 把引号内的APP_ID、APP_SECRET替换为微信公众号对应的配置

## 配置Nginx虚拟主机

* 参考config_template/nginx.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com

## 文件夹结构：

	/root
	└─sites
	  └─syms
	    ├─database
	    ├─media
	    ├─react
	    ├─source
	    ├─static
	    └─virtualenv