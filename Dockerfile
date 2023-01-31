FROM python:3.9.7

WORKDIR data_collection_project 

COPY . .

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

#install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN apt-get install -yqq unzip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

#install requirements
RUN pip3 --version
RUN python -m pip install selenium 
RUN python -m pip install requests
RUN python -m pip install --upgrade pip

#add the above into a requirements file rather?
#RUN pip install -r requirements.txt

CMD ["python", "webscraper_project/myprotein_scraper.py"]