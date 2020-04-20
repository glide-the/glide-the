# mysql主从docker

## mysql主从docker

* docker-compose.yml

```text
version: '2'
services:
  mysql-master:
   image: docker.io/mysql
   networks:
       jznet:
        ipv4_address: 172.18.4.24
   volumes:
+ ./master/data:/var/lib/mysql
+ ./master/conf/mysql.conf.cnf:/etc/mysql/conf.d/mysql.conf.cnf
   ports:
+ "3306:3306"
   environment:
+ MYSQL_DATABASE=root
+ MYSQL_ROOT_PASSWORD=123456
  mysql-slave:
   image: docker.io/mysql
   networks:
       jznet:
        ipv4_address: 172.18.4.25
   volumes:
+ ./slave/data:/var/lib/mysql
+ ./slave/conf/mysql.conf.cnf:/etc/mysql/conf.d/mysql.conf.cnf
   ports:
+ "3307:3306"
   environment:
+ MYSQL_DATABASE=root
+ MYSQL_ROOT_PASSWORD=123456
networks:
  jznet:
    driver: bridge
    ipam:
      driver: default
      config:
+ subnet: 172.18.4.0/26
```



* 执行如下命令

```text
docker-compose  up -d
Creating network "wen_jznet" with driver "bridge"
Creating wen_mysql-slave_1
Creating wen_mysql-master_1
```

## master

* 创建用户

  ```text
    CREATE USER 'repl'@'%' IDENTIFIED WITH mysql_native_password BY 'Ron_master_1';
  ```

* 赋予权限

  ```text
    GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
  ```

* 查询bin-log Positior

  ```text
     show master status;
  ```

## slave

* 设置master的信息

  ```text
     CHANGE MASTER TO
     MASTER_HOST='172.18.4.24',
     MASTER_USER='repl',
     MASTER_PASSWORD='Ron_master_1',
     MASTER_LOG_FILE='mysql-bin.000003',
     MASTER_LOG_POS=650;
  ```

* 启动slave

  ```text
    start slave;
    show slave status;
  ```

## 验证

```text
create schema test;
show schemas;
```

