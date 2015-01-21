#coding:utf-8
# author: Ke Mao
import sqlite3

output = open( 'data.js', 'w' )
output.write("var codropsEvents = {\n")

# sqlite db
con = sqlite3.connect("data.db")
# auto commit
con.isolation_level = None
cur = con.cursor()

date_events = dict()

for event in cur.execute('SELECT * FROM event ORDER BY date, title'):
	
	(url, date, title, location, source) = event
	if date_events.has_key( date ):
		pass
	else:
		date_events[ date ] = []
	date_events[ date ].append( event )

for key in sorted( date_events.keys() ):

	date = key[5:7] + '-' + key[8:10] + '-' + key[0:4]
	output.write("'" + date + "': [")

	for event in date_events[ key ]:
		(url, date, title, location, source) = event
		title = title.replace("'", "").replace('"', '')
		location = location.replace("'", "").replace('"', '')

		if source == 'facebook':
			output.write( ("'<a " ).encode("utf-8")  )
		else:
			output.write( ("'<a " ).encode("utf-8")  )

		if location == '':
			output.write( ("href=\"" + url + '" target="_blank">' + title + "</a>',\n").encode("utf-8")  )
		else:
			output.write( ("href=\"" + url + '" target="_blank">' + title + ' @ ' + location + "</a>',\n").encode("utf-8")  )
	output.write("],\n\n");

output.write("};")
output.close()

