# examples


## ubuntu
* header onlyで完結する構造のクラスはUbuntuだとweak symbol扱い
  * [リンクと同名シンボル: weak シンボル編 \- bkブログ]( http://0xcc.net/blog/archives/000062.html )
* コンストラクタとデストラクタ実装が複数存在する意味は?
* 配置アドレスが0である意味は?

```
$ clang++ -std=c++11 class.cpp -c
$ nm -AC class.o
class.o:0000000000000000 W A::A()
class.o:0000000000000000 T B::B()
class.o:0000000000000000 T B::B()
class.o:0000000000000010 T main
WIP
```

## darwin
* コンストラクタとデストラクタ実装が複数存在する意味は?

```
$ clang++ -std=c++11 class.cpp -c
$ nm -AC class.o
class.o: 000000000000012c s GCC_except_table4
class.o:                  U __Unwind_Resume
class.o: 00000000000000d0 T A::()
class.o: 0000000000000110 T A::()
class.o: 00000000000000f0 T A::~()
class.o: 0000000000000120 T A::~()
class.o: 0000000000000010 T B::()
class.o: 0000000000000000 T B::()
class.o: 0000000000000040 T B::~()
class.o: 0000000000000030 T B::~()
class.o:                  U ___gxx_personality_v0
class.o: 0000000000000060 T _main
```

## FYI
### nm w/W

[nm\(1\): symbols from object files \- Linux man page]( https://linux.die.net/man/1/nm )

> The symbol is a weak symbol that has not been specifically tagged as a weak object symbol. When a weak defined symbol is linked with a normal defined symbol, the normal defined symbol is used with no error. When a weak undefined symbol is linked and the symbol is not defined, the value of the symbol is determined in a system-specific manner without error. On some systems, uppercase indicates that a default value has been specified.

