import tweepy
import json
import urllib2
import pprint
import json
import traceback
import unirest
import csv

# Authentication details. To  obtain these visit dev.twitter.com
consumer_key = '2BVkDqAPinK9hOQ4NjnaqWXYh'
consumer_secret = 'E0GvBjF1mz9FhW337srR8t1n1f78OdYL6cOvWmWqY81B4GV8AP'
access_token = '4005103452-6sKsWEnePpllG6XQRHnQeE3lK6BMP9xOI4UF585'
access_token_secret = '56dAfGrzb59EiSEkpNdwsYlvVmntVgTCfaoEEtbltr6Do'
contestant = 'Ted Cruz'
tweetLocation = 'undefined'

# This is the listener, responsible for receiving data
class StdOutListener(tweepy.StreamListener):
	def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
		decoded = json.loads(data)
		tweetLocation = 'undefined'
		
		if decoded['user']['location'] is not None:
			try:
				add = urllib2.quote(decoded['user']['location'])
				geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s" % add
				req = urllib2.urlopen(geocode_url)
				jsonResponse = json.loads(req.read())
				results = jsonResponse['results']
				for result in results:
					for address_component in result['address_components']:
						if address_component['types'] == ['administrative_area_level_1', 'political']:
							tweetLocation = address_component['long_name']
							break
				req.close()
				# Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
				try:
					response = unirest.post("https://community-sentiment.p.mashape.com/text/",
					headers={
					"X-Mashape-Key": "H7cPnOjDcBmshbpL4XETuuiqneyKp1nfsVUjsn7g9Nxuvma6gg",
					"Content-Type": "application/x-www-form-urlencoded",
					"Accept": "application/json"
					},
					params={
					"txt": decoded['text'].encode('ascii', 'ignore')
					}
					)
					response_body = json.loads(response.raw_body)
					sentiment_result = response_body['result']['sentiment'].encode('ascii', 'ignore')
					
					# convert the json to csv
					with open('ted.csv', 'a') as f:
						writer = csv.writer(f)
						writer.writerow([decoded['user']['id_str'],contestant,sentiment_result,tweetLocation,decoded['created_at'].encode('ascii', 'ignore')])
					

					
				except Exception as error:
					traceback.print_exc()
					print 'Exception in DatumBox or DB insert'
				return True
			except Exception as error:
				traceback.print_exc()
				print 'Exception in location!!'



if __name__ == '__main__':
	l = StdOutListener()
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	
	print "Showing all new tweets :"
	stream = tweepy.Stream(auth, l)
	stream.filter(track=['@tedcruz45', '#TedCruz2016', '#TedCruzCampaignSlogans','#Cruz2016','#TrusTed','#CruzCrew','Ted Cruz'])
	
