# archive

To save archived doc. Refer `Tech note` instead.



### 生成检索词并获取镜像列表

keyword生成在`images/keywords-list`。这里遍历字符集包含所有的可能的查询词，并分析响应中的结果数量。一般而言两个关键词拼接已经足够。

`images/crawl_keyword_list.py`该文件生成查询词的字符树并进行审查。然后将获取到的信息存到`images/images.list`里

1. 生成字符树
2. 遍历字符树
   1. 对每条路径：
      1. 调用`check_keyword_search_results`。在该函数中向dockerhub发送查询请求，URL为`"https://hub.docker.com/search?q={}&type=image".format(keyWord)`。
      2. 如果上一条返回0（正常退出），则调用`add_leaf_node`否则进入错误处理：
         1. 如果返回-2，意思是没有查询结果
         2. 如果返回0，意思是返回数量超过最大值1000000，则可继续添加查询词
         3. 如果返回1，意思是数量小于1000,将关键词加入`./keyWordList.txt`
         4. 对于小于1000000大于1000的结果数量如果小于2500返回1，其他情况返回0

### 获取镜像详细信息

位置在`images/search_dockerhub.py`

### 分析Dockerfile

位置在`data/dataset.py`

### `main.py`

读取`./images_list/$FILE`中提取到的镜像名，并多线程通过调用复写`threading. Thread`类的`run`方法，在`thread.srart`调用该方法获取对应的dockerfile写进`./results/words-$FILE.list`。

![main.dot](assets\main.dot.svg)

`crawler.py`按照从三个地方获取dockerfile，如果在之前的获得到则不执行后面的来源：

- Dockerhub。URL为`https://hub.docker.com/v2/repositories/<image_name>/dockerfile/`。例子：`https://hub.docker.com/v2/repositories/aaadigital/gcloud-backup-manager/dockerfile/`。
- Github。
  - 先从`https://hub.docker.com/api/audit/v1/build/?include_related=true&offset=0&limit=50&object=%2Fapi%2Frepo%2Fv1%2Frepository%2F<username>%2F<image_name>%2F`解析github repo地址,如果返回json中有`source_repo`字段则有repo，返回。
  - 如果有repo，则访问`https://raw.githubusercontent.com/<repo>/Dockerfile`。
- build history。
  - 获取tag列表。URL为`https://hub.docker.com/v2/repositories/<image_name>/tags/`,得到response中的`content["results"]["name"]`,例如：`"name": "latest",`
  - 然后遍历tags，对于每个image, tagName对，进行解析：
    - 访问`https://hub.docker.com/v2/repositories/<image_name>/tags/<tag_name>/images`获取response
    - 获取**每个**`layers`字段。对于每个layer获取其`instruction`字段。如果没有`ENTRYPOINT`则添加一个。

这里Dockerhub和buildhistroy的内容不一致？拿不到size信息

Dockerhub:

```json
{
    "contents": "FROM google/cloud-sdk:alpine\nRUN apk --no-cache add mysql-client gzip rsync tar\nCOPY /scripts/*.sh /scripts/\n"
}
```

buildhistory:

```json
 "layers": [

            {
                "size": 0,
                "instruction": " CMD [\"/bin/sh\"]"
            },
            {
                "size": 0,
                "instruction": " ARG CLOUD_SDK_VERSION=285.0.1"
            }
//...
]
```
