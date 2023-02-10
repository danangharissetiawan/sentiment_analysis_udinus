from scraping import Instagram
import pandas as pd


def instagram_scraping(username, password, user_name):
    instagram = Instagram()
    instagram.login_instagram(username, password)
    instagram.get_user_post(user_name)

    if pd.read_csv(f"data/instagram/{user_name}.csv").empty:
        print(f"Data {user_name}_posts.csv is empty")
    else:
        ds = pd.read_csv(f"data/instagram/{user_name}.csv")
        for i in range(len(ds)):
            url = ds['url'][i]
            instagram.get_post_comment(url)

    # instagram.get_post_comment("https://www.instagram.com/p/CnZ8wn0Jqel/")




if __name__ == '__main__':

    username = 'hinata_646'
    password = '@Hinata180900'

    user_name = 'udinusofficial'

    instagram_scraping(username, password, user_name)

