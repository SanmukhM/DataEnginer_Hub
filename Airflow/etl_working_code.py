#!/usr/bin/env python
# coding: utf-8

# In[14]:

from pyspark.sql import SparkSession

spark=SparkSession.builder.master('yarn').appName('etl_model-ops-demo').getOrCreate()

jdbc = "jdbc:mysql://35.200.190.236:3306/db1"

jdbcUrl = jdbc #"jdbc:mysql://{0}:{1}/{2}?user={3}&password={4}".format(jdbcHostname, jdbcPort, jdbcDatabase, username, password)

connectionProperties = {
  "user" : "etl_test",
  "password" : "EYmlopsPOC",
  "driver" : "com.mysql.cj.jdbc.Driver" #com.mysql.jdbc.Driver
}


# In[15]:


train1_df = spark.read.format("jdbc").option("url", "jdbc:mysql://35.200.190.236:3306/db1").option("driver", "com.mysql.cj.jdbc.Driver").option("dbtable", "applications_train1").option("user", "etl_test").option("password", "EYmlopsPOC").load()

train1_df.show(5, False)


# In[8]:


train2_df = spark.read.options(inferSchema='True',delimiter=',',header='True').csv("gs://application-train-data/application_train2.csv")
train2_df.show(5, False)


# In[9]:


train3_df = spark.read.options(inferSchema='True',delimiter=',',header='True').csv("gs://application-train-data/application_train3.csv")
train3_df.show(5, False)


# In[16]:


#print(train1_df.count())
#print(train2_df.count())
#print(train3_df.count())


# In[32]:


final_join_train_df = train1_df.join(train2_df,train1_df["SK_ID_CURR"] ==  train2_df["SK_ID_CURR"], "inner").join(train3_df,train1_df["SK_ID_CURR"] ==  train3_df["SK_ID_CURR"], "inner").select("*").drop(train2_df["SK_ID_CURR"]).drop(train3_df["SK_ID_CURR"])

#Writing output to gcs bucket
final_join_train_df.coalesce(1).write.option("header", "true").option("treatEmptyValuesAsNulls", "false").mode('overwrite').csv("gs://ml-ops-poc-data/credit-risk-data/raw_data/etl_output")

# In[29]:


print(len(final_join_train_df.columns))
#print(join_train_df.count())


# In[ ]:




