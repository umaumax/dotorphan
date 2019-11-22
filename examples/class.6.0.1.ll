; ModuleID = 'class.cpp'
source_filename = "class.cpp"
target datalayout = "e-m:o-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.13.0"

%class.B = type { i8 }
%class.A = type { i8 }

; Function Attrs: noinline nounwind optnone ssp uwtable
define void @_ZN1BC2Ev(%class.B*) unnamed_addr #0 align 2 {
  %2 = alloca %class.B*, align 8
  store %class.B* %0, %class.B** %2, align 8
  %3 = load %class.B*, %class.B** %2, align 8
  ret void
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define void @_ZN1BC1Ev(%class.B*) unnamed_addr #0 align 2 {
  %2 = alloca %class.B*, align 8
  store %class.B* %0, %class.B** %2, align 8
  %3 = load %class.B*, %class.B** %2, align 8
  call void @_ZN1BC2Ev(%class.B* %3)
  ret void
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define void @_ZN1BD2Ev(%class.B*) unnamed_addr #0 align 2 {
  %2 = alloca %class.B*, align 8
  store %class.B* %0, %class.B** %2, align 8
  %3 = load %class.B*, %class.B** %2, align 8
  ret void
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define void @_ZN1BD1Ev(%class.B*) unnamed_addr #0 align 2 {
  %2 = alloca %class.B*, align 8
  store %class.B* %0, %class.B** %2, align 8
  %3 = load %class.B*, %class.B** %2, align 8
  call void @_ZN1BD2Ev(%class.B* %3) #3
  ret void
}

; Function Attrs: noinline norecurse optnone ssp uwtable
define i32 @main(i32, i8**) #1 personality i8* bitcast (i32 (...)* @__gxx_personality_v0 to i8*) {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i8**, align 8
  %6 = alloca %class.A, align 1
  %7 = alloca %class.B, align 1
  %8 = alloca i8*
  %9 = alloca i32
  store i32 0, i32* %3, align 4
  store i32 %0, i32* %4, align 4
  store i8** %1, i8*** %5, align 8
  call void @_ZN1AC1Ev(%class.A* %6)
  invoke void @_ZN1BC1Ev(%class.B* %7)
          to label %10 unwind label %12

; <label>:10:                                     ; preds = %2
  store i32 0, i32* %3, align 4
  call void @_ZN1BD1Ev(%class.B* %7) #3
  call void @_ZN1AD1Ev(%class.A* %6) #3
  %11 = load i32, i32* %3, align 4
  ret i32 %11

; <label>:12:                                     ; preds = %2
  %13 = landingpad { i8*, i32 }
          cleanup
  %14 = extractvalue { i8*, i32 } %13, 0
  store i8* %14, i8** %8, align 8
  %15 = extractvalue { i8*, i32 } %13, 1
  store i32 %15, i32* %9, align 4
  call void @_ZN1AD1Ev(%class.A* %6) #3
  br label %16

; <label>:16:                                     ; preds = %12
  %17 = load i8*, i8** %8, align 8
  %18 = load i32, i32* %9, align 4
  %19 = insertvalue { i8*, i32 } undef, i8* %17, 0
  %20 = insertvalue { i8*, i32 } %19, i32 %18, 1
  resume { i8*, i32 } %20
}

; Function Attrs: noinline optnone ssp uwtable
define linkonce_odr void @_ZN1AC1Ev(%class.A*) unnamed_addr #2 align 2 {
  %2 = alloca %class.A*, align 8
  store %class.A* %0, %class.A** %2, align 8
  %3 = load %class.A*, %class.A** %2, align 8
  call void @_ZN1AC2Ev(%class.A* %3)
  ret void
}

declare i32 @__gxx_personality_v0(...)

; Function Attrs: noinline nounwind optnone ssp uwtable
define linkonce_odr void @_ZN1AD1Ev(%class.A*) unnamed_addr #0 align 2 {
  %2 = alloca %class.A*, align 8
  store %class.A* %0, %class.A** %2, align 8
  %3 = load %class.A*, %class.A** %2, align 8
  call void @_ZN1AD2Ev(%class.A* %3) #3
  ret void
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define linkonce_odr void @_ZN1AC2Ev(%class.A*) unnamed_addr #0 align 2 {
  %2 = alloca %class.A*, align 8
  store %class.A* %0, %class.A** %2, align 8
  %3 = load %class.A*, %class.A** %2, align 8
  ret void
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define linkonce_odr void @_ZN1AD2Ev(%class.A*) unnamed_addr #0 align 2 {
  %2 = alloca %class.A*, align 8
  store %class.A* %0, %class.A** %2, align 8
  %3 = load %class.A*, %class.A** %2, align 8
  ret void
}

attributes #0 = { noinline nounwind optnone ssp uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noinline norecurse optnone ssp uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { noinline optnone ssp uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind }

!llvm.module.flags = !{!0, !1}
!llvm.ident = !{!2}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!2 = !{!"clang version 6.0.1 (tags/RELEASE_601/final)"}
