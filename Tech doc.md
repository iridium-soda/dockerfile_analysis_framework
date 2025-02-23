# 需求分析

## Targets

- [ ] 尽可能多的爬取dockerhub上的镜像
- [ ] 分析出metadata，分拣出尺寸比较大（大于10G、100G的镜像层）
- [ ] 数据的分析和清理

## Details

### Images get

- Dockerhub上的api最多只能返回10000个结果
- 通过枚举关键词进行尽可能全的搜集（e.g. `aaa`返回10000个结果，则继续搜索`aaaa`/`aaab`
- IP池

### Data Creep

It is necessary to take care of the following places：

Tags

![Oq4wz6.png](https://i.imgtg.com/2023/06/02/Oq4wz6.png)

Image size

![OqDqvg.png](https://i.imgtg.com/2023/06/02/OqDqvg.png)

Last updated

![OqD5dB.png](https://i.imgtg.com/2023/06/02/OqD5dB.png)

Overview: might to be too long; more processings needed.

![OqD5dB.png](https://i.imgtg.com/2023/06/02/OqDTOs.png)

Build history

1. Build Command
2. Size

## Structure

项目分为两个部分；

1. 爬取镜像名称和原数据
2. 以镜像名为主键获取dockerfile相关信息

## Usages

### main.py

- Description: Read images' names in `./images_list/$FILE` and get their dockerfile via dockerhub, github, and building history.
- Input: the path of images list in `images_list`
- Output: Dockerfile are saved at `./results/words-$FILE.list`.

URLS:

- `https://hub.docker.com/v2/repositories/<image_name>/dockerfile/`: Get dockerfile from dockerhub
- `https://hub.docker.com/api/audit/v1/build/?include_related=true&offset=0&limit=50&object=%2Fapi%2Frepo%2Fv1%2Frepository%2F<username>%2F<image_name>%2F`: Get github repo from dockerhub(if has)
- `https://raw.githubusercontent.com/<repo>/Dockerfile`: Get dockerfile from github repo
- `https://hub.docker.com/v2/repositories/<image_name>/tags/`: Get all tags from dockerhub and extract them via `content["results"]["name"]`
- `https://hub.docker.com/v2/repositories/<image_name>/tags/<tag_name>/images`: Get each layer's instruction to make up a dockerfile; exeract instructions from `content[layer][instruction]`. Add `ENTRYPOINT` if necessary.

### images\search_dockerhub.py

- Description: Get the image name, create time and update time from the images searching list like `image +` ", " + created + ", " + updated`.
- Input: Path of the keyword list.
- Output: Save metadata of images in `./results/all_images.list`.

URLS:

- `https://hub.docker.com/api/content/v1/products/search?page_size=100&q=<keyword>&type=image`

### images\crawl_keyword_list.py

- Input: None
- Output: Available keywords to `./keyWordList.txt`
- Description: Generate keywords and send research requests to the docker hub to find if it is accurate enough to crawl all results(<10000).

URLS:

- `https://hub.docker.com/search?q=<keyword>&type=image`: return html.

Note:

~~Put Firefox binary path to `browser = webdriver.Firefox(options=options,firefox_binary="")` before starting~~

**To do crwaling Parallelly, we divide the trees to 6 parts(maybe changed later), use command args to decide.**

### data/dataset.py

- Description: Read and parse docker file, and pick out the docker file that deserves attention.
- Input: filename in `/dataset/`.
- Output: Write `image + "-marked; " + str(words_dict[image])` to `/dataset/filename-words.list`

## TroubleShoots

`images\crawl_keyword_list.py`在无图形界面的ubuntu上运行时卡住了。（或者报Failed to read marionette port）这是个比较麻烦的问题，检查之后发现可能是firefox的问题。见<https://stackoverflow.com/questions/72374955/failed-to-read-marionette-port-when-running-selenium-geckodriver-firefox-a>

参考这个回答：<https://stackoverflow.com/a/76395058>

目前的问题是在收到合适的结果之后没有返回而是继续遍历tree，以及中途退出可能并非网络的问题。
