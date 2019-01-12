#!/usr/bin/env python
from cgi import parse_qs, escape
import requests

def get_metadata ( item ) :
	block = '<h2>'
	if item.get('icons'):
		block += '<img src="%s" />' % escape(item.get('icons').get('x32'))
	block += '%s - %s</h2>' % (escape(item.get('name', 'endpoint')), escape(item.get('version', 'v?')))
	block += '<p>%s</p>' % item.get('description', '<em>No Description</em>')
	if item.get('discoveryRestUrl') :
		block += '''<a href="?url={0}">Discovery</a>
		<a href="{0}" target="_blank">Discovery (raw)</a>'''.format(escape(item.get('discoveryRestUrl')))
	if(item.get('documentationLink')):
		block += '<a href="{0}" target="_blank">Documentation ({0})</a>'.format(escape(item.get('documentationLink')))
	return block

# The application interface is a callable object
def application ( env, start_response ):
	api_url = 'https://www.googleapis.com/discovery/v1/apis/'
	
	get = parse_qs(env['QUERY_STRING'])
	if(get.get('url')):
		api_url = get.get('url')[0]
	
	
	r = requests.get(api_url).json()
	
	response_body = '''<!doctype HTML>
<html>
    <head>
        <title>
            API Discovery Tool
        </title>
        <link rel="stylesheet" type="text/css" href="../php/api.css" />
    </head>
    <body>'''
	
	
	if r.get('kind'):
		if 'discovery#directoryList' == r.get('kind'):
			#iterate the list of APIs and build the metadata
			for item in r['items'] :
				response_body += '<div>%s</div>' % get_metadata(item)
				
				
		if 'discovery#restDescription' == r.get('kind'):
			#display the metadata
			response_body += '<div>' + get_metadata(r)
			
			#build a table of all the properties that are just strings
			response_body += '<table><tbody>'
			for key in r:
				if isinstance(r.get(key), basestring) :
					response_body += '<tr><td>{0}</td><td>{1}</td></tr>'.format(escape(key), escape(r.get(key, '-')))
			response_body += '</table></div>'
			
			#make an info card for each "schema"
			if(r.get('schemas')):
				for name in r.get('schemas'):
					schema = r.get('schemas').get(name)
					response_body += '''<div><h3>Schema: {0}</h3>
					<p>{1}</p>'''.format(escape(name), escape(schema.get('description', 'no description')))
					
					if schema.get('properties'):
						#build a "properties" table
						response_body += '''<h4>Properties:</h4>
						<table>
							<thead>
								<tr><th>Name</th><th>Type</th><th>Description</th>
							</thead>
							<tbody>'''
						for propname in schema.get('properties'):
							property = schema.get('properties').get(propname)
							response_body += '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>'.format(escape(propname), escape(property.get('type', '-')), escape(property.get('description', '-')))
						response_body += '</tbody></table>'
					response_body += '</div>'
	response_body += '</body></html>'
	
	response_body = bytes(response_body)
	
	# HTTP response code and message
	status = '200 OK'

	response_headers = [
		('Content-Type', 'text/html'),
		('Content-Length', str(len(response_body)))
	]

	# Start the HTTP response by sending the status and headers
	start_response(status, response_headers)

	#send the content
	return [response_body]