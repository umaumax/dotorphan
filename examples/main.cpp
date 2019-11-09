#include "sub.hpp"

void D() {}
void Y() { D(); }
void X() { Y(); }
void C() {
  D();
  X();
}
void B() { C(); }
void S() { D(); }
void P() { S(); }
void O() { P(); }
void N() { O(); }
void M() { N(); }
void G() { M(); }
void A() {
  B();
  G();
}

void hello_main_world() {}

int main() {
  A();
  hello_main_world();
  sub_func();
}
