#!/usr/bin/env bash
PATH_BACKUP="$PATH"

# NOTE: 4,6,7,8 latest is 9
if [[ $(uname) == "Darwin" ]]; then
  llvm_bin_path_ary=("/usr/local/opt/llvm@4/bin" "/usr/local/opt/llvm@6/bin" "/usr/local/opt/llvm@7/bin" "/usr/local/opt/llvm@8/bin" "")
fi
if [[ "$(uname -a)" =~ Ubuntu ]]; then
  llvm_bin_path_ary=("/usr/lib/llvm-3.8/bin" "/usr/lib/llvm-5.0/bin" "/usr/lib/llvm-6.0/bin")
fi
for llvm_bin_path in "${llvm_bin_path_ary[@]}"; do
  PATH="$llvm_bin_path:$PATH_BACKUP"
  version=$(clang++ --version | grep -o "version [0-9.]*" | grep -o "[0-9.]\+")
  echo "$version"
  clang++ -emit-llvm class.cpp -c -S -o "class.${version}.ll"
  # NOTE: below is same result
  # clang++ -g -emit-llvm class.cpp -c -o "class.${version}.o"
  # llvm-dis "class.${version}.o"
done
