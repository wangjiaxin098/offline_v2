### twenty 10.5
1.安装postGreSQL 
Navicat Premium17 新建连接 
配置属性 连接postgre
![img_11.png](img_11.png)

在postgre 里面创建两张表

    CREATE TABLE public.a (
    id SERIAL PRIMARY KEY,
    name VARCHAR(10),
    sex VARCHAR(10)
    );
    INSERT INTO a VALUES (1,'张三','男');
    INSERT INTO a VALUES (2,'张二','男');
    INSERT INTO a VALUES (3,'张三三','男');
    INSERT INTO a VALUES (4,'张四','男');
    INSERT INTO a VALUES (5,'张五','男');
    
    CREATE TABLE public.b (
    id SERIAL PRIMARY KEY,
    name VARCHAR(10),
    sex VARCHAR(10)
    );
    INSERT INTO b VALUES (1,'小花1','女');
    INSERT INTO b VALUES (2,'小花2','女');
    INSERT INTO b VALUES (3,'小花3','女');
    INSERT INTO b VALUES (4,'小花4','女');
    INSERT INTO b VALUES (5,'小花5','女');

启动kfk读数据 
    kfk启动命令 kfk.sh start

使用flinkcdc读取sql数据
public static void main(String[] args) throws Exception {
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.setParallelism(1);

        SingleOutputStreamOperator<String> cdc = FlinkCDC.mysqlCDC(env, "aa", "*");
        cdc.print();

        // 实时获取MySQL表中的问诊数据，过滤掉脏数据，并解析json，将结果保存到kafka话题中。（5分）
        SingleOutputStreamOperator<JSONObject> flatted = cdc.flatMap(new FlatMapFunction<String, JSONObject>() {
            @Override
            public void flatMap(String string, Collector<JSONObject> collector) throws Exception {
                try {
                    JSONObject jsonObject = JSONObject.parseObject(string);
                    if (jsonObject != null) {
                        collector.collect(jsonObject);
                    }
                } catch (Exception e) {
                    System.out.println("数据有误");
                }
            }
        });
-- 查看数据
//        flatted.print();


-- 数据通过工具包 上传kafka
        flatted.map(JSONObject::toString).addSink(MyKafkaUtil.getKafkaProducer("zk2"));

        env.execute();
    }








































2.安装sql server
    下载官方sql server 2019源到本地
wget -O /etc/yum.repos.d/mssql-server.repo https://packages.microsoft.com/config/rhel/8/mssql-server-2019.repo

    linux安装命令
yum install -y mssql-server






