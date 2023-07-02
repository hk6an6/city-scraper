# Investigating on the shell
```bash
export URL="https://www.tripadvisor.com/Restaurants-g315917-Nerja_Costa_del_Sol_Province_of_Malaga_Andalucia.html" && \
export PYTHON_VERSION=`python --version | sed 's/Python \([[:digit:]].[[:digit:]]\+\).*/python\1/g'` && \
export SCRAPY_SETTINGS="scrapy/lib/${PYTHON_VERSION}/site-packages/scrapy/settings/default_settings.py" && \
cat "${SCRAPY_SETTINGS}" \
| sed "s/^USER_AGENT = .*$/USER_AGENT = f\'Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/114.0.0.0 Safari\/537.36\'/g" \
> new_settings.py && \
mv new_settings.py ${SCRAPY_SETTINGS}
source scrapy/bin/activate
scrapy shell "${URL}"
```

# Set up
Prerrequisites:
```bash
xcode-select --install && \
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && \
brew install python
```

Dependencies:
```bash
python3 -m venv ./scrapy && \
source scrapy/bin/activate && \
pip3 install scrapy
```

# Running
```bash
source scrapy/bin/activate
scrapy runspiler /.spider.py -o output.csv
```
