import sys

import instaloader
from datetime import datetime
from itertools import dropwhile, takewhile
import csv
import pandas as pd
import os
import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GetInstagramProfile:
    def __init__(self, username, password):
        self.L = instaloader.Instaloader()
        self.username = username
        self.password = password

    def download_users_profile_picture(self, username):
        self.L.download_profile(username, profile_pic_only=True)

    def download_users_posts_with_periode(self, username, start_date, end_date):
        profile = instaloader.Profile.from_username(self.L.context, username)
        posts = profile.get_posts()
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        posts = takewhile(lambda p: p.date > end_date, posts)
        posts = dropwhile(lambda p: p.date < start_date, posts)
        self.L.download_posts(posts, target=username)

    def download_hastag_posts(self, hastag):
        for post in instaloader.Hashtag.from_name(self.L.context, hastag).get_posts():
            self.L.download_post(post, target=hastag)

    def get_users_followers(self, username):
        self.L.login(self.username, self.password)
        profile = instaloader.Profile.from_username(self.L.context, username)
        file = open('followers.csv', 'w', newline='', encoding='utf-8')
        writer = csv.writer(file)
        writer.writerow(['username', 'full_name', 'is_private', 'is_verified', 'profile_pic_url'])
        for follower in profile.get_followers():
            writer.writerow([follower.username, follower.full_name, follower.is_private, follower.is_verified, follower.profile_pic_url])
        file.close()

    def get_users_following(self, username):
        self.L.login(self.username, self.password)
        profile = instaloader.Profile.from_username(self.L.context, username)
        file = open('following.csv', 'w', newline='', encoding='utf-8')
        writer = csv.writer(file)
        writer.writerow(['username', 'full_name', 'is_private', 'is_verified', 'profile_pic_url'])
        for following in profile.get_followees():
            writer.writerow([following.username, following.full_name, following.is_private, following.is_verified, following.profile_pic_url])
        file.close()

    def get_users_posts(self, username):
        profile = instaloader.Profile.from_username(self.L.context, username)
        file_name = f'{username}_posts.csv'
        file = open(f'data/instagram/{file_name}', 'w', newline='', encoding='utf-8')
        writer = csv.writer(file)
        writer.writerow(['caption', 'date', 'likes', 'comments', 'url'])
        comment_writer = csv.writer(open(f'data/instagram/{username}_comments.csv', 'w', newline='', encoding='utf-8'))
        for post in profile.get_posts():
            writer.writerow([post.caption, post.date, post.likes, post.comments, post.url])
            for comment in post.get_comments():
                comment_writer.writerow([comment.owner_username, comment.text])

        file.close()
        print(f'File saved as {file_name}')

    def get_post_comments(self, post_url):
        post = instaloader.Post.from_shortcode(self.L.context, post_url)
        file_name = f'{post.owner_username}_comments.csv'
        file = open(f"data/instagram/{file_name}", 'w+', newline='', encoding='utf-8')
        writer = csv.writer(file)
        writer.writerow(['username', 'text'])
        for comment in post.get_comments():
            writer.writerow([comment.owner_username, comment.text])
        file.close()

    def get_post_info_csv(self, post_url):
        post = instaloader.Post.from_shortcode(self.L.context, post_url)
        file = open('post_info.csv', 'w', newline='', encoding='utf-8')
        writer = csv.writer(file)
        writer.writerow(['caption', 'date', 'likes', 'comments'])
        writer.writerow([post.caption, post.date, post.likes, post.comments])
        file.close()

    def get_post_info(self, post_url):
        post = instaloader.Post.from_shortcode(self.L.context, post_url)
        return post.caption, post.date, post.likes, post.comments

    def get_post_comments_csv(self, post_url):
        post = instaloader.Post.from_shortcode(self.L.context, post_url)
        file = open('comments.csv', 'w', newline='', encoding='utf-8')
        writer = csv.writer(file)
        writer.writerow(['username', 'text'])
        for comment in post.get_comments():
            writer.writerow([comment.owner_username, comment.text])
        file.close()


class GetYoutubeCommand:
    def __init__(self):

        # self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.driver = Chrome(executable_path="C:/Users/mrdan/Downloads/chromedriver_win32/chromedriver.exe")

    def get_user_videos(self, username):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get(f'https://www.youtube.com/@{username}/videos')
        url_list = []
        file = open('youtube_videos.csv', 'w', newline='', encoding='utf-8')
        writer = csv.writer(file)
        writer.writerow(['title', 'url', 'views', 'date'])

        for item in range(3):
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)

            time.sleep(5)

        for video in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#video-title"))):
            writer.writerow([video.text, video.get_attribute('href'), video.get_attribute('aria-label').split(' ')[0], video.get_attribute('aria-label').split(' ')[-1]])

            url_list.append(video.get_attribute('href'))
        file.close()

        print('done')
        return url_list

    def get_youtube_command(self, url):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get(f"https://youtu.be/{url}")

        for item in range(10):
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(10)
            if item >= 1:
                try:
                    # click more comments
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#more-replies"))).click()
                    print('clicked more comments')
                    time.sleep(5)
                except Exception as e:
                    print('no more comments')
                    print(f"only {len(wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#content-text'))))} comments")
            elif item == 3 and len(wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#content-text")))) < 30:
                print(f"only {len(wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#content-text'))))} comments")
                break
            else:
                try:
                    comments = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#content-text")))
                except Exception as e:
                    print('no comments')
                    return



        file_name = url.split('=')[1] if '=' in url else url.split('/')[-1]

        file = open(f"data/comments/{file_name}.csv", 'w', newline='', encoding='utf-8')
        writer = csv.writer(file)
        writer.writerow(['text'])
        try:
            for comment in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#content-text"))):
                writer.writerow([comment.text])
        except Exception as e:
            print('no comments')
            return
        file.close()
        print(f"{file_name} with length {pd.read_csv(f'data/comments/{file_name}.csv').shape[0]} is done")

    def get_video_url_from_search(self, search):
        options = ChromeOptions()
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        self.driver = Chrome(chrome_options=options, executable_path="C:/Users/mrdan/Downloads/chromedriver_win32/chromedriver.exe")
        wait = WebDriverWait(self.driver, 30)
        self.driver.get("https://www.youtube.com/")

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input#search"))).send_keys(search)

        self.driver.find_element(By.CSS_SELECTOR, "button.style-scope.ytd-searchbox#search-icon-legacy").click()

        file = open(f"data/{search}.csv", 'w', newline='', encoding='utf-8')
        writer = csv.writer(file)
        writer.writerow(['title', 'url', 'url_id'])
        url_list = []

        for item in range(10):
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)

            time.sleep(5)

        for video in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a.yt-simple-endpoint.style-scope.ytd-video-renderer#video-title"))):
            title = video.text
            url = video.get_attribute('href')
            url_id = url.split('=')[1] if '=' in url else url.split('/')[-1]
            writer.writerow([title, url, url_id])
            url_list.append(url)

        file.close()

        print('done')
        return url_list

    def get_video_url_from_channel(self, channel, num_video):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get(f'https://www.youtube.com/channel/{channel}/videos')

        for video in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a.yt-simple-endpoint.style-scope.ytd-video-renderer#video-title"))):
            return video.get_attribute('href')


# Scraping Instagram Comments with Selenium

class Instagram:
    def __init__(self):
        self.driver = None

    def login_instagram(self, username, password):
        options = ChromeOptions()
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        self.driver = Chrome(chrome_options=options, executable_path="C:/Users/mrdan/Downloads/chromedriver_win32/chromedriver.exe")
        wait = WebDriverWait(self.driver, 30)
        self.driver.get("https://www.instagram.com/accounts/login/")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))).send_keys(username)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))).send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(5)

    def get_user_post(self, user):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get(f"https://www.instagram.com/{user}/")
        time.sleep(5)
        write = open(f"data/instagram/{user}.csv", 'w', newline='', encoding='utf-8')
        writer = csv.writer(write)
        writer.writerow(['url'])

        # scroll
        # scrolldown = self.driver.execute_script(
        #     "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        # match = False
        # while (match == False):
        #     last_count = scrolldown
        #     time.sleep(3)
        #     scrolldown = self.driver.execute_script(
        #         "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        #     if last_count == scrolldown:
        #         match = True

        for item in range(10):
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)

            time.sleep(5)

        # for post in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a"))):

        # get post url
        post_url = []
        link = self.driver.find_elements(By.CSS_SELECTOR, "a")
        for i in link:
            post = i.get_attribute('href')
            if '/p/' in post:
                post_url.append(post)
                writer.writerow([post])

        # get comment
        # for url in post_url:
        #     self.driver.get(url)
        #     time.sleep(5)
        #     try:
        #         for comment in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span"))):
        #             writer.writerow([comment.text])
        #     except Exception as e:
        #         print('no comments')
        #         break
        #
        # write.close()

    def get_post_comment(self, url):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get(url)
        file_name = url.split('/')[-2]
        time.sleep(5)
        write = open(f"data/instagram/comments/{file_name}.csv", 'w', newline='', encoding='utf-8')
        writer = csv.writer(write)
        writer.writerow(['comment'])

        # load more comment
        try:
            loadmore = self.driver.find_element(By.CSS_SELECTOR, "._ab8w._ab94._ab99._ab9h._ab9m._ab9p._abcj._abcm > ._abl-")
            print(f"load more comment {loadmore}")
            while loadmore.is_displayed():
                loadmore.click()
                time.sleep(5)
                loadmore = self.driver.find_element(By.CSS_SELECTOR, "._ab8w._ab94._ab99._ab9h._ab9m._ab9p._abcj._abcm > ._abl-")
                print(f"load more comment {loadmore}")

        except Exception as e:
            print('no more comment')

        # get comment
        try:
            for comment in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "._aacl._aaco._aacu._aacx._aad7._aade"))):
                writer.writerow([comment.text])

        except Exception as e:
            print('no comments')

        write.close()
        length = len(open(f"data/instagram/comments/{file_name}.csv", 'r', encoding='utf-8').readlines())
        print(f'{file_name} has {length} comments. DONE')

