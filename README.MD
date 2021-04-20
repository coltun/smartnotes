

How to run the project locally?
1. pip install -r requirements.txt
2. telegram webhook does not work without https (localhost not suitable)
- In step 1 ngrok was installed
- Open a new terminal and run localserver (localhost8000)
- Open a new terminal and run ```ngrok http 8000``` (this will forward your localhost to a https ngrok link)
3. Make a post request with postman to:
https://api.telegram.org/[your BOT_ID ]/setWebhook?url=[Your ngrok url]/webhook/
4. Go on the browser and open the https url
5. You will see:
Invalid HTTP_HOST header: 'copy me and paste me in settings.py in ALLOWED_HOSTS'
