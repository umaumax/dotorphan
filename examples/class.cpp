class A {
 public:
  A() {}
  ~A() {}
};
class B {
 public:
  B();
  ~B();
};
B::B() {}
B::~B() {}

int main(int argc, char* argv[]) {
  A a;
  B b;
  return 0;
}
