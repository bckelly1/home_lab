# Brian Home Lab

This is my smart home configuration. Or at least part of it. Some parts cannot be checked in.. yet :)

If you want to spin up this stack, start with Traefik. The docker-compose.yml file will spin things up if you provide the right .env file. Read the README in that folder for help.

After setting up Traefik, fill out the .env.example in this folder as well. You might not need everything but if you want something I did my best to label the required .env fields.

The final step is you need to register your subdomains with DNS. I use AdGuard as a DNS server as well as an ad blocker. After you set up one of these services you need to register it with AdGuard (or PiHole, or whatever you're using for DNS). Basically:
`subdomain.maindomain.com=<ip address of traefik server>`

I will figure out a way to add the AdGuard config to this. It's not easy because it's a flat yaml file that contains secrets (Admin Login).

## Prerequisites:
* AdGuard DNS server
* Cloudflare DNS
* You own a domain name that is configured in Cloudflare.
* Know a little bit about Docker

## Services:
* bitwarden - Home Password manager
* chronograf - Views of contents in the influx db. Should probably be demoted, I never use it.
* change_detection - Watches for changes on websites
* cloudflare-ddns - Automatically updates my public DNS record with my public IP.
* ghost - Home blog
* grafana - Visualization of data. Primarily for Unifi Poller, but I can monitor Home Assistant devices in more detail in Grafana.
* home_assistant - Home automation and monitoring hub. Everything (almost) hooks into Home Assistant for automation and monitoring purposes.
* homer - Main dashboard where I hold links to all of the different services that are running. Glorified bookmark holder in a webpage.
* mosquitto - Messaging bus for Home Assistant
* netdata - Monitors system metrics (CPU, Disk, Memory, Network traffic, etc)
* nut_server - Integration with the Network Uninterruptible Powersupply backup.
* paperless - Optical Character Recognition tools used for tagging and cataloging documents (PDF, Word, Excel, etc)
* portainer - Monitors the health, status and configuration of all Docker containers.
* redis - Caching system for paperless
* retroarch - Retro game emulation tool. Works acceptably in the browser for many games, have not got it to work for DosBox. Should probably be demoted.
* tandoori - Recipe manager! All Interesting recipes are saved here.
* unifi_poller - Monitors every metric possible from the Unifi Dream Machine Pro. Client metrics, Deep Packet Inspection, total network traffic, etc.
* uptime_kuma - Monitors all home services (docker containers) as well as any external websites.
* watchtower - Automatically keeps all docker containers up to date with the latest released images.
* wireguard - VPN.
* wyze_bridge - Allows for local control and monitoring of all Wyze devices (cameras)
* baby_sleep_coach - Experiment for monitoring the sleep/hungry status of a child. Mostly an experiment, should be moved until it is refined.


* traefik - network proxy. Allows all services to share an HTTP endpoint (80/443) rather than all services running on their own ports/colliding. It also manages SSL for all services that are connected.

### Labels
In every docker service there is a section called labels. This is how the container "registers" with traefik to use SSL and get it's connection proxied. You need four labels for every service:
```
- "traefik.enable=true" # Says yes, I want this service in Traefik
- "traefik.docker.network=$DEFAULT_NETWORK" # This is the Traefik Network in docker
- "traefik.http.routers.grafana.rule=Host(`grafana.$MY_DOMAIN`)" # Subdomain that you want. Remember to change the router in the label name!
- "traefik.http.routers.grafana.tls.certresolver=dns-cloudflare" # What certificate resolver you want Traefik to use.
- "traefik.http.services.grafana.loadbalancer.server.port=3000" # What HTTP port the service typically runs on
```