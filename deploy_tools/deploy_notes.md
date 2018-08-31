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

## Supervisor任务

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