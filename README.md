hashtagprint
Using the Twitter API to send documents to any printer, web-enabled or not

USAGE:

Step 1: Download the zip file and extract it
Step 2: Create a twitter handle for your printer
Step 3: Go to https://apps.twitter.com/ and click create a new App
Step 4: Enter the https://github.com/rtrad/hashtagprint as the description link
Step 5: Go to the Keys and Access Tokens tab and generate your Access Token
Step 6: Note the Consumer Key (API Key), Consumer Secret (API Secret), Access Token, Access Token Secret
Step 7: Open the config.py file and paste these values under their respective names in the ouath_params dictionary
Step 8: In the config.py file paste the twitter handle for your printer under the printer_handle in the twitter_api_params dictionary and save the file
Step 9: Open the command prompt and run the __init__.py file
