import facebook
import requests

# Prompt the user to enter their Facebook credentials, Facebook group name, and a list of words to monitor for in the Facebook group
email = "monepoy122@gam1fy.com"
password = "6pNYqJk3YcJDAXz"
user_access_token = "EAARLtz0aLMQBAONvUfxqg5G5kkYM44UBRNtpRBkrJCLwpAOegqbQwqRFGA9V8wDuAGZANIkVhnGCrSDpa2tSXp5FywBy5jqLekOt2rbFUW1FEZAzdZC2gZCw4dz5aUEOX9Q49Kxb3ZC5ZBGnZCZAZA09hKmmqHHtlYU60LYIIK5O8ZCeKvKK6BbaMZC2gEWwWMBOD4Xgty5e8O9ozgpCWnVNJz0dg11KmPb6Vi6Co68G9fBohH9ro5taZCF1j2mva5HjEaUZD"
group_id = "184920528370332" # input("Enter the name of the Facebook group to monitor: ")
words_to_monitor = "hey,hi,2" # input("Enter a comma-separated list of words to monitor: ").split(',')

# Log in to Facebook using the user's credentials
session = requests.Session()
session.verify = True
session.auth = (email, password)

# Retrieve the ID of the Facebook group based on its name
graph = facebook.GraphAPI(access_token=user_access_token, version="3.0")
import pdb; pdb.set_trace()
groups = graph.get_object('me/groups')
found_group = False
for group in groups['data']:
    if group['id'] == group_id:
        group_id = group['id']
        found_group = True
        break
if not found_group:
    print("Could not find Facebook group with id: " + group_id)
    exit()

# Fetch the posts in the Facebook group
posts = graph.get_connections(group_id, "feed")

# Loop through the posts and check if any of them contain any of the words in the user's list of words to monitor
for post in posts['data']:
    if 'message' in post:
        message = post['message']
        for word in words_to_monitor:
            if word in message:
                print("Found post containing monitored word: " + word)
                print("Post details:")
                print("Message: " + message)
                print("Link: " + post['link'])
                break
