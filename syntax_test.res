// SYNTAX TEST "ReScript.sublime-syntax"

// hi
// ^ source.res comment.line

//
// <- source.res comment.line punctuation.definition.comment

/* hello
// <- source.res comment.block punctuation.definition.comment.begin
  world */
//^ source.res comment.block
//       ^ source.res comment.block punctuation.definition.comment.end

   "aa";
// ^ source.res string.quoted.double punctuation.definition.string.begin
//  ^^ source.res string.quoted.double
//    ^ source.res string.quoted.double punctuation.definition.string.end
//     ^ source.res punctuation.terminator

   'a'
// ^^^ source.res string.quoted.single

   'ab'
// ^^^^ source.res

exception Hello
// <- keyword
//        ^^^^^ variable.function variable.other

let a = -.0.1
//      ^^ source.res keyword.operator
//        ^^^ source.res constant.numeric
let a = 0b1
//    ^ source.res keyword.operator
//      ^^^ source.res constant.numeric
let a = 0o73
//      ^^^^ source.res constant.numeric
let a = 0xff
//      ^^^^ source.res constant.numeric
let a = 0Xff
//      ^^^^ source.res constant.numeric
let a = +1_000_000.12
//      ^ source.res keyword.operator
//       ^^^^^^^^^^^^ source.res constant.numeric
let a = 1E3
//      ^^^source.res constant.numeric
// bad
let a = 0bf
//      ^^^source.res
let a = 0o58
//      ^^^^source.res
let a = 0xfz
//      ^^^^source.res
let a = -.1
//      ^^ source.res keyword.operator
//        ^source.res
let a = 1.
//      ^source.res constant.numeric
//       ^source.res punctuation.accessor
let a = .2
//      ^source.res punctuation.accessor
//       ^source.res constant.numeric

let bar = true
// <- source.res keyword
//        ^source.res constant.language
let recordAccess = fooRecord.myName
//                          ^source.res punctuation.accessor
let recordAccessWithScope = fooRecord.ReasonReact.myName
//                                    ^source.res entity.name.namespace

let [1, 2.2] = foo()
//   ^ source.res constant.numeric
//      ^^^ source.res constant.numeric
let [c, [a, [1], list{a, ...rest},  c], 2.2] = [c, 1, "d", 'a', 1+2]
//               ^ source.res keyword
//                       ^ source.res keyword.operator

type bla<'a> = {
// <- source.res storage.type
//             ^ source.res punctuation.section.braces.begin
  a: int,
     // ^ source.res punctuation.separator
  ok: 'a,
}
// <- source.res punctuation.section.braces.end

let getItem = (theList) =>
  if callSomeFunctionThatThrows() {
    /* return the found item here */
//  ^ source.res comment.block
  } else {
    raise(Not_found)
  }

let result =
  try (getItem([1, 2, 3])) {
  | Not_found => 0 /* Default value if getItem throws */
//^ source.res punctuation.separator
              //   ^ source.res comment.block
  }

let getCenterCoordinates = (aBla, doHello, ~b=1, ~c, ()) => {
                                        // ^ source.res punctuation.definition.keyword
  let x = doSomeOperationsHere("a")
  let yy = doSomeMoreOperationsHere()
  (x, y)
}

 a->b(c)->Some
//^^ keyword.operator
//      ^^ keyword.operator

type profession = Teacher | Director
//                ^ source.res
/* test */

let person1 = Teacher
//            ^ source.res
let getProfession = (person) =>
  switch person {
  | [Teacher] => "A teacher"
  | Director => "A director"
  | rest => "..."
  }

open Soup
// <- source.res keyword
//   ^^^^ entity.name.namespace
include {let a = 1}
// <- keyword
//       ^ source.res keyword
open Belt.Map
//   ^ source.res entity.name.namespace
//        ^ source.res entity.name.namespace
include Belt.Map.Make()
//               ^ source.res entity.name.namespace

Foo.Some(Bar)
// <- source.res entity.name.namespace
//     ^ source.res
//          ^ source.res
Foo.Some(Bar())
//       ^ source.res
Foo.make(Bar())
module Bla = Belt.Map.Make(Bar({type t let a:b = "cc"}))
//     ^ source.res entity.name.namespace
//           ^ source.res entity.name.namespace
//                    ^ source.res entity.name.namespace
//                        ^ source.res punctuation.section.parens.begin
//                         ^ source.res entity.name.namespace
//                            ^ source.res punctuation.section.parens.begin
//                              ^ source.res storage.type
//                                                    ^ source.res punctuation.section.parens.end
//                                                     ^ source.res punctuation.section.parens.end
module SetOfIntPairs: Foo = MakeSet(IntPair)
//                    ^ source.res entity.name.namespace
//                          ^ source.res entity.name.namespace
//                                  ^ source.res entity.name.namespace
module SetOfIntPairs = MakeSet((IntPair), Bar);
//                              ^ source.res entity.name.namespace
//                                        ^ source.res entity.name.namespace
module SetOfIntPairs = MakeSet(IntPair({type t = Bar}))
//                             ^ source.res entity.name.namespace
//                                               ^^^ entity.name.namespace
module Foo = (Bar: Baz) => (Bar: Baz) => {let a = Bar};
//            ^ source.res entity.name.namespace
//                 ^ source.res entity.name.namespace
//                          ^ source.res entity.name.namespace
//                               ^ source.res entity.name.namespace
//                                                ^ source.res
module Foo = (Bar: Baz) => (Bar: Baz) => List;
//                                       ^ source.res entity.name.namespace

module Nested = (Foo: {}) => {
  module NestMore = Bla
//       ^ source.res entity.name.namespace
//                  ^ source.res entity.name.namespace
}
module type Bla = {
//          ^ source.res entity.name.namespace
  include (module type of BaseComponent)
//                        ^ source.res entity.name.namespace
}
/* test */
module School = {
  type profession = Teacher | Director
  /* test */

  let person1 = Teacher
  let getProfession = (person) =>
    switch (person) {
    | Teacher => "A teacher"
    | Director => "A director"
    }
  module Nested = (
    Foo: Bar,
//  ^ source.res entity.name.namespace
//       ^ source.res entity.name.namespace
    {
      type a = Bar
//             ^ source.res
      let a = ["1"]
    }
  ) => {
    module NestMore =
      Bla
//    ^ source.res entity.name.namespace
    module NestMore = (Foo: {}) => Bla
//                     ^ source.res entity.name.namespace
//                                 ^ source.res entity.name.namespace
  }
  module Nested2 = (
    Foo: Bar,
//  ^ source.res entity.name.namespace
//       ^ source.res entity.name.namespace
    Bar: Baz,
//  ^ source.res entity.name.namespace
//       ^ source.res entity.name.namespace
  ) => List
//     ^ source.res entity.name.namespace
  module Nested = (Foo: Bar, {type a = Bar let a = 1 } ) => {
//                 ^ source.res entity.name.namespace
//                      ^ source.res entity.name.namespace
//                                     ^ source.res
    module NestMore = Bla
    module NestMore: Foo = Bla
    module NestMore: {type t = Bar} = Bla
//                   ^ source.res punctuation.section.braces.begin
//                             ^ source.res
//                                ^ source.res punctuation.section.braces.end
//                                    ^ source.res entity.name.namespace
    module NestMore: {type t = Bar} = {
//                             ^ source.res
      type t = Variant
//             ^ source.res
      let a = ["hello"]
    }
    module NestMore = (Foo: {type t = Variant}) => Bla
    module NestMore: Bla = (Foo: {}) => Bla
    module NestMore: {type t = Bar let a: b = "cc" module Foo = {}} = (Foo: {}) => Bla
//                             ^ source.res
//                                                        ^ source.res entity.name.namespace
    module type NestMore = {}
    module NestMore = () => Bla.Qux
//                              ^ source.res entity.name.namespace
  }
}

let p: School.School2.profession = School.getProfession(School.Foo)
//     ^ source.res entity.name.namespace
//            ^ source.res entity.name.namespace
//                                                      ^ source.res entity.name.namespace
//                                                             ^ source.res

let getAudience = (~excited) => excited ? "world!" : "world"

let jsx = <div className="foo">
  <>
    hi
  </>
  <Comp.Uter bar />
// ^ source.res entity.name.namespace
//      ^ source.res entity.name.namespace
  <Foo>
// ^ source.res entity.name.namespace
    "hi"
  </Foo>
//  ^ source.res entity.name.namespace
  <Foo.Bar> {"hi"} </Foo.Bar>
//     ^ source.res entity.name.namespace
//                       ^ source.res entity.name.namespace
  <Comp bar />
// ^ source.res entity.name.namespace
</div>


let \"a b" = c
let str = `hi`
//        ^ source.res string.quoted.other punctuation.definition.string.begin
//         ^^ source.res string.quoted.other
//           ^ source.res string.quoted.other punctuation.definition.string.end
let interp = j`hello $bla bye`
//                   ^ punctuation.section.interpolation
//                    ^^^ source.res
//                       ^^^^^ string.quoted.other
let interp = j`hello $1 bye`
//                    ^^^^^^ string.quoted.other
let interp = j`hello ${world.bla->b(a)} bye`
//            ^ source.res string.quoted.other punctuation.definition.string.begin
//             ^ source.res string.quoted.other
//                   ^^ source.res punctuation.section.interpolation.begin
//                          ^ punctuation.accessor
//                              ^^ keyword.operator
//                                 ^ punctuation.section.parens.begin
//                                    ^ punctuation.section.interpolation.end
//                                      ^^^ string.quoted.other
//                                         ^ string.quoted.other punctuation.definition.string.end
let variant = #foo
//            ^ source.res punctuation.definition.keyword
let #...foo = bar
//  ^^^^ punctuation.definition.keyword

   @foo(bar) let a = 1
// ^ source.res meta.annotation punctuation.definition.annotation
//  ^^^ source.res meta.annotation variable.annotation
@foo (bar) let a = 1
@foo(@bar(baz)) let a = 1
//   ^ source.res meta.annotation punctuation.definition.annotation
//    ^^^ source.res meta.annotation variable.annotation
@foo let a = 1
   @@foo let a = 1
// ^^ source.res meta.annotation punctuation.definition.annotation
@@foo(bar) let a = 1
   %foo(bar)-2
// ^ source.res meta.annotation punctuation.definition.annotation
//  ^^^ source.res meta.annotation variable.annotation
%foo (bar)-2
%foo-1
   %%foo let a = 1
// ^^ source.res meta.annotation punctuation.definition.annotation
//   ^^^ source.res meta.annotation variable.annotation
%%foo(bar) let a = 1
%%foo (bar) let a = 1

@bs.module external foo: {..} => {..} = "bla"
//                        ^^ source.res keyword.operator
//                                ^^ source.res keyword.operator

let asd = ["bar"]
let asd = list{"bar"}
//        ^ source.res keyword
let asd = foo["bar"]
//        ^ source.res
foo["bar"] = baz
// <- source.res
