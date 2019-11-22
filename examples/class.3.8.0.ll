; ModuleID = 'class.cpp'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%class.B = type { i8 }
%class.A = type { i8 }

$_ZN1AC2Ev = comdat any

$_ZN1AD2Ev = comdat any

$__clang_call_terminate = comdat any

@_ZN1BC1Ev = alias void (%class.B*), void (%class.B*)* @_ZN1BC2Ev
@_ZN1BD1Ev = alias void (%class.B*), void (%class.B*)* @_ZN1BD2Ev

; Function Attrs: nounwind uwtable
define void @_ZN1BC2Ev(%class.B* %this) unnamed_addr #0 align 2 {
  %1 = alloca %class.B*, align 8
  store %class.B* %this, %class.B** %1, align 8
  %2 = load %class.B*, %class.B** %1, align 8
  ret void
}

; Function Attrs: nounwind uwtable
define void @_ZN1BD2Ev(%class.B* %this) unnamed_addr #0 align 2 {
  %1 = alloca %class.B*, align 8
  store %class.B* %this, %class.B** %1, align 8
  %2 = load %class.B*, %class.B** %1, align 8
  ret void
}

; Function Attrs: norecurse uwtable
define i32 @main(i32 %argc, i8** %argv) #1 personality i8* bitcast (i32 (...)* @__gxx_personality_v0 to i8*) {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i8**, align 8
  %a = alloca %class.A, align 1
  %b = alloca %class.B, align 1
  %4 = alloca i8*
  %5 = alloca i32
  store i32 0, i32* %1, align 4
  store i32 %argc, i32* %2, align 4
  store i8** %argv, i8*** %3, align 8
  call void @_ZN1AC2Ev(%class.A* %a)
  invoke void @_ZN1BC1Ev(%class.B* %b)
          to label %6 unwind label %7

; <label>:6                                       ; preds = %0
  store i32 0, i32* %1, align 4
  invoke void @_ZN1BD1Ev(%class.B* %b)
          to label %11 unwind label %7

; <label>:7                                       ; preds = %6, %0
  %8 = landingpad { i8*, i32 }
          cleanup
  %9 = extractvalue { i8*, i32 } %8, 0
  store i8* %9, i8** %4, align 8
  %10 = extractvalue { i8*, i32 } %8, 1
  store i32 %10, i32* %5, align 4
  invoke void @_ZN1AD2Ev(%class.A* %a)
          to label %13 unwind label %19

; <label>:11                                      ; preds = %6
  call void @_ZN1AD2Ev(%class.A* %a)
  %12 = load i32, i32* %1, align 4
  ret i32 %12

; <label>:13                                      ; preds = %7
  br label %14

; <label>:14                                      ; preds = %13
  %15 = load i8*, i8** %4, align 8
  %16 = load i32, i32* %5, align 4
  %17 = insertvalue { i8*, i32 } undef, i8* %15, 0
  %18 = insertvalue { i8*, i32 } %17, i32 %16, 1
  resume { i8*, i32 } %18

; <label>:19                                      ; preds = %7
  %20 = landingpad { i8*, i32 }
          catch i8* null
  %21 = extractvalue { i8*, i32 } %20, 0
  call void @__clang_call_terminate(i8* %21) #3
  unreachable
}

; Function Attrs: nounwind uwtable
define linkonce_odr void @_ZN1AC2Ev(%class.A* %this) unnamed_addr #0 comdat align 2 {
  %1 = alloca %class.A*, align 8
  store %class.A* %this, %class.A** %1, align 8
  %2 = load %class.A*, %class.A** %1, align 8
  ret void
}

declare i32 @__gxx_personality_v0(...)

; Function Attrs: nounwind uwtable
define linkonce_odr void @_ZN1AD2Ev(%class.A* %this) unnamed_addr #0 comdat align 2 {
  %1 = alloca %class.A*, align 8
  store %class.A* %this, %class.A** %1, align 8
  %2 = load %class.A*, %class.A** %1, align 8
  ret void
}

; Function Attrs: noinline noreturn nounwind
define linkonce_odr hidden void @__clang_call_terminate(i8*) #2 comdat {
  %2 = call i8* @__cxa_begin_catch(i8* %0) #4
  call void @_ZSt9terminatev() #3
  unreachable
}

declare i8* @__cxa_begin_catch(i8*)

declare void @_ZSt9terminatev()

attributes #0 = { nounwind uwtable "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { norecurse uwtable "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { noinline noreturn nounwind }
attributes #3 = { noreturn nounwind }
attributes #4 = { nounwind }

!llvm.ident = !{!0}

!0 = !{!"clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final)"}
