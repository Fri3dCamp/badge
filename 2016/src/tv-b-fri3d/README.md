# TV B Fri3d

Aangezien de [TV B Gone](http://cornfieldelectronics.com/tvbgone/tvbg.home.php) één van de spreekwoordelijks ouders is van de Fri3d Badge, kan een implementatie van deze software niet ontbreken.

Het gebruiken van een Arduino om een "TV B Gone" te maken, is ook het onderwerp van een workshop van Mitch Altman zelf (zie: [http://cornfieldelectronics.com/cfe/projects/tvbg_arduino/tvbg_arduino_workshop.php](http://cornfieldelectronics.com/cfe/projects/tvbg_arduino/tvbg_arduino_workshop.php) voor meer info).

Deze versie is gebaseerd op eerder werk door Ken Shirriff. Mitch Altman heeft de code verder aangepast voor meerdere Arduino platformen, o.a. voor de "Adafruit's Flora", welke ook werkt op basis van de ATMega32u4.

## Aanpassingen

De code werkt niet "out-of-the-box" op de Fri3d Badge. Ze compileert prima,  maar we moeten nog wel enkele aanpassingen doen, omdat we andere pinnen (kunnen) gebruiken om de verschillende LEDs aan te sturen. Enerzijds is er de aansturing van de IR LEDs en anderszijds is er de status LED.

#### IR LED

In het geval van de Fri3d Badge is de pin om de IR LEDs aan te sturen (`IR_TX`) voorzien op pin `PF6`. In de code is ondersteuning voor Arduino/ATmega32u4 digitale pinnen "Digital Pin 3" of "Digital Pin 11" voorzien. Deze komen respectievelijk overeen met pin 18, `PD0`, en pin 12, `PB7 `(zie [https://www.arduino.cc/en/Hacking/PinMapping32u4](https://www.arduino.cc/en/Hacking/PinMapping32u4))

De code die hier relevant is:

```c
...
    // Fast PWM, setting top limit, divide by 8
    // Output to pin 3
#ifdef __AVR_ATmega32U4__
  #if (IRLED == 11)
    TCCR0A = _BV(COM0A1) | _BV(COM0A0) | _BV(WGM01) | _BV(WGM00);
  #elif (IRLED == 3)
    TCCR0A = _BV(COM0B1) | _BV(COM0B0) | _BV(WGM01) | _BV(WGM00);
  #else
    #error "IR LED must be on Leonardo digital pin 3 or 11."
  #endif
...  
```

Nader onderzoek leert dat dit tevens de twee pinnen zijn die op de ATmega32u4 kunnen gebruikt worden in een opstelling met `Timer0`. Zie [http://r6500.blogspot.be/2014/12/fast-pwm-on-arduino-leonardo.html](http://r6500.blogspot.be/2014/12/fast-pwm-on-arduino-leonardo.html), sectie over 'Single Slope PWM':
>Timer 0 has two compare channels A and B associated to two compare registers OCR0A and OCR0B. The two channels are linked to two hardware outputs OC0A and OC0B that are used as Arduino pins numbers 11 and 3.

Aangezien de Arduino implementatie voor de ATmega32 Beide pinnen zijn in ons design nog beschikbaar, zal het dus neerkomen op een aanpassing van het schema en de layout. Aangezien dit van de onderkant naar de bovenkant van de layout moet, zal het dus langs de onderkant moeten doorlopen. Gegeven de huidige layout, lijkt `PD0`, "Digital Pin 3", de beste keuze.

#### Status LED

The TV B Gone uses a status LED to indicate what it's doing. We don't have a simple LED on Fri3d Badge, but we have an RGB LED ;-)

De code die hier relevant is:

```c
// This function quickly pulses the visible LED (connected to PB0, pin 5)
// This will indicate to the user that a code is being transmitted
void quickflashLED( void ) {
  digitalWrite(LED, HIGH);
  delay_ten_us(3000);   // 30 millisec delay
  digitalWrite(LED, LOW);
}
```

Hier gaan we de RGB LED gebruiken, dus de code "moet" structureel aangepast worden, en drie verschillende pinnen aansturen. Oops, ook hier lopen we opnieuw _bijna_ tegen een slechte voorbereiding op: om de drie kleuren/pinnen te controleren hebben we opnieuw 3 PWM kanalen nodig. Gelukkig zijn de drie pinnen (`RGB_REG`, `RGB_GREEN` en `RGB_BLUE`) net aangesloten op drie pinnen met PWM support on "Digital Pins 5, 10 en 9". Een snelle test moet dit weldra bevestigen.

Wordt vervolgd...

## Fri3d Badge op Fri3d Camp 2016

Mitch Altman komt met zijn "Arduino for newbies" workshop naar Fri3d Camp, en wie weet werken jullie wel met jullie eigen badge tijdens deze workshop ;-) We sturen onze aanpassingen in ieder geval naar hem door ;-)
