# Usage

Steps of steps to install and run the service.

## Requirements

- Windows or ubuntu22.04(My env)
- Python3

## Installation

Clone the repo:

```shell
git clone https://github.com/iridium-soda/dockerfile_analysis_framework.git
cd dockerfile_analysis_framework
```

Prepare a python venv:

```shell
python -m venv dockerfile_analysis
dockerfile_analysis\Scripts\activate.bat # for Windows cmd
source ./dockerfile_analysis/bin/activate  # for ubuntu
```

Install dependencies:

```shell
pip3 install -r requirements.txt
cd pkg && sudo python3 setup.py install
```

Prepare drivers:

- For windows:
    1. Download [Firefox](https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US)
    2. Download [geckodriver](https://github.com/mozilla/geckodriver/releases/download/v0.32.2/geckodriver-v0.32.2-win64.zip). **Thoroughly inspect the release log to ascertain whether the driver corresponds to the version of Firefox that has been downloaded.**
    3. Add the path of `geckodriver` to the system PATH.
- For Ubuntu:
    1. [Download](https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz) geckodriver by `wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz`. **Thoroughly inspect the release log to ascertain whether the driver corresponds to the version of Firefox that has been downloaded.**
    2. Decompress:`tar -xvzf geckodriver-v0.33.0-linux64.tar.gz`
    3. Move the binary to `/usr/local/bin/`:`sudo mv geckodriver /usr/local/bin/`
    4. Grant executable privileges to `geckodriver`:`sudo chmod +x /usr/local/bin/geckodriver`
    5. Install Firefox carefully, refer this answer in [StackOverflow](https://stackoverflow.com/a/76395058):
       1. `sudo apt-get install xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic xvfb dbus-x11 x11-apps imagemagick`
       2. `sudo snap remove firefox`
       3. `sudo add-apt-repository ppa:mozillateam/ppa`
       4. **copy and paste it whole, not line by line**:

        ```shell
        echo '
        Package: *
        Pin: release o=LP-PPA-mozillateam
        Pin-Priority: 1001
        ' | sudo tee /etc/apt/preferences.d/mozilla-firefox
        ```

        5. `echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox`
        6. `sudo apt install firefox`

## Run

### Generate keywords

Generate keywords and test their availability, valid keywords(getting less than 10000 results) will be written to `./keyWordList-<char>.txt`.

(Under python venv)

```shell
python images/crawl_keyword_list.py (0~37) # To determine the initial character of keywords, from a to -
```

To run background:

```shell
nohup python3 -u images/crawl_keyword_list.py 0 >> output-a.log 2>&1 &
```

**Be sure to remove all file named `./keyWordList-<char>.txt` before running. Maybe fix it later.**

**Try never run multi this programs at the same time.**

TroubleShoots:

If the program stuck, uninstall and reinstall Firefox follow steps above. Or just praying and retrying...

### Search Images

Search for all images based on avaliable keywords we get in the previous step.

```shell
python images/search_dockerhub.py keywords/keyWordList-_.txt
```

Ensure the network connection runs normally.
