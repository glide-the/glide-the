#### 基于mycat的透明代理
- 环境
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

#### mysql安装配置

- docker-compose.yml
```yml
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
- 数据库初始化配置
```text


```


