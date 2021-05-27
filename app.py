from flask import Flask,render_template,request,jsonify,send_file
from os import system

app = Flask(__name__)

@app.route('/')
def welcome():
  return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /result is accessed directly. Try going to '/' and Enter domain"
    if request.method == 'POST':
        form_data = request.form
        domain = form_data['domain']
        system('./subfinder -silent -d {} > domains/{}.txt'.format(domain, domain))
        aa = open('doms/{}.txt'.format(domain), 'r')
        bb = aa.readlines()
        aa.close()
        for i in range(len(bb)):
          bb[i] = bb[i].rstrip('\n')
        f = open('templates/{}.html'.format(domain),'w')
        f.write('''
	<!DOCTYPE html>
	<html lang="en">
	<head>
	<title>Subdomain Enumerator by Gokul</title>
	  <meta charset="utf-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1">
	  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
	  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
	  <style>
	    .navbar {
	      margin-bottom: 0;
	      border-radius: 0;
	    }

	    footer {
	      background-color: #f2f2f2;
	      padding: 25px;
	    }
	  </style>
	</head>
	<body>

	<nav class="navbar navbar-inverse">
	  <div class="container-fluid">
	    <div class="navbar-header">
	      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
	        <span class="icon-bar"></span>
	        <span class="icon-bar"></span>
	        <span class="icon-bar"></span>
	      </button>
	      <a class="navbar-brand" href="#"><center>Subdomain Enumerator</center></a>
	    </div>
	    <div class="collapse navbar-collapse" id="myNavbar">
	      <ul class="nav navbar-nav">
	      </ul>
	      <ul class="nav navbar-nav navbar-right">
	      </ul>
	    </div>
	  </div>
	</nav>

	<div class="jumbotron">
	  <div class="container text-center">
	    <h3>Enter Domain</h3>
	    <form action="/result" method="POST">
	    <input type="text" name="domain">
	    <br><br><input type=submit value=submit>
	    </form>
	  </div>
	</div>

	<b><h3><center>Subdomains Found are 
	''')

	# adding all found subdomains using <li> tag and for loop
        f.write(' {}</center></h3></b><br><p><center><form method="post" action="download/{}.txt"><button type="submit">Download results!</button></form></center><br><p><ul>'.format(str(len(bb)), domain))
        for i in bb:
          f.write('<li> {}\n'.format(i))

        f.write('''
	</ul>
	<br><br><br><br>
	<footer class="container-fluid text-center">
	  <p>Created By Gokul</p>
	</footer>

	</body>
	</html>
	  </div>
	</div><br><br>
''')

        f.close()
        return render_template('{}.html'.format(domain))


@app.route('/download/<filename>', methods=['GET', 'POST'])
def download(filename):
   if request.method == "GET":
     return "The result is accessed directly go to / and enter domain to download results"
   if request.method == "POST":
     return send_file('./domains/{}'.format(filename), as_attachment=True, mimetype='txt')


app.run()
