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
source ./dockerfile_analysis/Scripts/activate  # for ubuntu
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
       1. `sudo snap remove firefox`
       2. `sudo add-apt-repository ppa:mozillateam/ppa`
       3. **copy and paste it whole, not line by line**:

        ```shell
        echo '
        Package: *
        Pin: release o=LP-PPA-mozillateam
        Pin-Priority: 1001
        ' | sudo tee /etc/apt/preferences.d/mozilla-firefox
        ```

        4. `echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox`
        5. `sudo apt install firefox`

## Run

### Generate keywords

Generate keywords and test their availability, valid keywords(getting less than 10000 results) will be written to `./keyWordList-<char>.txt`.

(Under python venv)

```shell
python images/crawl_keyword_list.py (0~37) # To determine the initial character of keywords, from a to -
```

To run with `pm2`:

Install:

```shell
sudo apt install nodejs npm
sudo npm install pm2 -g
```

Run:

```shell
pm2 start --interpreter path_to_venv/bin/python images/crawl_keyword_list.py (0~37) --name crawl_keyword_list  --no-autorestart
```
