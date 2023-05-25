Need to touch the acme file first. Not sure why but it's a requirement. If you don't, traefik creates a directory not a file and gives it the wrong permissions.
`touch ./appdata/traefik2/acme/acme.json`
`chmod 600 ./appdata/traefik2/acme/acme.json`

Fill out the example .env.example file with relevant values. 
I am assuming you are using Cloudflare as the DNS host and LetsEncrypt as the SSL provider. You need to own a domain for this to work correctly! If you don't have a domain set up in Cloudflare this might still work but you won't get SSL anywhere.

The docker-compose.yml file for Traefik here was heavily influenced by [this repo](https://github.com/htpcBeginner/docker-traefik/tree/master). I needed Traefik to cooperate with Cloudflare and LetsEncrypt and this did the job nicely. I don't think it's doing wildcards correctly yet though.

