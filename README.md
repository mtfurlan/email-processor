# automations triggered by email

## plan
* run runner.py on a cronjob
* runner lists all emails in the inbox
* runner fetches each email one at a time
* find each plugin that wants to handle that sender or whatever
* run each one
* if all succeed, runner archives the email on the server

plugin requirements
* idempotent
