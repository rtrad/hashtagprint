#HashtagPrint

Using the Twitter API to send documents to any printer, web-enabled or not

Usage:

    Step 1: Download the zip file and extract it
    Step 2: Create a twitter handle for your printer
    Step 3: Go to https://apps.twitter.com/ and click create a new App
    Step 4: Enter the https://github.com/rtrad/hashtagprint as the description link
    Step 5: Go to the Keys and Access Tokens tab and generate your Access Token
    Step 6: Note the Consumer Key (API Key), Consumer Secret (API Secret), Access Token, Access Token Secret
    Step 7: Run the start.py file and paste these values under their respective names
    Step 8: In the GUI paste the twitter handle for your printer, the name of the printer device that you are going to use to print (This can be found in the control pannel) and also your own twitter handle(as the super user)
    Step 9: Press Configure and Run to start printing

Dependencies:

    pip install requests
    pip install requests_oauthlib
    pip install pdfkit
    pywin32: http://sourceforge.net/projects/pywin32/
    Python image library: http://www.pythonware.com/products/pil/
    wkhtmltopdf: http://wkhtmltopdf.org/downloads.html

