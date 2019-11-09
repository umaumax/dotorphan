# examples

## cxxopts
```
git clone https://github.com/jarro2783/cxxopts
cd cxxopts
git apply ../cxxopts.patch
mkdir -p build
cd build
cmake -C ../../enable_clang_flto.cmake ..
make -j4

find . -name 'example*.o' | xargs llvm-link -o all.o
opt -analyze -dot-callgraph all.o
dotorphan callgraph.dot -o callgraph.filtered.dot
dot -Tsvg -ocallgraph-filtered.svg callgraph.filtered.dot
```


