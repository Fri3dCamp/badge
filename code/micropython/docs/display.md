# Fri3dBadge Display Module

## Matrix
Er zijn twee LED matrices beschikbaar op de badge. Elke LED matrix heeft 5 rijen en 7 kolommen en je kan elke led afzonderlijk aan zetten.

### Hardware
Elk van de twee matrices is opgebouwd uit 35 blauwe LED's volgens een matrix structuur waarbij de kolommen de negatieve pool en de rijen de positieve pool voorstellen. Dit wil dus zeggen dat wanneer je aan 1 kolom een ground (GND, -) aansluit en aan 1 rij een vcc (3.3V, +) dat de led op het kruispunt van de rij en de kolom zal oplichten.
Natuurlijk is het vrij moeilijk om 35 led's aan te sturen met 1 microcontroller, aangezien we daarvoor niet voldoende pinnen vrij hebben op de microcontroller. Om dat op te lossen maken we gebruik van shift registers. Hierdoor hebben we maar 4 pinnen nodig om in totaal 70 led's aan te sturen.

Meer informatie over shift registers kan je vinden op [http://artimesdiy.nl/index.php?option=com_content&view=article&id=117:arduino-les-4-shift-register-hc595-shiftout&catid=46:lessen&Itemid=76](artimesdiy.nl)

### Software
Wanneer je binnen micropython de matrices wil gebruiken, dan kan je dit doen door middel van de ```Matrices``` klasse binnen de display module.

```python
from display import Matrices

matrices = Matrices()
```

Eenmaal je de matrices instantie beschikbaar hebt, kan je led's aan zetten door middel van de ```set(matrix, x, y)``` functie:

```python
# zet van de eerste matrix de led in de linker benedenhoek aan
matrices.set(0, 0, 0)
```

Je kan de display terug leeg maken door de ```clear()``` functie te gebruiken:

```python
matrices.clear()
```

Er draait een apparte thread op de 2e CPU die er voor zorgt dat de LED's uiteindelijk gezet worden 