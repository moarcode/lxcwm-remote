LXC Board

Projekt jest rozwinieciem aplikacji lxc-panel (https://github.com/moarcode/lxcwm).

Elementy projektu:
 - serwer proxy (proxy.py) + plik konfiguracyjny (proxy.cfg)
 - agent.py + plik konfiguracyjny (agent.cfg)

Instrukacj instalacji:
Sklonowac repozytorium: git clone https://github.com/moarcode/lxcwm-remote

Wymagane pakiety (Debian/Ubuntu):
 - pylxc
 - python2.7
 - moduly Pythona: pickle, sqlalchemy, socket

Instrukcja obslugi:
 - Plik proxy.py umiesic na serwerze na ktorym zainstalowana jest aplikacja lxc-panel
 - W pliku konfiguracyjnym proxy.cfg wpisać kolejno: adres i port, na którum proxy ma nasłuchiwać (separator: spacja)
 - Plik agenta (agent.py) wraz z plikiem konfiguracyjnym umiescic na serwerze zdalnym, na ktorym maja byc obslugiwane kontenery LXC
 - Plik konfiguracyjny agent.cfg umiescic na serwerze zdalnym. Wpisac kolejno adres,port serwera zdalnego oraz adres,port serwera proxy.
 - Uruchomic agenta i proxy poleceniem: python {agent.py, proxy.py}
 - Od tej pory usluga proxy oraz agent jest uruchomiona i nasluguje na podanych portach
