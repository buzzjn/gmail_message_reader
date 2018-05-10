
from __future__ import print_function
from googleapiclient import errors
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import re
from datetime import date, timedelta

'''
Authentication part. 
Use credentials.json in working dir
'''
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

'''
Returns list of today's messages - dictionary objects.
'''
def get_messages():
	today = date.today()
	# query that gets messages from today only
	query = "after: {0}".format(today.strftime('%Y/%m/%d'))

	message = service.users().messages().list(userId='me', q=query).execute()
	messages = []
	text_messages = []

	for m in message['messages']:
		message = service.users().messages().get(userId='me',id=m['id'],format='full').execute()
		messages.append(message)
	
	return messages

'''
Use regEx and cut when .?! as end of sentanse.
'''
def get_message_text():
	messages = get_messages()

	if len(messages) > 3:
		print('Today you got more than 3 messages. Print all message.')
		for m in messages:
			print( str(m['snippet'].encode('utf-8')))
			print('-------')
			
	elif len(messages) < 3:
		print('Today you got less than 3 messages. Print each odd message.')

		for m in messages:
			s = str(m['snippet'].encode('utf-8'))
			sentEnd = re.compile('[.!?]')
			sentList = sentEnd.split(s)
			#print(sentList[0])
			for i in range(len(sentList)):
				if i%2 != 0:
					print('Print each odd sentance for the current message.\n')
					print(sentList[0])
					print(sentList[i])
					print('-----------------')


if __name__ == '__main__':
	get_message_text()





