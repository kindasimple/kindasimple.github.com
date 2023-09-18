#!/usr/bin/env python
import functools
import logging
import os
import random
import time
from time import sleep
from typing import List

import click
import schedule
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

logger = logging.getLogger(__name__)


def get_delay(delay_seconds: int = 2, jitter: int = 1):
    return delay_seconds + random.randint(0, jitter)


def run(username: str, password: str, profiles: List[str]):
    """
    Log into the account with the credentials and like the posts of the profiles
    """
    logger.info("Initializing headless selenium browser")
    # start the session
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    browser.implicitly_wait(5)
    browser.get("https://www.instagram.com/")

    logger.info("Starting the session for login: %s", username)

    # complete login form and log in to instagram
    input_username = browser.find_element(By.NAME, "username")
    input_username.send_keys(username)
    input_password = browser.find_element(By.NAME, "password")
    input_password.send_keys(password)
    login = browser.find_element(
        By.XPATH, '//button[descendant-or-self::*[contains(text(), "Log in")]]'
    )
    login.submit()

    # dismiss the dialog boxes
    while True:
        try:
            logger.info("Searching for dialog boxes to dismiss")

            save_creds_not_now = browser.find_element(
                By.XPATH,
                '//div[contains(text(), "Not Now")] | //button[contains(text(), "Not Now")]',
            )
        except NoSuchElementException:
            logger.error("No further dialog boxes to dismiss")
            break
        logger.info("Dialog box found. Dismissing")
        save_creds_not_now.click()

    # loop through the profiles and hit the likes!
    for profile in profiles:
        # Open the users profile page
        logger.info("Get profile page for %s", profile)
        browser.get(f"https://www.instagram.com/{profile}/")
        sleep(get_delay())

        # get the links to all the posts
        anchors = browser.find_elements(By.XPATH, "//article//*[self::a]")

        # loop through the posts and
        for index, active in enumerate(anchors, start=1):
            logger.info("Liking post %d of %d", index, len(anchors))
            browser.execute_script("arguments[0].scrollIntoView();", active)
            sleep(get_delay())
            browser.execute_script("arguments[0].click();", active)
            sleep(get_delay())
            # find unlike button and skip liking if already liked
            unlike_icon = browser.find_elements(
                By.XPATH,
                '//div[.//div[.//span[.//*[local-name()="svg"][.//*[local-name()="title"][contains(text(), "Unlike")]]]]]',
            )
            if not unlike_icon:
                # find the like button
                like_icon = browser.find_elements(
                    By.XPATH,
                    '//div[.//div[.//span[.//*[local-name()="svg"][.//*[local-name()="title"][contains(text(), "Like")]]]]]',
                )
                if like_icon:
                    browser.execute_script("arguments[0].click();", like_icon[-1])
                    logger.info("Post liked")
            else:
                logger.info("Post already liked. Skipping")
            # close the popup for the active window
            close_icon = browser.find_elements(
                By.XPATH,
                '//div[.//div[.//*[local-name()="svg"][.//*[local-name()="title"][contains(text(), "Close")]]]]',
            )
            browser.execute_script("arguments[0].click();", close_icon[-1])

    # exit the browser
    logger.info("Exiting the browser")
    browser.close()


def scheduler(username: str, password: str, profiles: List[str]):
    job = functools.partial(run, username, password, profiles)
    logger.info("Scheduling job (Hourly)")
    schedule.every().hour.do(job)
    # schedule.every().day.at("15:41").do(job)
    while True:
        logger.info("Scheduling jobs")
        schedule.run_pending()
        time.sleep(10 * 60)  # wait 10 minutes


@click.command()
@click.option("--schedule", is_flag=True, default=False)
def main(schedule: bool):
    username = os.environ.get("IG_USERNAME")
    password = os.environ.get("IG_PASSWORD")
    profiles = os.environ.get("IG_PROFILES").split(",")

    if schedule:
        scheduler(username, password, profiles)
    else:
        run(username, password, profiles)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
