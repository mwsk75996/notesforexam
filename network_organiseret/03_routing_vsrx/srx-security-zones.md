# SRX security zones og policies

Juniper SRX er både router og firewall.

Interfaces placeres i security zones.

Trafik mellem zoner bliver kun tilladt hvis der findes en policy der matcher trafikken.

Eksempel:

```text
USERLAN -> SERVERLAN -> HTTP tilladt
USERLAN -> INTERNET -> tilladt
GUEST -> SERVERLAN -> blokeret
```

## Zone på interface

```text
set security zones security-zone USERLAN interfaces ge-0/0/1.0
```

Tillad ping til routerens interface:

```text
set security zones security-zone USERLAN interfaces ge-0/0/1.0 host-inbound-traffic system-services ping
```

Tillad SSH til routerens interface:

```text
set security zones security-zone USERLAN interfaces ge-0/0/1.0 host-inbound-traffic system-services ssh
```

## Simpel policy

```text
set security policies from-zone USERLAN to-zone SERVERLAN policy allow-http match source-address any
set security policies from-zone USERLAN to-zone SERVERLAN policy allow-http match destination-address any
set security policies from-zone USERLAN to-zone SERVERLAN policy allow-http match application junos-http
set security policies from-zone USERLAN to-zone SERVERLAN policy allow-http then permit
```

Tillad alt i en øvelsesopstilling:

```text
set security policies from-zone myTrust to-zone myTrust policy default-permit match source-address any
set security policies from-zone myTrust to-zone myTrust policy default-permit match destination-address any
set security policies from-zone myTrust to-zone myTrust policy default-permit match application any
set security policies from-zone myTrust to-zone myTrust policy default-permit then permit
```

Tjek:

```text
show security zones
show security policies
show configuration security
```

Gem:

```text
commit check
commit
```

God eksamensforklaring:

Security zones bruges til at segmentere netværket logisk. Selvom routing-tabellen kender ruten, betyder det ikke automatisk at trafikken er tilladt. På en SRX skal både routing og security policy passe.

