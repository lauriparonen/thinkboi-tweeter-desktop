# thinkboi-tweeter-desktop

“Simplicity is the ultimate sophistication.” Leonardo da Vinci

A simple desktop Twitter client for sending tweets less than 140 characters of length, made with Python and PyQt5.

To use the client, you need a Twitter account with a developer status - this can be obtained via https://developer.twitter.com/. 
When you have an account with access to the Twitter API, you must enter your API keys into the file api_keys.txt. You can use multiple accounts; you could for example create different text files with different account API keys, and name each <account_name>.txt and then update the line in the code 

all_keys = open("api_keys.txt", 'r').read().splitlines()

to correspond to the new account name. 

You can write the tweets to the text input, and you can choose to tweet it right away or save it into the drafts.txt file for further consideration. 
