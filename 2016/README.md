# Fri3d Camp Badge 2016

Bij het ontwerp van de badge voor Fri3d Camp 2016 zijn we vertrokken van drie principes:

1. Een hoge _hack_-baarheid.
2. Leerzaam voor beginners.
3. Interactief.

Daarom brengt de badge het Arduino platform samen met infra-rode stralen om een eenvoudig Fri3d Camp draadloos (IR) netwerk te maken.

Het Arduino platform laat iedereen toe om de software van de badge aan te passen, of er iets totaal anders mee te doen. Naast de badge-functie voor Fri3d Camp, brengen we alle andere mogelijke functionaliteit van de microcontroller naar buiten, zodat de badge, na het kamp, letterlijk kan dienen als jouw eigen Arduino ontwikkel-bord.

Aan de hand van de IR componenten en bijhorende software kunnen de elementaire aspecten van draadloze communicatie uitgelegd worden.

### Meta-Leerzaam

Dit ontwerp was mijn eerste SMD-gebaseerde project en het is op zich al een leerzame ervaring. Daarom bevat deze repository tevens een [design dagboek](design/dagboek.md) waarin ik alle stappen van het proces beschrijf.

## Hardware Design

Twee bestaande projecten kunnen beschouwd worden als de spreekwoordelijke ouders van de badge: 

* [Arduino Pro Micro - 3.3V/8MHz van Sparkfun](https://www.sparkfun.com/products/12587)
* [TV B Gone van Mitch Altman](https://cornfieldelectronics.com/tvbgone/tvbg.home.php)

Voeg nog een IR receiver en een RGB LED toe en je hebt alle basis componenten voor een leerzame, interactieve en zeer _hack_-bare Fri3d Camp badge!

## Software

Om zelf aan de slag te gaan met de [software](src/README.md) zo eenvoudig mogelijk te maken, was één van dé belangrijkste aspecten een makkelijke integratie met het Arduino software platform. De mogelijkheid om de badge te programmeren via de Arduino IDE door middel van louter een micro-USB kabel was daarom een noodzaak.

Om het Arduino platform nog verder zo veel mogelijk te gebruiken, hebben we ook gekozen om zo dicht mogelijk bij een bestaand Arduino bord te blijven en zo is de badge in essentie een [Arduino Mirco](https://www.arduino.cc/en/Main/ArduinoBoardMicro) geworden.

Je kan dus onmiddellijk aan de slag, zoals met elke andere Arduino. Daarnaast bevat deze [repository](src/README.md) enkele applicaties specifiek geschreven voor de Fri3d Camp badge, en dit naast een bibliotheek die het aanspreken van de extras makkelijk maakt. Zo vindt je hier:

* dé Fri3d Camp 2016 app
* een implementatie van de TV B Gone applicatie van Mitch Altman
* ...

Als je zelf een nieuwe app maakt die op de Fri3d Camp badge werkt en op een andere, leuke manier gebruik maakt van de IR communicatie en de RGB LED of van andere componenten die je er zelf aan toegevoegd hebt, bezorg ons dan deze code en we voegen ze toe aan deze repository (pull request).

## Credits

De badge werd ontworpen door Christophe VG, samen met de hele Fri3d Camp organisatie, en uitgewerkt met de hulp van Dragan Subotic, Yannick Verbelen, Maarten Weyn, Willy De a Court, Anthony Liekens, Dries Deroeck, Jef Van Den Broeck, Toon Van de Putte,...
