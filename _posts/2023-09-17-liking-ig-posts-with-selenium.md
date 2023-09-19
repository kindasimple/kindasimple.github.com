---
title: Engage with Instagram Posts using Selenium
author: evan
tagline: Using selenium to automate liking Instagram posts
tags: [social media, python, selenium]
category: [Automation]
header:
  teaser: /assets/images/header-liking-ig-posts-with-selenium.png
  image: /assets/images/header-liking-ig-posts-with-selenium.png
  image_description: "A helpful robot ready to like your posts"
  show_overlay_excerpt: true
  overlay_image: /assets/images/header-liking-ig-posts-with-selenium.png
  overlay_filter: 0.5
---

Social media engagement matters, like it or not. Lately I find myself more engaged with creator content on YouTube and TikTok than the posts from my connections on Facebook and Instagram. I feel bad about neglecting posts from friends and family, but I don't always have the attention to spare. Automating this engagement is a fun project.

## InstaPy

 There is already a full featured python library for interactive [InstaPy](https://github.com/InstaPy/InstaPy)

> Tooling that automates your social media interactions to “farm” Likes, Comments, and Followers on Instagram Implemented in Python using the Selenium module.

It *should* be possible to write a quick script to like posts.

```python
session = InstaPy(username=insta_username, password=insta_password, headless_browser=True)
session.login()
with smart_run(session):
    session.interact_by_users(["someone_I_follow"], amount=5, randomize=False, media="Photo")
    session.like_by_tags(["love"], amount=100, media="Photo")
```

Unfortunately, there are a bunch of open issues and the project is not actively maintained. There is [A fork](https://github.com/InstaPy2/InstaPy2) that might resuscitate the project, but for the time being there don't seem to be any good alternatives in for automating likes using python scripting. What I'm looking to do is pretty simple, so I'll just use selenium directly.

## Selenium

[Selenium](https://www.selenium.dev/) is a browser automation tool. It can be used to automate interactions with a browser. It's a great tool for testing web applications, but it can also be used to automate repetitive tasks.


### Installation

Using docker to run selenium is a great way to get started. We need our browser (Firefox), geckodriver, and the selenium python library.

```bash
docker run -it python:3.11.5 bash

# Install dependencies outlined in https://takac.dev/example-of-selenium-with-python-on-docker-with-latest-firefox/

# set the configuration
PLATFORM=aarch64
GECKODRIVER_VER=v0.33.0

# install firefox
apt install -y firefox-esr

# install geckodriver
curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux-${PLATFORM}.tar.gz \
    && tar zxf geckodriver-${GECKODRIVER_VER}-linux-${PLATFORM}.tar.gz \
    && mv geckodriver /usr/bin/

# install selenium
python3 -m pip install selenium
```

### Scripting

With selenium set up, we can start to write our python script. Its simple to open a browser and navigate to a page.

```python
browser = webdriver.Firefox(options=options)
browser.get("https://www.instagram.com/")
```

### Login

Next is to interact with the page. We need to log in to instagram. I used browser's developer tools to inspect the login form and find the name of the input fields. We can then use selenium's `find_element` method with the `By.NAME` parameter to find the well named input fields and fill them in with our credentials by sending keystrokes for our credential.

```
# complete login form and log in to instagram
input_username = browser.find_element(By.NAME, "username")
input_username.send_keys(username)
input_password = browser.find_element(By.NAME, "password")
input_password.send_keys(password)
```
Finding buttons is a bit less strait-forward since the buttons need to be identified by the text in a nested element. here we can use `find_element` method with `By.XPATH` to find the button, then submit the form.

```python
login = browser.find_element(
    By.XPATH, '//button[descendant-or-self::*[contains(text(), "Log in")]]'
)
login.submit()
```
### Dismissing Modals

After logging in, we need to dismiss the dialog boxes. I used the `find_element` method with `By.XPATH` to locate the dialog box button with the event handler to dismiss the modal box and then clicked on it.


```python
# dismiss the dialog boxes
save_creds_not_now = browser.find_element(
    By.XPATH,
    '//div[contains(text(), "Not Now")] | //button[contains(text(), "Not Now")]',
)
save_creds_not_now.click()
```

### Smashing that Like button
The rest of the script is more of the same. The React.js obfuscates the class names, and so since they're likely to change I tried to select based on the elements in the DOM.

Some things I learned along the way:

* Some elements weren't known to XPath. To find the like button which is an `<svg />`, I had to use `*[local-name()="svg"]`. Similarly, `<title />` elements needed to be identified this way `[local-name()="title"]`.
* The "dot" (`.`) is a special character in XPath that refers to the current node, and so selecting nested elements within a container could be done with something like: `//div[.//*[additional-selection]]]`
* Using a javascript click `browser.execute_script("arguments[0].click();", target_element)` was needed to trigger onclick events. I expected to be able to call `.click()` on the element, but that didn't always work.


## Complete Script

For now this script will run on my personal laptop, we I want a headless browser which can be configured in the selenium options.

```python
options = Options()
options.add_argument("--headless")
browser = webdriver.Firefox(options=options)
```


[The script](/assets/files/pylikes.py) and its running on my laptop as a docker container in daemon mode with `docker run --env-file=.env --name=pylike -it -d pylike`. The complete dockerfile is below.

```docker
# based off of https://takac.dev/example-of-selenium-with-python-on-docker-with-latest-firefox/
FROM python:3.11.5

ARG PLATFORM=aarch64
ENV PLATFORM ${PLATFORM}
ENV GECKODRIVER_VER=v0.33.0

RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y \
       firefox-esr

# install geckodriver
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux-${PLATFORM}.tar.gz \
    && tar zxf geckodriver-${GECKODRIVER_VER}-linux-${PLATFORM}.tar.gz \
    && mv geckodriver /usr/bin/

# copy application files to /app
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

WORKDIR /app

# Install test dependencies
RUN python3 -m pip install -r requirements.txt

CMD ["python3", "./main.py", "--schedule"]
```

### Next Steps

Ideally, this script is only liking posts on my behalf occasionally to avoid throttling. Some basic scheduling is needed, and there is the [schedule](https://schedule.readthedocs.io/en/stable/) package for that. Here is an hourly schedule for the script.

```
schedule.every().hour.do(job)
while True:
    schedule.run_pending()
    time.sleep(10 * 60)  # check every 10 minutes
```

It would be nice to have scheduling during the window that is waking hours. I might move this to cron or find a cron-like python package.

It might be a little bit evil, but I think using ChatGPT to comment on posts could be a useful enhancement.
