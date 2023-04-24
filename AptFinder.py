from FacebookScraper import FacebookScraper
from facebook_scraper import get_posts

### Facebook user: Boris Red
email = "monepoy122@gam1fy.com"
password = "6pNYqJk3YcJDAXz"
group_id = "184920528370332"


def run():
    # older_posts = get_posts('184920528370332', pages=1, timeout=30, credentials=(email, password), encoding='utf-8')
    # with open('posts.txt', 'w', encoding="utf-8") as f:
    #     for p in older_posts:
    #         f.write(p['text'])
    #         f.write('\n\n')

    # facebook_scraper = FacebookScraper(email, password, [group_id])
    # with FacebookScraper(email, password, [group_id]) as fs:
    #     older_posts = fs.get_older_posts()
    #     with open('posts.txt', 'w', encoding="utf-8") as f:
    #         for p in older_posts:
    #             f.write(p.text)
    #             f.write('\n\n')        
        # new_post = facebook_scraper.run()
        # parsed_post = PostManager.parse(new_post)
        # if PostManager.filter(parsed_post):
        #     telegram_bot.send(parsed_post)


if __name__ == '__main__':
    run()
