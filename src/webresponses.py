# part of webserver

def HttpResponseHeader(is404):
  if is404:
      return 'HTTP/1.1 404 Not Found\n', 'Content-Type: text/html\n', 'Connection: close\n\n'
  else:
      return 'HTTP/1.1 200 OK\n', 'Content-Type: text/html\n', 'Connection: keep-alive\n\n'
    
   
def HttpPage(is404, Status):  
    # The web server will serve either an index.html page or a 404 error page.
    # Both pages share common elements
    
    htmlTop = """<!DOCTYPE html>
      <html>
        <head>
        <title>W600-PICO Web Server Example</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <link rel="icon" href="data:,">
        <style>
        html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
        h1{color: #0F3376; padding: 2vh;}
        p{font-size: 1.5rem;}
        .button{display: inline-block; background-color: blue; border: none; border-radius: 6px;
        color: white; font-size: 1.5rem; width: 5em; height: 3em; text-decoration: none; margin: 2px; cursor: pointer;}
        .button2{background-color: silver;}
        </style>
        </head>
        <body>
        <h1>W600-PICO Web Server Example</h1>"""

    htmlBottom = "</body></html>"
    
    if is404:
      html = htmlTop + """<h1 style="color: red">404 Error</h1><p><a href="/"><button class="button button2">Return</button></a></p>""" + htmlBottom
    else:
      html = htmlTop + """<p>LED: <strong>""" + ("ON" if Status else "OFF") + """</strong></p>
      <p><a href="/?led=toggle"><button class="button">Toggle</button></a></p>
      <p><a href="/quit"><button class="button button2">Quit</button></a></p>""" + htmlBottom
    return html
