# dockerfile_analysis_framework

To install docker file parse package

``cd pkg && sudo python3 setup.py install``

``pip3 install bashlex,request``

Others may need install:

- Selenium
- geckodriver (refer <https://pythondjango.cn/python/tools/7-python_selenium/#%E9%A9%B1%E5%8A%A8%E4%B8%8B%E8%BD%BD> to install)
- etc

## Usages

### Preparation

```bash
python -m venv dockerfile_analysis
dockerfile_analysis\Scripts\activate.bat #for Windows bash
dockerfile_analysis\Scripts\Activate.ps1 #In Powershell
```

Then install dependencies:

```shell
pip install -r requirements.txt
```

### KeywordsGen

Generate keywords and test their availability, valid keywords(getting less than 10000 results) will be written to `./keyWordList.txt`.

#### Installation

1. [Download](https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US) Firefox
2. [Download](https://github.com/mozilla/geckodriver/releases/download/v0.32.2/geckodriver-v0.32.2-win64.zip)`geckodriver`
3. Export the path of `geckodriver.exe` to `PATH`
4. Put the path to `s` :

```python
s = Service(r"PATH/to/geckodriver.exe")# NOTE:change it before running
```

#### Run

```shell
python ./images/crawl_keyword_list.py (0~37)
```

How many processes are running at the same time? Refer the source code.

### Search images by keywords in dockerhub

- Configure proxy pool

```shell
python images\\search_dockerhub.py images\\keywords-list\\keyWordList_--.txt 
```

- `isAlive`应该改为`t.is_alive()`