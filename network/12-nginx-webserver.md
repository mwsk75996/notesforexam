# Nginx webserver

Nginx er en webserver. Den kan bruges til at vise en hjemmeside, servere statiske filer eller sende requests videre til et andet program som reverse proxy.

Typisk flow:

```text
Client/browser -> DNS -> webserver IP -> TCP port 80/443 -> nginx -> website/backend
```

Vigtige porte:

```text
HTTP   TCP port 80
HTTPS  TCP port 443
```

## Vigtige ord

- Webserver: program der svarer på HTTP/HTTPS requests
- Server block: konfiguration for et bestemt domæne eller site
- `server_name`: domænenavnet nginx matcher på
- `root`: mappe med statiske filer
- `index`: standardfil, fx `index.html`
- `location`: regel for en bestemt URL/path
- Reverse proxy: nginx modtager request og sender den videre til en backend
- Access log: requests der rammer serveren
- Error log: fejl i nginx eller backend-forbindelsen

## Installation og service

Debian/Ubuntu:

```sh
sudo apt install nginx
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx
```

Arch/CachyOS:

```sh
sudo pacman -S nginx
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx
```

Tjek at nginx lytter:

```sh
sudo ss -tulpn | grep ':80'
```

## Simpel statisk webside

Eksempel på server block:

```nginx
server {
    listen 80;
    server_name awesome.dk;

    root /var/www/awesome;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

På Debian/Ubuntu ligger site-konfigurationer ofte her:

```text
/etc/nginx/sites-available/
/etc/nginx/sites-enabled/
```

Aktiver et site:

```sh
sudo ln -s /etc/nginx/sites-available/awesome /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

`nginx -t` tester om konfigurationen er gyldig, før man reloader servicen.

## Reverse proxy

Nginx kan også stå foran et andet program, fx en backend der kører på port `3000`.

Eksempel:

```nginx
server {
    listen 80;
    server_name api.awesome.dk;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Her er det kun nginx der behøver være synlig på netværket. Backend-programmet kan køre lokalt på serveren og behøver ikke være åbent direkte fra klienterne.

## DNS, firewall og SRX

For at klienter kan ramme nginx med et navn, skal DNS pege på webserverens IP:

```text
awesome.dk -> 192.168.11.2
```

Hvis klient og server ligger på forskellige subnets, skal routing virke. Hvis der er SRX/firewall imellem, skal der også være en security policy der tillader HTTP/HTTPS.

Eksempel:

```text
USERLAN -> SERVERLAN -> HTTP tilladt
```

På SRX kan HTTP matche `junos-http`. Hvis webserveren kører på en anden port end `80`, skal man bruge en custom application.

Hvis serveren skal nås udefra, skal man også tænke på:

- NAT/port forwarding
- DNS-navn der peger på den offentlige IP
- firewall policy for port `80` og/eller `443`
- TLS certificate hvis HTTPS bruges

## Test og fejlfinding

Test fra klient:

```sh
curl -I http://192.168.11.2
curl http://awesome.dk
ping 192.168.11.2
```

Tjek logs på server:

```sh
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u nginx -n 50
```

Wireshark-filtre:

```text
http
tcp.port == 80
tcp.port == 443
```

God eksamensforklaring:

Nginx er applikationslaget oven på TCP. Før browseren kan hente websiden, skal DNS finde IP-adressen, routing skal kunne nå serveren, TCP handshake skal gennemføres, og firewall/SRX skal tillade trafikken. Derefter sender browseren en HTTP request, og nginx svarer med HTML, filer eller videresender requesten til en backend.
