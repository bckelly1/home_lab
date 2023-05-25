# Brian Home Lab

This is my smart home configuration. Or at least part of it. Some parts cannot be checked in.. yet :)

If you want to spin up this stack, start with Traefik. The docker-compose.yml file will spin things up if you provide the right .env file. Read the README in that folder for help.

After setting up Traefik, fill out the .env.example in this folder as well. You might not need everything but if you want something I did my best to label the required .env fields.

You will need to spin up a MySQL Database and a Postgres Database. MySQL is used primarily but some services don't support MySQL so Postgres is used there. Drop into the databases folder and spin up the databases using docker compose.

The final step is you need to register your subdomains with DNS. I use AdGuard as a DNS server as well as an ad blocker. After you set up one of these services you need to register it with AdGuard (or PiHole, or whatever you're using for DNS). Basically:
`subdomain.maindomain.com=<ip address of traefik server>`
Drop into the `adguard` folder to spin up your AdGuardHome server from there.

*The only cost for this setup is paying for the domain name. That is usually about $8/year. This is optional. You can do most of this without ever owning an official domain! You just won't have SSL*

## Prerequisites:
* You own a domain name that is configured in Cloudflare.
* Cloudflare DNS
* Know a little bit about Docker and [have it installed](https://docs.docker.com/get-docker/).
* *Optional*: NAS uses a CIFS Share. If you don't want to do a CIFS share, remove the cifs_document_backup volume from home_assistant.

## Setup Instructions
1. Fill out the .env file in the root directory as much as you can/want.
2. Fill out the .env file in the `./traefik` directory
3. Fill out the `config.yml.example` file in the `./homer` directory. (Create a `config.yml` file).
3. In the `./traefik` directory, run `docker compose up -d` to create the traefik config.
4. In the `./databases` directory (which you can run on this server or elsewhere), run `docker compose up -d`.
5. In the root directory, trim out whatever services you don't want in the `docker-compose.yml` file.
6. In the root directory, run `docker compose up -d`
7. In the `./adguard` directory, run `docker compose up -d` and then view `<ip address>:3000` to view the adguard config. Set up any users and additional config. Set up the DNS rewrites for the subdomains in the `docker-compose.yml` in the root directory.
8. Navigate to `homer.setupjustforme.com`

## Services:
* [adguard](https://github.com/AdguardTeam/AdGuardHome) - Home DNS Server. Blocks ads, custom domains/subdomains, rewrites URLs as necessary.
* [bitwarden](https://github.com/dani-garcia/vaultwarden) - Home Password manager
* [change_detection](https://github.com/dgtlmoon/changedetection.io) - Watches for changes on websites
* [cloudflare-ddns](https://github.com/timothymiller/cloudflare-ddns) - Automatically updates my public DNS record with my public IP.
* [ghost](https://hub.docker.com/_/ghost) - Home blog
* [grafana](https://github.com/grafana/grafana) - Visualization of data. Primarily for Unifi Poller, but I can monitor Home Assistant devices in more detail in Grafana.
* [home_assistant](https://github.com/home-assistant/core) - Home automation and monitoring hub. Everything (almost) hooks into Home Assistant for automation and monitoring purposes.
* [homer](https://github.com/bastienwirtz/homer) - Main dashboard where I hold links to all of the different services that are running. Glorified bookmark holder in a webpage.
* [immich](https://github.com/immich-app/immich) - Photo storage assistant. Copies and backs up photos from phones onto the NAS every night. Much like Google Photos or iCloud storage for photos.
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
I typically spin up the database and AdGuard/PiHole on a separate server, the most reliable one I have. Things go crazy on the network if the databases or DNS Server go out, so I try to keep them as stable as possible. You can put all of these on one server if you want.

I would not suggest putting all of these on a Raspberry Pi, unless you are working with a Raspberry Pi 4 4GB or above. The databases alone suck down 2 GB of RAM, and the rest of the stack uses 6 GB with everything running.

Be careful about running any of these on a Raspberry Pi by itself. The microSD card in the Raspberry pi isn't made for the logging from the services. When I first span up a Home Assistant instance on it the SD card died in about 4 months. I swapped it out with a USB SSD. For smaller scale applications this is fast enough but it's not great. I eventually moved onto a HP ProDesk 600 that I bought used for cheap.

## Suggestions
I welcome suggestions! I am always looking to improve my stack, configuration and services. Fork the repo, make your change, and open a pull request! If you have a suggestion, put it in a GitHub Issue.

## Disclaimer
I don't own the individual services. I am standing on the shoulders of giants. Thank you to all the services and applications that I have used. I do my best to contribute back where I can for each service.

With that said, I can't guarantee that each service is free of vulnerabilities, bugs and exploits. There are probably lots. It is best to try to isolate them as much as can be reasonably done.

However, I have not had a problem with any of these services. I keep them up to date with Watchtower.

