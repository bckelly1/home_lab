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
* *Optional*: NAS uses a CIFS Mount. It's easiest if you have the system mount the share as a volume and then all services 
that need a network mount can reference it. This avoids having dozens of services have their own CIFS shares active. To set up a CIFS mount on boot, add this to /etc/fstab:
```
# Mount the nas on startup
//<IP ADDRESS>/<Mount Name> /mnt/nas cifs credentials=/PATH/TO/CREDENTIALS/FILE/.cifs-nas 0 0
```
And the credentials file (.cifs-nas) should have:
```
username=<Mount Username>
password=<Mount Password>
```

## Setup Instructions
1. Fill out these example files:
- `./.env.example` -> `./.env`
- `./traefik/.env.example` -> `./traefik/.env`
- `./databases/.env.example` -> `./databases/.env`
- `./adguard/config/AdGuardHome.yml.example` -> `./adguard/config/AdGuardHome.yml`
- `./homer/data/config.yml.example` -> `./homer/data/config.yml` Mostly you just need to replace `exampledomain.com` with whatever your domain is. Homer is very basic, you can't pass it the domain as a var.
2. In the `./traefik` directory, run `docker compose up -d` to create the traefik config.
3. In the `./databases` directory (which you can run on this server or elsewhere), run `docker compose up -d`.
4. In the root directory, pick which service you want to use and run. Inside the directory run `docker compose up -d`.
6. In the `./adguard` directory, run `docker compose up -d` and then view `<ip address>:3000` to view the adguard config. Set up any users and additional config. Set up the DNS rewrites for the subdomains in the `docker-compose.yml` in the application directory you chose in #4.
7. Navigate to `homer.exampledomain.com (put in your domain)`

## Services:
* [adguard](https://github.com/AdguardTeam/AdGuardHome) - Home DNS Server. Blocks ads, custom domains/subdomains, rewrites URLs as necessary.
* [audiobookshelf](https://github.com/advplyr/audiobookshelf) - eBook Manager. Allows for reading eBooks and listening to Audiobook MP3s. Like Plex for Audiobooks.
* [bitwarden](https://github.com/dani-garcia/vaultwarden) - Home Password manager
* [change_detection](https://github.com/dgtlmoon/changedetection.io) - Watches for changes on websites
* [cloudflare-ddns](https://github.com/timothymiller/cloudflare-ddns) - Automatically updates my public DNS record with my public IP.
* [cura](https://github.com/Ultimaker/Cura) - 3d Printer Slicer.
* [ghost](https://hub.docker.com/_/ghost) - Home blog
* [grafana](https://github.com/grafana/grafana) - Visualization of data. Primarily for Unifi Poller, but I can monitor Home Assistant devices in more detail in Grafana.
* [home_assistant](https://github.com/home-assistant/core) - Home automation and monitoring hub. Everything (almost) hooks into Home Assistant for automation and monitoring purposes.
* [home_lab_apis](https://github.com/bckelly1/home_lab_apis) - Where I write some of my custom APIs and web interfaces.
* [homer](https://github.com/bastienwirtz/homer) - Main dashboard where I hold links to all of the different services that are running. Glorified bookmark holder in a webpage.
* [immich](https://github.com/immich-app/immich) - Photo storage assistant. Copies and backs up photos from phones onto the NAS every night. Much like Google Photos or iCloud storage for photos.
* [jellyfin](https://github.com/jellyfin/jellyfin) - Media management platform. Like Plex, but open source and a bit more flexible.
* [linkding](https://github.com/sissbruecker/linkding/tree/master) - Link Manager. I copy interesting URLs into here to look into later. Sort of like bookmarks but maybe not as permanent.
* [mosquitto](https://github.com/eclipse/mosquitto) - MQTT Messaging bus for Home Assistant
* [netdata](https://github.com/netdata/netdata) - Monitors system metrics (CPU, Disk, Memory, Network traffic, etc)
* [nut_server](https://hub.docker.com/r/instantlinux/nut-upsd) - Integration with the Network Uninterruptible Powersupply backup.
* [openwebrx](https://github.com/jketterl/openwebrx) - SDR (Software Defined Radio). Allows you to listen to Ham Radio broadcasts.
* [paperless](https://github.com/paperless-ngx/paperless-ngx) - Optical Character Recognition tools used for tagging and cataloging documents (PDF, Word, Excel, etc)
* [portainer](https://github.com/portainer/portainer) - Monitors the health, status and configuration of all Docker containers.
* [redis](https://github.com/redis/redis) - Caching system for paperless
* [stirling-pdf](https://github.com/Stirling-Tools/Stirling-PDF/tree/main) - Tool for splitting, merging, modifying, managing PDF files.
* [tandoori](https://github.com/TandoorRecipes/recipes) - Recipe manager! All Interesting recipes are saved here.
* [unifi_poller](https://github.com/unpoller/unpoller) - Monitors every metric possible from the Unifi Dream Machine Pro. Client metrics, Deep Packet Inspection, total network traffic, etc.
* [uptime_kuma](https://github.com/louislam/uptime-kuma) - Monitors all home services (docker containers) as well as any external websites.
* [watchtower](https://github.com/containrrr/watchtower) - Automatically keeps all docker containers up to date with the latest released images.
* [wireguard](https://github.com/linuxserver/docker-wireguard) - VPN.
* [wyze_bridge](https://github.com/mrlt8/docker-wyze-bridge) - Allows for local control and monitoring of all Wyze devices (cameras)
* [zap2xml](https://github.com/jef/zap2xml) - Downloads a TV guide for your local broadcasts so Jellyfin can show a guide and be able to tune into Over-The-Air broadcasts.


* [traefik](https://github.com/traefik/traefik) - network proxy. Allows all services to share an HTTP endpoint (80/443) rather than all services running on their own ports/colliding. It also manages SSL for all services that are connected. When Traefik is initially started, allow it to pull the wildcard SSL cert. Check in the acme.json file for a wildcard cert. Once it appears, you can then add whatever services you want and they will all use the wildcard cert.


### Labels
In every docker service there is a section called labels. This is how the container "registers" with traefik to use SSL and get it's connection proxied. You need four labels for every service:
```
- "traefik.enable=true" # Says yes, I want this service in Traefik
- "traefik.docker.network=$DEFAULT_NETWORK" # This is the Traefik Network in docker
- "traefik.http.routers.grafana.rule=Host(`grafana.$MY_DOMAIN`)" # Subdomain that you want. Remember to change the router in the label name!
- "traefik.http.routers.grafana.tls.certresolver=dns-cloudflare" # OPTIONAL: What certificate resolver you want the service to use. If you set this, you will get a dedicated cert, not the wildcard cert.
- "traefik.http.services.grafana.loadbalancer.server.port=3000" # What HTTP port the service typically runs on
```
Most services are very upfront about what port they use for the UI, but you may need to check the Dockerfile in the service to see what they expose.

## Cronjobs
Scheduled runs of maintenance tasks, services and scripts. I use it to take manual backups of the entire home_lab directory every night. It isn't active cronjob file, it must be registered with cron in order to operate. You would need to modify the paths inside the scripts too.

## Network Configuration
* Wifis - All IoT devices are on a segregated network, with forced client isolation. Most IoT devices are not allowed to reach back to the internet.
* DNS Rewrites - The router is configured to send all clients a custom DNS server (AdGuardHome IP Address) as the preferred DNS provider and fallback to quad 9 (9.9.9.9). That allows all clients to not only utilize the Ad Blocker, and connect to the custom DNS services (Bitwarden, Home Assistant, etc).

## Intended use case notes
I typically spin up the database and AdGuard/PiHole on a separate server, the most reliable one I have. Things go crazy on the network if the databases or DNS Server go out, so I try to keep them as stable as possible. You can put all of these on one server if you want.

I would not suggest putting all of these on a Raspberry Pi, unless you are working with a Raspberry Pi 4 4GB or above. The databases alone suck down 2 GB of RAM, and the rest of the stack uses 6 GB with everything running.

Be careful about running any of these on a Raspberry Pi by itself. The microSD card in the Raspberry pi isn't made for the logging from the services. When I first span up a Home Assistant instance on it the SD card died in about 4 months. I swapped it out with a USB SSD. For smaller scale applications this is fast enough but it's not great. I eventually moved onto a HP ProDesk 600 that I bought used for cheap. It has been solid ever since.

## Suggestions
I welcome suggestions! I am always looking to improve my stack, configuration and services. Fork the repo, make your change, and open a pull request! If you have a question or suggestion, put it in a GitHub Issue or Discussion.

## Future
- Geo trackers - Google kind of gets there but I'm not super pleased with that.
- Health trackers - Apple probably has the best ones on the market right now but I would prefer a fully local system.



## Disclaimer
I don't own the individual services. I am standing on the shoulders of giants. Thank you to all the services and applications that I have used. I do my best to contribute back where I can for each service.

With that said, I can't guarantee that each service is free of vulnerabilities, bugs and exploits. There are probably lots. It is best to try to isolate them as much as can be reasonably done.

However, I have not had a problem with any of these services. I keep them up to date with Watchtower.

I haven't checked in a lot of my personal configuration because A) it won't make sense because it's tailored to my hardware and B) It either has secrets or I'm not sure if it would expose sensitive info. Reach out to me if you want clarification on something!
