# 基于mycat的透明代理

## 基于mycat的透明代理

* 环境

  ```text
  系统版本：linux
  数据库版本：mysql8.0
  jdk：8.0
  mycat：1.6
  ```

  -说明

  ```text
  本章对于数据库仅涉及主从复制的透明代理，不涉及主从切换，分库分表。对于mycat仅涉及仅涉及主从路由配置
  ```

## mysql安装配置

* docker-compose.yml

  ```text
  version: '2'
  services:
  m1:
    build: ./mysql_m1
    container_name: m1
    volumes:
      - ../config/mysql-m1/:/etc/mysql/:ro
      - ../config/mysql-m1/my.cnf:/etc/my.cnf:ro  
      - ../data/master/data:/var/lib/mysql
      - ../config/hosts:/etc/hosts:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3306:3306"
    networks:
      jznet:
        ipv4_address: 172.31.4.24
    ulimits:
      nproc: 65535
    hostname: m1
    mem_limit: 512m
    restart: always
    environment:
      - MYSQL_DATABASE=root
      - MYSQL_ROOT_PASSWORD=123456
  s1:
      build: ./mysql_s1
      container_name: s1
      volumes:
        - ../config/mysql-s1/:/etc/mysql/:ro
        - ../config/mysql-s1/my.cnf:/etc/my.cnf:ro  
        - ../data/slave/data:/var/lib/mysql
        - ../config/hosts:/etc/hosts:ro
        - /etc/localtime:/etc/localtime:ro
      ports:
        - "3307:3306"
      networks:
        jznet:
          ipv4_address: 172.31.4.25
      links:
        - m1
      ulimits:
        nproc: 65535
      hostname: s1
      mem_limit: 512m
      restart: always
      environment:
        - MYSQL_DATABASE=root
        - MYSQL_ROOT_PASSWORD=123456
  networks:
  jznet:
    driver: bridge
    ipam:
      driver: default
      config:
      - subnet: 172.31.4.0/26
        gateway: 172.31.4.1
  ```

* 数据库初始化配置

mysql-master

```text
# Copyright (c) 2014, 2016, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

#
# The MySQL  Server configuration file.
#
# For explanations see
# http://dev.mysql.com/doc/mysql/en/server-system-variables.html

[mysqld]
pid-file	= /var/run/mysqld/mysqld.pid
socket		= /var/run/mysqld/mysqld.sock
datadir		= /var/lib/mysql
#log-error	= /var/log/mysql/error.log

character-set-client-handshake=FALSE
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
init-connect='SET NAMES utf8mb4'

# By default we only accept connections from localhost

max_connections = 1000
default-authentication-plugin=mysql_native_password
#bind-address	= 127.0.0.1
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

secure_file_priv=/var/lib/mysql
#给数据库服务的唯一标识，一般为大家设置服务器Ip的末尾号
server-id=1
log-bin=mysql-bin

max_binlog_size = 500M #每个bin-log最大大小，当此大小等于500M时会自动生成一个新的日志文件。一条记录不会写在2个日志文件中，所以有时日志文件会超过此大小。
binlog_cache_size = 128K #日志缓存大小
log-slave-updates  #当Slave从Master数据库读取日志时更新新写入日志中，如果只启动log-bin 而没有启动log-slave-updates则Slave只记录针对自己数据库操作的更新。

expire_logs_days=20 #设置bin-log日志文件保存的天数，此参数mysql5.0以下版本不支持。

binlog_format="MIXED"   #设置bin-log日志文件格式为：MIXED，可以防止主键重复。

lower_case_table_names=1
```





