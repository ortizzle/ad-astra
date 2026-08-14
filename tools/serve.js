/* Tiny static server for the test harness — python http.server resets
   connections under the SW's re-fetch pattern, which poisons update tests. */
const http = require('http'), fs = require('fs'), path = require('path');
const [dir, port] = process.argv.slice(2);
const MIME = {'.html':'text/html','.js':'text/javascript','.json':'application/json',
  '.svg':'image/svg+xml','.png':'image/png'};
http.createServer((req,res)=>{
  const u = decodeURIComponent(req.url.split('?')[0]);
  let f = path.join(dir, u === '/' ? 'index.html' : u);
  fs.readFile(f, (err,data)=>{
    if(err){ res.writeHead(404); res.end('nope'); return; }
    res.writeHead(200, {'Content-Type': MIME[path.extname(f)]||'application/octet-stream',
      'Cache-Control':'no-store'});
    res.end(data);
  });
}).listen(+port, ()=>console.log('serving', dir, 'on', port));
