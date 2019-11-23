# examples

## コールグラフでコンストラクタとデストラクタが適切に解決されない不具合
llvmにbug?報告のメールがあるが，IBMの記事がわかりやすい答え

llvm bug? mail: [\[LLVMbugs\] \[Bug 14557\] New: clang doesn't generate "complete object constructor" code when the class contains pure virtual method\.]( http://lists.llvm.org/pipermail/llvm-bugs/2012-December/026249.html )

あるクラスにvirtual baseがない場合にはcomplete object constructorはVTT(virtual table table)を必要とせず，
base object constructorと一致するため，コンパイラによっては，emitしてaliasを作成しても良いとのこと

IBM blog: [Two identical constructors emitted? That’s not a bug\! \(C/C\+\+ compilers for IBM Z Blog\)]( https://www.ibm.com/developerworks/community/blogs/5894415f-be62-4bc0-81c5-3956e82276f3/entry/Two_identical_constructors_emitted_That_s_not_a_bug?lang=en )

> # Complete object constructor and base object constructor
> Now let’s get back to the constructors. We know that VTT would be generated for objects which have virtual bases and the constructor would use this to pass a construction virtual table when the constructor of its base is invoked. But note that the actions related with VTT are the business of grandchild, so no VTT action is taken during the construction of the base object, such as child::child(). That is to say,  there is a bit of difference between object constructors and base object constructors. That’s why we need two kinds of constructors.
> From the name you can tell the difference. The complete object constructor (C1) processes the whole construction work, including fetching VTT and invoking all constructions of bases. On the other hand, the base object constructor (C2) is only called when the object is constructed as a base. It only cares about the object itself.
> In this case, the complete object constructor (C1) of struct grandchild is called, it would invoke father::father() to construct the virtual base of grandchild. And also, it would invoke the base object constructor (C2) of struct child, which would not construct virtual base father. So both the complete object constructor and the base object constructor of struct child are generated, and they are used for child c and child-in-grandchild g respectively. Since grandchild is not derived in the program, the base object constructor is never invoked so only complete object constructor is generated.

この記述の通り，macのLLVM-IRをみると，`_ZN1BC1Ev`(complete object constructor)の中で，`_ZN1BC2Ev`(base object constructor)を呼び出していることが確認できる

> # Cases for classes without virtual base
> For classes that have no virtual bases, such as struct father in this case, the complete object constructor doesn’t need to do VTT so it would be completely the same as the base object constructor. In such situations, it depends on the implementation of compilers whether to emit both constructors. Some compilers might generate two constructors with just the same implementation, some might generate two functions and make them alias, while others would just emit one base object constructor.
> So, don’t be too surprised if you find two symbols for one constructor in your binary. They do exist for some reason.

つまり，コールグラフの作成用途としては，aliasを強制的に変換し，`opt`コマンドで名前を拾えるように変換した後に，demangleすることで，共通のシンボル名に変換した後に，描画するというステップは正しい

```
# for pipe
perl -pe 's/^(@[_0-9a-zA-Z]+) = alias ([_0-9a-zA-Z]+) \(.+?\), [_0-9a-zA-Z]+ (\(.+?\))\* @[_0-9a-zA-Z]+$/declare $2 $1$3/'
# for overwrite mode
perl -i -pe 's/^(@[_0-9a-zA-Z]+) = alias ([_0-9a-zA-Z]+) \(.+?\), [_0-9a-zA-Z]+ (\(.+?\))\* @[_0-9a-zA-Z]+$/declare $2 $1$3/' "$FILENAME"
```

input
```
@_ZN1BC1Ev = alias void (%class.B*), void (%class.B*)* @_ZN1BC2Ev
```

output
```
declare void @_ZN1BC1Ev(%class.B*)
```

## ubuntu
* header onlyで完結する構造のクラスはUbuntuだとweak symbol扱い
  * [リンクと同名シンボル: weak シンボル編 \- bkブログ]( http://0xcc.net/blog/archives/000062.html )
* 配置アドレスが0である意味は?(WIP)

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
$ nm -Am class.o
class.o: 000000000000012c (__TEXT,__gcc_except_tab) non-external GCC_except_table4
class.o:                  (undefined) external __Unwind_Resume
class.o: 00000000000000d0 (__TEXT,__text) weak external automatically hidden __ZN1AC1Ev # complete object constructor
class.o: 0000000000000110 (__TEXT,__text) weak external automatically hidden __ZN1AC2Ev # base object constructor
class.o: 00000000000000f0 (__TEXT,__text) weak external automatically hidden __ZN1AD1Ev # complete object destructor
class.o: 0000000000000120 (__TEXT,__text) weak external automatically hidden __ZN1AD2Ev # base object destructor
class.o: 0000000000000010 (__TEXT,__text) external __ZN1BC1Ev
class.o: 0000000000000000 (__TEXT,__text) external __ZN1BC2Ev
class.o: 0000000000000040 (__TEXT,__text) external __ZN1BD1Ev
class.o: 0000000000000030 (__TEXT,__text) external __ZN1BD2Ev
class.o:                  (undefined) external ___gxx_personality_v0
class.o: 0000000000000060 (__TEXT,__text) external _main
```

なぜ，demangleしたときに同一シンボルになる?
* C1 or D1: complete object constructor or destructor
* C2 or D2: base object constructor or destructor

```
$ echo "__ZN1AC1Ev __ZN1AC2Ev __ZN1AC3Ev __ZN1AC5Ev" | c++filt
A::() A::() A::() A::()
```
`C5`は? itanium-cxx-abiに記載がない
* [clang: lib/AST/ItaniumMangle\.cpp Source File]( https://clang.llvm.org/doxygen/ItaniumMangle_8cpp_source.html#l04464 )
  * > In addition, C5 is a comdat name with C1 and C2 in it.
  * > In addition, D5 is a comdat name with D1, D2 and, if virtual, D0 in it.
* [clang: lib/CodeGen/ItaniumCXXABI\.cpp Source File]( https://clang.llvm.org/doxygen/CodeGen_2ItaniumCXXABI_8cpp_source.html#l03911 )
  * > Only ELF and wasm support COMDATs with arbitrary names (C5/D5).

## FYI
### nm w/W

[nm\(1\): symbols from object files \- Linux man page]( https://linux.die.net/man/1/nm )

> The symbol is a weak symbol that has not been specifically tagged as a weak object symbol. When a weak defined symbol is linked with a normal defined symbol, the normal defined symbol is used with no error. When a weak undefined symbol is linked and the symbol is not defined, the value of the symbol is determined in a system-specific manner without error. On some systems, uppercase indicates that a default value has been specified.

### mangling
* [C\+\+名前マングリングの互換性 \- yohhoyの日記]( https://yohhoy.hatenadiary.jp/entry/20130607/p1 )
* [Itanium C\+\+ ABIのManglingルールについて \- 基礎構文編 \- Qiita]( https://qiita.com/WhiteGrouse/items/7a5e41075dc398652e67 )

#### `__ZN1AC1Ev`を読み解く

* [\# types are possible return type, then parameter types]( https://itanium-cxx-abi.github.io/cxx-abi/abi.html#mangle.name )
* [c\+\+ \- Dual emission of constructor symbols \- Stack Overflow]( https://stackoverflow.com/questions/6921295/dual-emission-of-constructor-symbols/6921467#6921467 )
* [Two identical constructors emitted? That’s not a bug\! \(C/C\+\+ compilers for IBM Z Blog\)]( https://www.ibm.com/developerworks/community/blogs/5894415f-be62-4bc0-81c5-3956e82276f3/entry/Two_identical_constructors_emitted_That_s_not_a_bug?lang=en )
* [c\+\+ \- Function coverage is lesser even with 100% code coverage when objects created in the stack \- Stack Overflow]( https://stackoverflow.com/questions/46447674/function-coverage-is-lesser-even-with-100-code-coverage-when-objects-created-in )

```
<mangled-name> ::= _Z <encoding>
                      <encoding> ::= <function name> <bare-function-type>
                                                     <bare-function-type> ::= <signature type>+ # types are possible return type, then parameter types
                                     <name> ::= <nested-name>
                                                <nested-name> ::= N [<CV-qualifiers>] [<ref-qualifier>] <prefix> <unqualified-name> E
                                                                                                                 <unqualified-name> ::= <ctor-dtor-name>
                                                                                                                                        <ctor-dtor-name> ::= C1	# complete object constructor
                                                                                                                                                         ::= C2	# base object constructor
                                                                                                                                                         ::= C3	# complete object allocating constructor
                                                                                                                                                         ::= D0	# deleting destructor
                                                                                                                                                         ::= D1	# complete object destructor
                                                                                                                                                         ::= D2	# base object destructor
                                                                                                        <prefix> ::= <unqualified-name>
                                                                                                                     <unqualified-name> ::= <source-name>
                                                                                                                                            <source-name> ::= <positive length number> <identifier>
                                                                                                                                                                                       <identifier> ::= <unqualified source code identifier>
```

上記と下記の具体例を参考にするとわかりやすい

```
echo "__ZN1AC1Ev" | c++filt
echo "__ZN1AD1Ev" | c++filt
echo "__ZN1AC1Ei" | c++filt
echo "__ZN1AD1Ei" | c++filt
echo "__ZN1AC1Eii" | c++filt
echo "__ZN1AC1Eiii" | c++filt
echo "__ZN3XYZC1Eiii" | c++filt
echo "__ZN4WXYZC1Eiii" | c++filt
echo "__ZN1AC2Ev" | c++filt
echo "__ZN1AC3Ev" | c++filt
echo "__ZN1AD0Ev" | c++filt
echo "__ZN1AD2Ev" | c++filt
```

```
A::()
A::~()
A::(int)
A::~(int)
A::(int, int)
A::(int, int, int)
XYZ::XYZ(int, int, int)
WXYZ::WXYZ(int, int, int)
A::()
A::()
A::~()
A::~()
```

* `C`: constructor
* `D`: destructor
