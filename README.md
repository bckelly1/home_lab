# Brian Home Lab

This is my smart home configuration. Or at least part of it. Some parts cannot be checked in.. yet :)

If you want to spin up this stack, start with Traefik. The docker-compose.yml file will spin things up if you provide the right .env file. Read the README in that folder for help.

After setting up Traefik, fill out the .env.example in this folder as well. You might not need everything but if you want something I did my best to label the required .env fields.

You will need to spin up a MySQL Database and a Postgres Database. MySQL is used primarily but some services don't support MySQL so Postgres is used there. Drop into the databases folder and spin up the databases using docker compose.

The final step is you need to register your subdomains with DNS. I use AdGuard as a DNS server as well as an ad blocker. After you set up one of these services you need to register it with AdGuard (or PiHole, or whatever you're using for DNS). Basically:
`subdomain.maindomain.com=<ip address of traefik server>`
Drop into the `adguard` folder to spin up your AdGuardHome server from there.

## Prerequisites:
* Cloudflare DNS
* You own a domain name that is configured in Cloudflare.
* Know a little bit about Docker
* *Optional*: NAS uses a CIFS Share. If you don't want to do a CIFS share, remove the cifs_document_backup volume from home_assistant.

## Services:
* [adguard](https://github.com/AdguardTeam/AdGuardHome) - Home DNS Server. Blocks ads, custom domains/subdomains, rewrites URLs as necessary.
* [bitwarden](https://github.com/dani-garcia/vaultwarden) - Home Password manager
* [change_detection](https://github.com/dgtlmoon/changedetection.io) - Watches for changes on websites
* [cloudflare-ddns](https://github.com/timothymiller/cloudflare-ddns) - Automatically updates my public DNS record with my public IP.
* [ghost](https://hub.docker.com/_/ghost) - Home blog
* [grafana](https://github.com/grafana/grafana) - Visualization of data. Primarily for Unifi Poller, but I can monitor Home Assistant devices in more detail in Grafana.
* [home_assistant](https://github.com/home-assistant/core) - Home automation and monitoring hub. Everything (almost) hooks into Home Assistant for automation and monitoring purposes.
* [homer](https://github.com/bastienwirtz/homer) - Main dashboard where I hold links to all of the different services that are running. Glorified bookmark holder in a webpage.
* [mosquitto](https://github.com/eclipse/mosquitto) - MQTT Messaging bus for Home Assistant
* [netdata](https://github.com/netdata/netdata) - Monitors system metrics (CPU, Disk, Memory, Network traffic, etc)
* [nut_server](https://hub.docker.com/r/instantlinux/nut-upsd) - Integration with the Network Uninterruptible Powersupply backup.
* [paperless](https://github.com/paperless-ngx/paperless-ngx) - Optical Character Recognition tools used for tagging and cataloging documents (PDF, Word, Excel, etc)
* [portainer](https://github.com/portainer/portainer) - Monitors the health, status and configuration of all Docker containers.
* [redis](https://github.com/redis/redis) - Caching system for paperless
* [tandoori](https://github.com/TandoorRecipes/recipes) - Recipe manager! All Interesting recipes are saved here.
* [unifi_poller](https://github.com/unpoller/unpoller) - Monitors every metric possible from the Unifi Dream Machine Pro. Client metrics, Deep Packet Inspection, total network traffic, etc.
* [uptime_kuma](https://github.com/louislam/uptime-kuma) - Monitors all home services (docker containers) as well as any external websites.
* [watchtower](https://github.com/containrrr/watchtower) - Automatically keeps all docker containers up to date with the latest released images.
* [wireguard](https://github.com/linuxserver/docker-wireguard) - VPN.
* [wyze_bridge](https://github.com/mrlt8/docker-wyze-bridge) - Allows for local control and monitoring of all Wyze devices (cameras)


* [traefik](https://github.com/traefik/traefik) - network proxy. Allows all services to share an HTTP endpoint (80/443) rather than all services running on their own ports/colliding. It also manages SSL for all services that are connected


### Labels
In every docker service there is a section called labels. This is how the container "registers" with traefik to use SSL and get it's connection proxied. You need four labels for every service:
```
- "traefik.enable=true" # Says yes, I want this service in Traefik
- "traefik.docker.network=$DEFAULT_NETWORK" # This is the Traefik Network in docker
- "traefik.http.routers.grafana.rule=Host(`grafana.$MY_DOMAIN`)" # Subdomain that you want. Remember to change the router in the label name!
- "traefik.http.routers.grafana.tls.certresolver=dns-cloudflare" # What certificate resolver you want Traefik to use.
- "traefik.http.services.grafana.loadbalancer.server.port=3000" # What HTTP port the service typically runs on
```

## Intended use case notes
One note; I typically spin up the database and AdGuard/PiHole on a separate server, the most reliable one I have. Things go crazy on the network if the databases or DNS Server go out, so I try to keep them as stable as possible. You can put all of these on one server if you want.
I would not suggest putting all of these on a Raspberry Pi, unless you are working with a Raspberry Pi 4 4GB or above. The databases alone suck down 2 GB of RAM, and the rest of the stack uses 6 GB with everything running.
