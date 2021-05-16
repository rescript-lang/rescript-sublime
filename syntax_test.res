// SYNTAX TEST "ReScript.sublime-syntax"

// hi
// ^ comment.line

//
// <- comment.line punctuation.definition.comment

/* hello
// <- comment.block punctuation.definition.comment.begin
    /* nested
//  ^^ comment.block comment.block punctuation.definition.comment.begin
       bla
    */
//  ^^ comment.block comment.block punctuation.definition.comment.end
  world */
//^ comment.block
//       ^ comment.block punctuation.definition.comment.end


// === binding

let myBinding = 5
// <- keyword
//            ^ keyword.operator


// === string

   "aa";
// ^ string.quoted.double punctuation.definition.string.begin
//  ^^ string.quoted.double
//    ^ string.quoted.double punctuation.definition.string.end
//     ^ punctuation.terminator

   'a'
// ^^^ string.quoted.single

   'ab'
// ^^^^ source.res

let \"a b" = c
let str = `hi`
//        ^ string.quoted.other punctuation.definition.string.begin
//         ^^ string.quoted.other
//           ^ string.quoted.other punctuation.definition.string.end
let interp = j`hello $bla bye`
//           ^ string.quoted.other variable.annotation
//                   ^ punctuation.section.interpolation
//                    ^^^ source.res
//                       ^^^^^ string.quoted.other
let interp = j`hello $1 bye`
//                    ^^^^^^ string.quoted.other
let interp = j`hi ${world.bla->b(a)} bye`
//            ^ string.quoted.other punctuation.definition.string.begin
//             ^^^ string.quoted.other
//                ^^ punctuation.section.interpolation.begin
//                       ^ punctuation.accessor
//                           ^^ keyword.operator
//                              ^ punctuation.section.parens.begin
//                                 ^ punctuation.section.interpolation.end
//                                   ^^^ string.quoted.other
//                                      ^ string.quoted.other punctuation.definition.string.end


// === numbers

let a = -.0.1
//      ^^ keyword.operator
//        ^^^ constant.numeric
let a = 0b1
//    ^ keyword.operator
//      ^^^ constant.numeric
let a = 0o73
//      ^^^^ constant.numeric
let a = 0xff
//      ^^^^ constant.numeric
let a = 0Xff
//      ^^^^ constant.numeric
let a = +1_000_000.12
//      ^ keyword.operator
//       ^^^^^^^^^^^^ constant.numeric
let a = 1E3
//      ^^^constant.numeric

// to reconsider
let a = -.1
//      ^^ keyword.operator
//        ^ constant.numeric
let a = 1.
//      ^ constant.numeric
//       ^ punctuation.accessor
let a = .2
//      ^ punctuation.accessor
//       ^ constant.numeric

// negative examples. Shouldn't assign numeric scope
let a = 0bf
//      ^^^source.res
let a = 0o58
//      ^^^^source.res
let a = 0xfz
//      ^^^^source.res


// === other primitives

let bar = true && false
//        ^^^^ constant.language
//                ^^^^^ constant.language


// === collections

let [1, 2.2] = foo()
//   ^ constant.numeric
//      ^^^ constant.numeric
let [c, [a, [1], list{a, ...rest},  c], 2.2] = [c, 1, "d", 'a', 1+2]
//               ^ keyword
//                       ^ keyword.operator

let asd = ["bar"]
//        ^ punctuation.section.brackets.begin
//              ^ punctuation.section.brackets.end
let asd = list{"bar"}
//        ^^^^ keyword
let asd = foo["bar"]
//           ^ punctuation.section.brackets.begin
//                 ^ punctuation.section.brackets.end

// === record

type bla<'a> = {
// <- storage.type
//       ^^ support.type
//             ^ punctuation.section.braces.begin
  a: int,
// ^ punctuation.separator
//      ^ punctuation.separator
  ok: 'a,
//    ^^ support.type
}
// <- punctuation.section.braces.end

let recordAccess = fooRecord.myName
//                          ^ punctuation.accessor
let recordAccessWithScope = fooRecord.ReasonReact.myName
//                                    ^entity.name.namespace


// === variant

exception Hello
// <- keyword
//        ^^^^^ variable.function variable.other
type profession = Teacher | Director
//                ^^^^^^^ variable.function variable.other
let person1 = Teacher
//            ^^^^^^^ variable.function variable.other

try (getItem([1, 2, 3])) {
| Not_found => 0 /* Default value if getItem throws */
// <- punctuation.separator
//               ^ comment.block
}

switch person {
| [Teacher] => "A teacher"
// <- punctuation.separator
//^ punctuation.section.brackets.begin
// ^^^^^^^ variable.function variable.other
//          ^^ storage.type.function keyword.declaration.function
| Director => "A director"
//^^^^^^^^ variable.function variable.other
| rest => "..."
}

let polyVar = #hey
//            ^ punctuation.definition.keyword
//             ^^^ variable.function variable.other
let polyVar = #"hey"
//            ^ punctuation.definition.keyword
//             ^ string.quoted.double punctuation.definition.string.begin
let polyVar = #123
//            ^ punctuation.definition.keyword
//             ^^^ constant.numeric
let #...restPattern = myPolyVariant
//  ^^^^ punctuation.definition.keyword
//      ^^^^^^^^^^^ variable.function variable.other

// === function

let getItem = (theList) =>
//                      ^^ storage.type.function keyword.declaration.function
  if callSomeFunctionThatThrows() {
    /* return the found item here */
//  ^ comment.block
  } else {
    raise(Not_found)
  }

let getCenterCoordinates = (aBla, ~b=1, ~c=?, ()) => {
//                       ^ keyword.operator
//                                ^ punctuation.definition.keyword
//                                         ^ punctuation.separator
  let x = doSomeOperationsHere("a")
  let yy = doSomeMoreOperationsHere()
  (x, y)
}


// === operators

 a->b(c)->Some
//^^ keyword.operator
//      ^^ keyword.operator

a > b && a < b && a >= b
//    ^^ keyword.operator
//                  ^^ keyword.operator
a <= b || a == (b === c)
//^^ keyword.operator
//     ^^ keyword.operator
//          ^^ keyword.operator
//                ^^^ keyword.operator


// negative examples
let f: (~r: option<int>=?) = 1
//                    ^ source.res
//                     ^ keyword.operator
//                      ^ punctuation.separator
let f: (~r: option<int>= ?) = 1
//                    ^ source.res
//                     ^ keyword.operator
//                       ^ punctuation.separator


// === jsx

let myComponent = <div className="foo">
  <>
    <img src="avatar.png" className="profile" />
    <h3>{[user.firstName, user.lastName].join(" ")}</h3>
  </>
  <Comp.Uter bar />
// ^ entity.name.namespace
//      ^ entity.name.namespace
  <Foo>
// ^ entity.name.namespace
    "hi"
  </Foo>
//  ^ entity.name.namespace
  <Foo.Bar> {"hi"} </Foo.Bar>
//     ^ entity.name.namespace
//                       ^ entity.name.namespace
  <Comp bar />
// ^ entity.name.namespace
</div>


// === module

let openSesame = 1
//  ^^^^^^^^^^ source.res

open Soup
// <- keyword
//   ^^^^ entity.name.namespace
include {let a = 1}
// <- keyword
//       ^ keyword
open Belt.Map
//   ^ entity.name.namespace
//        ^ entity.name.namespace
include Belt.Map.Make()
//               ^ entity.name.namespace

Foo.Some(Bar)
// <- entity.name.namespace
//     ^ source.res
//       ^^^ variable.function variable.other
//          ^ source.res
Foo.Some(Bar())
//       ^ source.res
//       ^^^ variable.function variable.other
Foo.make(Bar())
//       ^^^ variable.function variable.other
module Bla = Belt.Map.Make(Bar({type t let a:b = "cc"}))
//     ^ entity.name.namespace
//         ^ keyword.operator
//           ^ entity.name.namespace
//                    ^ entity.name.namespace
//                        ^ punctuation.section.parens.begin
//                         ^ entity.name.namespace
//                            ^ punctuation.section.parens.begin
//                              ^ storage.type
//                                                    ^ punctuation.section.parens.end
//                                                     ^ punctuation.section.parens.end
module SetOfIntPairs: Foo = MakeSet(IntPair)
//                    ^ entity.name.namespace
//                          ^ entity.name.namespace
//                                  ^ entity.name.namespace
module SetOfIntPairs = MakeSet((IntPair), Bar);
//                              ^ entity.name.namespace
//                                        ^ entity.name.namespace
module SetOfIntPairs = MakeSet(IntPair({type t = Bar}))
//                             ^ entity.name.namespace
//                                               ^^^ variable.function variable.other
module Foo = (Bar: Baz) => (Bar: Baz) => {let a = Bar};
//            ^ entity.name.namespace
//                 ^ entity.name.namespace
//                          ^ entity.name.namespace
//                               ^ entity.name.namespace
//                                                ^^^ variable.function variable.other
module Foo = (Bar: Baz) => (Bar: Baz) => List;
//                                       ^ entity.name.namespace

module Nested = (Foo: {}) => {
  module NestMore = Bla
//       ^ entity.name.namespace
//                  ^ entity.name.namespace
}
module type Bla = {
//          ^ entity.name.namespace
  include (module type of BaseComponent)
//                        ^ entity.name.namespace
}

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
//  ^ entity.name.namespace
//       ^ entity.name.namespace
    {
      type a = Bar
//             ^^^ variable.function variable.other
      let a = ["1"]
    }
  ) => {
    module NestMore =
      Bla
//    ^ entity.name.namespace
    module NestMore = (Foo: {}) => Bla
//                     ^ entity.name.namespace
//                                 ^ entity.name.namespace
  }
  module Nested2 = (
    Foo: Bar,
//  ^ entity.name.namespace
//       ^ entity.name.namespace
    Bar: Baz,
//  ^ entity.name.namespace
//       ^ entity.name.namespace
  ) => List
//     ^ entity.name.namespace
  module Nested = (Foo: Bar, {type a = Bar let a = 1 } ) => {
//                 ^ entity.name.namespace
//                      ^ entity.name.namespace
//                                     ^^^ variable.function variable.other
    module NestMore = Bla
    module NestMore: Foo = Bla
    module NestMore: {type t = Bar} = Bla
//                   ^ punctuation.section.braces.begin
//                             ^^^ variable.function variable.other
//                                ^ punctuation.section.braces.end
//                                    ^ entity.name.namespace
    module NestMore: {type t = Bar} = {
//                             ^^^ variable.function variable.other
      type t = Variant
//             ^^^^^^^ variable.function variable.other
      let a = ["hello"]
    }
    module NestMore = (Foo: {type t = Variant}) => Bla
//                                    ^^^^^^^ variable.function variable.other
    module NestMore: Bla = (Foo: {}) => Bla
    module NestMore: {type t = Bar let a: b = "cc" module Foo = {}} = (Foo: {}) => Bla
//                             ^^^ variable.function variable.other
//                                                        ^ entity.name.namespace
    module type NestMore = {}
    module NestMore = () => Bla.Qux
//                              ^ entity.name.namespace
  }
}

let p: School.School2.profession = School.getProfession(School.Foo)
//     ^ entity.name.namespace
//            ^ entity.name.namespace
//                                                      ^ entity.name.namespace
//                                                             ^^^ variable.function variable.other

let getAudience = (~excited) => excited ? "world!" : "world"


// === attribute

   @foo(bar) let a = 1
// ^ meta.annotation punctuation.definition.annotation
//  ^^^ meta.annotation variable.annotation
@foo (bar) let a = 1
@foo(@bar(baz)) let a = 1
//   ^ meta.annotation punctuation.definition.annotation
//    ^^^ meta.annotation variable.annotation
@foo let a = 1
   @@foo let a = 1
// ^^ meta.annotation punctuation.definition.annotation
@@foo(bar) let a = 1
   %foo(bar)-2
// ^ meta.annotation punctuation.definition.annotation
//  ^^^ meta.annotation variable.annotation


// === extension point

%foo (bar)-2
%foo-1
   %%foo let a = 1
// ^^ meta.annotation punctuation.definition.annotation
//   ^^^ meta.annotation variable.annotation
%%foo(bar) let a = 1
%%foo (bar) let a = 1


// === external

  @module external foo: {..} => {..} = "bla"
// ^^^^^^ meta.annotation variable.annotation
//                       ^^ keyword.operator
//                           ^^ storage.type.function keyword.declaration.function
//                               ^^ keyword.operator


// === deprecated

myList |> map
//     ^^ invalid.deprecated
let a = %bs.raw("1")
//       ^^^ meta.annotation invalid.deprecated
  @bs.send.pipe external a: b => c = ""
// ^^^^^^^^^^^^ meta.annotation invalid.deprecated
  @bs.module external a: b = ""
// ^^^ meta.annotation invalid.deprecated
  @splice external a: b = ""
// ^^^^^^ meta.annotation invalid.illegal
  @bs.variadic external a: b = ""
// ^^^ meta.annotation invalid.deprecated
  @variadic external a: b = "" // works
// ^^^^^^^^ meta.annotation variable.annotation
