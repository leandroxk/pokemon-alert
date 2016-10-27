import getpass
import smtplib
import os
import time

from unipath import Path
from os.path import expanduser

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

class PrintConsumer():

	def consume(self, search_result):
		for pokemon in search_result.pokemon():
			print '%s  %s,%s  %s' % (pokemon.name(), 
				str(pokemon.lat), str(pokemon.lng),
				str(pokemon.remaining_time()))


class FileConsumer():

	def __init__(self):
		home = expanduser("~")
		self.filename = Path(*[home, '.pokemon', 'logs', '%s.log' % time.time()])

	def consume(self, search_result):
		with open(self.filename, 'a') as f:
			for pokemon in search_result.pokemon():
				f.write('%s  %s,%s  %s %s \n' % (pokemon.name(), 
					str(pokemon.lat), str(pokemon.lng),
					str(pokemon.expiration),
					str(pokemon.encounter_id)))


class GmailConsumer():

	def __init__(self, from_mail, password, to_emails, gmap_key, encounter_filter):
		self._guser = from_mail
		self._gpass = password
		self._to_emails = to_emails
		self._filter = encounter_filter
		self._gmap_key = gmap_key

	def consume(self, search_result):
		for pokemon in search_result.pokemon():
			if self._filter.accept(pokemon):
				print 'sending email...'
				self.mail(pokemon)


	def mail(self, encounter):
		msg = MIMEMultipart()
		msg['From'] = self._guser
		msg['To'] = ", ".join(self._to_emails)
		msg['Subject'] = 'Found Pokemon: %s %s' % (encounter.name(), encounter.remaining_time())
		msg.attach(MIMEText(self._mail_text(encounter), 'html'))

		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.login(self._guser, self._gpass)
		server.sendmail(self._guser, self._to_emails, msg.as_string())
		server.close()

	def _mail_text(self, encounter):
		img_url = "https://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=16&size=800x600&maptype=roadmap&markers=color:red|label:P|%s&key=%s"
		img_url = img_url % (encounter.get_map(), encounter.get_map(), self._gmap_key)

		html =  """
		<html>
		  <head></head>
		  <body>
			<pre>
Info:
	Id:<b> %s </b> 
	Lat/Lng: %s 
	Remaining: %s 
	Maps: http://maps.google.com/maps?q=%s
		    </pre>
		    <img src=\"%s\" />
		  </body>
		</html>
		"""

		return html % (encounter.name(), encounter.get_map(), encounter.remaining_time(), encounter.get_map(), img_url)
