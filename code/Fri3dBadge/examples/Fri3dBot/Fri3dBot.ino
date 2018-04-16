#include <Fri3dBadge.h>

#include <WiFi.h>

const char* ssid     = "WindyCloud";
const char* password = "100%wireless";

WiFiServer server(80);

void setup() {
	Serial.begin(115200);
	sta_neutraal();
  delay(3000);

  setup_wifi();
}

void setup_wifi() {
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  ontvang_en_verwerk();
  handle_wifi();
}

void handle_wifi() {
  WiFiClient client = server.available();
  if (client) {
    String currentLine = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        if (c == '\n') {
          if (currentLine.length() == 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();
            client.print("<a href=\"/n\">sta neutraal</a><br>\n");
            client.print("<a href=\"/w\">wandel 3 stappen vooruit</a><br>\n");
            client.println();
            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }
        if (currentLine.endsWith("GET /n")) {
          Serial.println("received cmd: n");
          sta_neutraal();
        }
        if (currentLine.endsWith("GET /w")) {
          wandel('v', 3);
          Serial.println("received cmd: w");
        }
      }
    }
    client.stop();
  }
}

// commando's die via monitor kunnen gegeven worden
#define NEUTRAAL  'n'
#define WANDEL    'w'
#define LEUN      'l'
#define DRAAI     'd'

// argumenten voor WANDEL, LEUN en DRAAI
#define VOORUIT   'v'
#define ACHTERUIT 'a'
#define LINKS     'l'
#define RECHTS    'r'

// lees commando's van de Serial Monitor en voer ze uit
void ontvang_en_verwerk() {
  if( ! Serial.available() )  {
    delay(100);
    return;
  }

  switch(Serial.read()) {
    case NEUTRAAL: sta_neutraal();                           break;
    case WANDEL:   wandel(Serial.read(), Serial.read()-'0'); break;
    case LEUN:     leun  (Serial.read());                    break;
    case DRAAI:    draai (Serial.read());                    break;
    default: Serial.println("onbekend commando");
  }
}

Fri3dBadge badge;

// mapping naar functionele namen voor de 4 servo's
enum {
	ENKEL_LINKS   = SERVO4,
	ENKEL_RECHTS  = SERVO2,
	BEEN_LINKS    = SERVO3,
	BEEN_RECHTS   = SERVO1
};

void sta_neutraal() {
  badge.servo(ENKEL_LINKS) .draai_naar(90);
  badge.servo(ENKEL_RECHTS).draai_naar(90);
  badge.servo(BEEN_LINKS)  .draai_naar(90);
  badge.servo(BEEN_RECHTS) .draai_naar(90);
}

void wandel(char richting, int stappen) {
  for(int s=0; s<stappen; s++) {
    if(richting == VOORUIT) {
      wandel_vooruit();
    } else if(richting == ACHTERUIT) {
      wandel_achteruit();
    }
  }
}

void leun(char richting) {
  if( richting == RECHTS ) {
   	badge.servo(ENKEL_LINKS) .draai(30);
		badge.servo(ENKEL_RECHTS).draai(30, 8);
  } else if( richting == LINKS ) {
   	badge.servo(ENKEL_RECHTS).draai(-25);
		badge.servo(ENKEL_LINKS) .draai(-25, 8);
  }
}

void draai(char richting) {
  if( richting == RECHTS ) {
    draai_rechts();
  } else if( richting == LINKS ) {
    draai_links();
  }
}

// functie om de 2 servos te gelijkertijd naar een eind hoek te laten bewegen
// TODO: voorlopig wordt aangenomen dat de servos onder dezelfde hoek starten
// TODO: te vervangen door te introduceren ServoGroep op lager niveau
void draai_naar(int servo1, int servo2, int eind_hoek, int interval) {
	int begin_hoek = badge.servo(servo1).hoek();
	int stap = begin_hoek < eind_hoek ? 1 : -1;
	while(badge.servo(servo1).hoek() != eind_hoek) {
		badge.servo(servo1).draai(stap);
		badge.servo(servo2).draai(stap);
    delay(interval);
  } 
}

// TODO: deelbewegigen hernoemen in NL
// TODO: bewegingen definiëren aan de hand van te introduceren Beweging klasse
//       op lager niveau

void wandel_vooruit(){
  leun(RECHTS);  
  
  rightfront2center();
  center2leftfront();

  leanbackright();

  leun(LINKS);

  leftfront2center();
  center2rightfront();
  
  leanbackleft();
}

void wandel_achteruit() {
  leun(RECHTS);  

  leftfront2center();
  center2rightfront();
  
  leanbackright();
 
  leun(LINKS);

  rightfront2center();
  center2leftfront();

  leanbackleft();
}

void draai_rechts(){
  badge.servo(BEEN_LINKS) .draai_naar(90);
  badge.servo(BEEN_RECHTS).draai_naar(90);
  
  leun(RECHTS);  

  badge.servo(BEEN_LINKS).draai(20, 15);

  leanbackright();

  leun(LINKS);

  badge.servo(BEEN_LINKS).draai_naar(90);
  delay(100);
   
  leanbackleft();
}

void draai_links(){
  badge.servo(BEEN_LINKS) .draai_naar(90);
  badge.servo(BEEN_RECHTS).draai_naar(90);
  
  leun(LINKS);  

  badge.servo(BEEN_RECHTS).draai(-20, 15);

  leanbackleft();

  leun(RECHTS);

  badge.servo(BEEN_RECHTS).draai_naar(90);
  delay(100);
  
  leanbackright();
}

void rightfront2center(){
  draai_naar(BEEN_LINKS, BEEN_RECHTS, 120, 5);
}

void center2leftfront(){
  draai_naar(BEEN_LINKS, BEEN_RECHTS, 60, 5);
}

void leanbackright(){
  badge.servo(ENKEL_LINKS) .draai_naar(90);
  badge.servo(ENKEL_RECHTS).draai_naar(90, 12);
}  

void leftfront2center(){
  draai_naar(BEEN_LINKS, BEEN_RECHTS, 90, 5);
}

void center2rightfront(){
  draai_naar(BEEN_LINKS, BEEN_RECHTS, 120, 5);
}

void leanbackleft(){
  badge.servo(ENKEL_RECHTS).draai_naar(90);
  badge.servo(ENKEL_LINKS) .draai_naar(90, 12);
}
