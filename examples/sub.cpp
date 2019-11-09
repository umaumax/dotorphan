#include "sub.hpp"
#include "main.hpp"

void sub_func() { sub_func2(); }
void sub_func2() {}

void sub_orphan_func() { sub_orphan_func2(); }
void sub_orphan_func2() { sub_orphan_func_call_main(); }
void sub_orphan_func3() { sub_orphan_func_call_main(); }

void sub_orphan_func_call_main() { hello_main_world(); }
