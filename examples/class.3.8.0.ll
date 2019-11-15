; ModuleID = 'class.cpp'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%class.B = type { i8 }

@_ZN1BC1Ev = alias void (%class.B*), void (%class.B*)* @_ZN1BC2Ev

; Function Attrs: nounwind uwtable
define void @_ZN1BC2Ev(%class.B* %this) unnamed_addr #0 align 2 {
  %1 = alloca %class.B*, align 8
  store %class.B* %this, %class.B** %1, align 8
  %2 = load %class.B*, %class.B** %1, align 8
  ret void
}

attributes #0 = { nounwind uwtable "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.ident = !{!0}

!0 = !{!"clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final)"}
