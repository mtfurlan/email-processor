# automations triggered by email

## plan
* run runner.py on a cronjob
* runner lists all emails in the inbox
* runner fetches each email one at a time
* runner runs plugins in plugins/ till one handles it
* runner archives the email on the server
