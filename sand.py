
from playwright.sync_api import sync_playwright
from eth_account import Account
import secrets
import names
import random

# Configuration
url = "https://docs.google.com/forms/d/e/1FAIpQLSfASIO2SGcIxql_h-ScVu-lLa79wQmEAu5WWybL-s35ur8aNw/viewform"

form = ['Your Name', 'Your Email', 'Add a direct link to your Twitter entry', 'Your Wallet Address']
send = "Отправить"

print("Url: " + url)
print()

# Process
emails = []
tweets = []

with open('email.txt') as file:
	for line in file:
		emails.append(''.join(line.splitlines()))

with open('tweets.txt') as file:
	for line in file:
		tweets.append(''.join(line.splitlines()))

log = open("log.txt", "a")

for i, x in enumerate(range(len(emails))):
	priv = secrets.token_hex(32)
	private_key = "0x" + priv
	acct = Account.from_key(private_key)

	data = [names.get_full_name(), emails[i], random.choice(tweets), acct.address]

	with sync_playwright() as p:
		browser = p.chromium.launch(headless=False, slow_mo=500)
		page = browser.new_page()
		page.goto(url)

		for idx, element in enumerate(form):
			page.fill("div[data-params*='" + element + "'] [type='text']", data[idx])

		print("Name: " + data[0])
		print("E-Mail: " + data[1])
		print("Tweet: " + data[2])
		print("Wallet: " + data[3])
		print("Private key: " + private_key)
		print()

		log.write(data[0] + "\n")
		log.write(data[1] + "\n")
		log.write(data[2] + "\n")
		log.write(acct.address + "\n")
		log.write(private_key + "\n" + "\n")

		page.locator("text=" + send).click()
		page.wait_for_timeout(2000)
		browser.close()
