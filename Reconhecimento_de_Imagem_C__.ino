int solLED = 2;  // Porta digital para o LED do sol
int luaLED = 3; // Porta digital para o LED da lua
#define MSol_1 4
#define MSol_2 5
#define MLua_1 6
#define MLua_2 7

void setup() {
  Serial.begin(9600); // Taxa de atualização da comunicação com o algoritmo do reconhecimento de imagem
  pinMode(solLED, OUTPUT); // Define a porta digital como saída
  pinMode(luaLED, OUTPUT); // Define a porta digital como saída
  pinMode(MSol_1, OUTPUT);
  pinMode(MSol_2, OUTPUT);
  pinMode(MLua_1, OUTPUT);
  pinMode(MLua_2, OUTPUT);
  digitalWrite(MSol_1, LOW);
  digitalWrite(MSol_2, LOW);
  digitalWrite(MLua_1, LOW);
  digitalWrite(MLua_2, LOW);
}

void loop() {
  if (Serial.available() > 0) { // Garante que a comunicação serial está estabelecida
    int numFingers = Serial.read() - '0';  // Converte o caractere recebido para um número
    if (numFingers == 1) { // Condição caso o contador do reconhecimento de imagem envie "1"
      digitalWrite(MSol_1, HIGH);   // Aciona o Motor do Sol
      digitalWrite(MSol_2, LOW);    // Aciona o Motor do Sol
      digitalWrite(solLED, HIGH);   // Acende o Sol
      digitalWrite(luaLED, LOW);    // Garante a Lua apagada      
    }
    else if (numFingers == 2) { // Condição caso o contador do reconhecimento de imagem envie "2"
      digitalWrite(MSol_1, LOW);  // Para o Motor do Sol
      digitalWrite(MSol_2, LOW);  // Para o Motor do Sol
    }
    else if (numFingers == 3) { // Condição caso o contador do reconhecimento de imagem envie "4"
      digitalWrite(MLua_1, HIGH);   // Aciona o Motor da Lua
      digitalWrite(MLua_2, LOW);    // Aciona o Motor da Lua
      digitalWrite(luaLED, HIGH);   // Acende a Lua
      digitalWrite(solLED, LOW);    // Garante o Sol apagado
    }
    else if (numFingers == 4) { // Condição caso o contador do reconhecimento de imagem envie "4"
      digitalWrite(MLua_1, LOW);    // Para o Motor da Lua
      digitalWrite(MLua_2, LOW);    // Para o Motor da Lua
    }
    else if (numFingers == 0) { // Condição caso o contador do reconhecimento de imagem envie "4"
      digitalWrite(MLua_1, LOW);    // Para o Motor da Lua
      digitalWrite(MLua_2, LOW);    // Para o Motor da Lua
      digitalWrite(MSol_1, LOW);  // Para o Motor do Sol
      digitalWrite(MSol_2, LOW);  // Para o Motor do Sol
      digitalWrite(luaLED, LOW);    // Garante a Lua apagada 
      digitalWrite(solLED, LOW);   // Garante o Sol apagado
    }
    
  }
}
