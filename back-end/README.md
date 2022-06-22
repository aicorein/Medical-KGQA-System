## 后端

### 1、目录

主要文件如下：

- `app.py`	后端启动
- `medicals_name.txt`	问句解析自定义词典
- `KG`	知识图谱相关数据、配置文件
  - `fuseki_config.ttl `	Apache Jena Fuseki 配置文件
  - `medicals.ttl`	知识图谱数据 ttl
  - `rules.ttl`	知识图谱推理规则 ttl



### 2、配置

​	python 依赖：`flask`、`flask-limiter`、`ltp`、`SPARQLWrapper`。

​	服务依赖：`Apache Jena Fuseki`。（配置可参考：[Apache jena 配置和使用](https://www.glowmem.com/archives/apache-jena)，配置常见问题可参考：[Apache Jena 查询配置 FAQ](https://www.glowmem.com/archives/apache-jena-qa)）



### 3、运行

​	运行 `Apahche Jena Fuseki` 服务。

​	运行 `app.py`。

​	浏览器 `localhost`。
