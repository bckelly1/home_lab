The files here configure fail2ban to monitor the logs and ban any IP that is making repeated failed attempts to log in.

Set up fail2ban by referencing this doc:
https://github.com/fail2ban/fail2ban/wiki/How-to-install-fail2ban-packages#debian--ubuntu

Then copy these files into the right location, ie:
/etc/fail2ban/jail.d/
/etc/fail2ban/filter.d/

and restart fail2ban
