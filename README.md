# Poem-es

## 简介

这是一个关于**中国古诗词**相关数据（唐诗5.7W+，宋诗25W+，宋词2.1W+）整合到elasticsearch中的项目。
涉及了这些数据的压缩. 简繁体转换. 数据加工. 数据建模和数据迁移等方面的步骤。

### 前置条件：

1. 请安装好**elk**套件（elasticsearch. logstash. kibana），且有elk的使用经验。
2. **elasticsearch**安装中文分词器**ik**。

### 使用：

1. 数据来源于[chinese-poetry](https://github.com/chinese-poetry/chinese-poetry)，通过`git clone`下载此项目

2. 将本项目中的fianl.py文件放置到chinese-poetry的根目录下，然后用python执行该脚本。即可在chinese-poetry的各个子数据目录中得到新增的`final_res_`为前缀的转换后的文件。该文件包含了对json数据文件的**压缩和简繁体转换**。

3. 将本项目中，mapping文件夹下的文件配置内容，分别复制到binaba的Devtool中进行执行，完成**数据建模**。

4. 修改本项目中logstash-conf文件夹下的文件配置内容，将path的所对应的值替换成，chinese-poetry项目在当前PC上的路径。

5. 切换到logstash的bin目录，依次执行`logstash -f 配置文件`，这里的配置文件，指前一个步骤中logstash-conf下的配置文件，建议依次执行。从而将对应的**数据导入到elasticsearch**中。

6. 上述步骤可以执行在服务器中执行。如果是在本地执行生成了最终数据，那么有如下几种迁移方式：
    * 用elasticsearch自带的api `reindex`。
    * 直接将本地elasticsearch的home目录下的data文件夹拷贝到服务器中。

### docker部署elasticsearch镜像的常见问题：

1. 通过`docker search elasticsearch`查看的elasticsearch版本是已经没有更新的老版本。最新的参考[这里](https://www.docker.elastic.co/)
2. docker运行挂载volumn的elasticsearch容器，通过`docker logs`，会查看到权限不足的问题，这个时候将要挂载的volumn权限修改成775
3. 暴露外网需要修改配置文件conf/elasticsearch.yml中的`network.host:0.0.0.0`
4. 暴露外网后，如果通过`docker logs`查看到`max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]`,那么在宿主机上执行`sudo sysctl -w vm.max_map_count=262144 docker`，具体参考docker的官方elasticsearch镜像的[issue](https://github.com/docker-library/elasticsearch/issues/98)
5. conf/jvm.options中的关于初始堆和最大堆内存，最好设置成一样的，运行时docker容器无法再申请更多内容资源。
6. 参考docker执行命令如下:

    `docker run -d -p 9200:9200 -p 9300:9300 --name poem-es -v $PWD/config:/usr/share/elasticsearch/config -v $PWD/esdata:/usr/share/elasticsearch/data  -v $PWD/plugins:/usr/share/elasticsearch/plugins   docker.elastic.co/elasticsearch/elasticsearch:6.3.2`