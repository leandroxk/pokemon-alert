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

	def __init__(self, email_config, pokemon_filter):
		self._guser = email_config.send_from()
		self._gpass = email_config.password() 
		self._to_emails = email_config.send_to()
		self._gmap_key = email_config.gmap_key()
		self._cont_enable = email_config.is_continuous_enable()
		self._cont_interval = email_config.continuous_interval()
		self._filter = pokemon_filter
		self._history = {}

	def consume(self, search_result):
		for pokemon in search_result.pokemon():
			if self._filter.accept(pokemon) and not self.is_already_sent(pokemon):
				print 'sending email...'
				self.send_mail(pokemon)

	def is_already_sent(self, pokemon):
		encounter_id = pokemon.encounter_id
		if not encounter_id in self._history:
			return False

		if not self._cont_enable:
			return True

		last_time = self._history[encounter_id]
		interval_sec = (time.time() - last_time)
		interval_min = (interval_sec / 60) % 60

		if interval_min < self._cont_interval:
			return True

		return False

	def send_mail(self, encounter):
		msg = MIMEMultipart()
		msg['From'] = self._guser
		msg['To'] = ", ".join(self._to_emails)
		msg['Subject'] = 'Found Pokemon: %s %s' % (encounter.name(), encounter.remaining_time())
		msg.attach(MIMEText(self._mail_text(encounter), 'html'))

		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.login(self._guser, self._gpass)
		server.sendmail(self._guser, self._to_emails, msg.as_string())
		self._history[encounter.encounter_id] = time.time()
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
