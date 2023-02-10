from scraping import GetInstagramProfile, GetYoutubeCommand
import pandas as pd
# username = str(input('Enter your username: '))
# password = str(input('Enter your password: '))


def instagram_scraping(username, password, user_name):
    instagram = GetInstagramProfile(username, password)
    # instagram.get_users_followers(username)
    # instagram.get_users_following(username)
    instagram.get_users_posts(user_name)
    # if pd.read_csv(f"data/instagram/{user_name}_posts.csv").empty:
    #     print(f"Data {user_name}_posts.csv is empty")
    # else:
    #     ds = pd.read_csv(f"data/instagram/{user_name}_posts.csv")
    #     for i in range(len(ds)):
    #         url = ds['url'][i]
    #         instagram.get_post_comments(url)
    #         if pd.read_csv(f"data/instagram/{user_name}_comments.csv").empty:
    #             print(f"Data {user_name}_comments.csv is empty")
    #         else:
    #             print(f"Data {user_name}_comments.csv is not empty")


def youtube_scraping():
    yt = GetYoutubeCommand()

    ds = pd.read_csv(f"data/UDINUS.csv")
    for i in range(len(ds)):
        url = ds['url_id'][i]
        yt.get_youtube_command(url)
    # yt.get_youtube_command("ePc5Kk9swaA")
    # url_list = yt.get_video_url_from_search('udinus')
    # print(url_list)


if __name__ == '__main__':

    username = 'hinata_646'
    password = '@Hinata180900'

    user_name = 'curhatan.udinus'
    instagram_scraping(username, password, user_name)

    # youtube_scraping()
