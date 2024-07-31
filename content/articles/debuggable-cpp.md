Title: How to build highly-debuggable C++ binaries
Date: 2024-07-19 09:00
Category: Blog

<style>
code {
  white-space : pre-wrap !important;
}
</style>

This article is tightly scoped to cover one topic with specific, actionable advice: **How to configure your C++ toolchain to produce binaries that are highly-debuggable with respect to your current bug**. [Follow this link to skip the intro text and jump directly to the advice](#general-compilation-changes).

C++ has a notoriously complicated compilation model, and it has no standard build tooling or package manager. It can be an ordeal to even get a C++ project to compile, and it is even harder to configure one to produce debuggable binaries. I want to help regular C++ programmers improve their debugging experiences.

For an overview of the base C++ compilation model, I highly recommend [this article by Fabien Sanglard](https://fabiensanglard.net/dc/index.php). It doesn't cover everything, but what it does cover is done exceptionally well.



I also recommend reading through the manual for your project's build system, if there is one. You will need to understand how your high-level build system maps down to the low-level base compilation model. That abstraction is always leaky. Advanced features of your build system may also be useful when implementing this advice.

For managing dependencies, I recommend just using whatever your project recommends. That could be the system package manager for a particular Linux distribution, or a specific docker image, or Nix, or Conan. Maybe everything is vendored and built from source. If this is a work project, then there should be some blessed setup somewhere that has everything already installed for you [^work_project]. It may be painful at first but trying to go your own way will probably be even more painful. Some of this advice is most useful if you are able to build your dependencies from source.

[^work_project]: At least, I really hope so. Engineer time is expensive and this is low-hanging fruit.

With regards to debugging, programmers tend to have a strong preference for either interactive debugging (e.g. gdb) or printf-style debugging. I think that it is situational which one is better.

The advantage of interactive debugging is that it iteratively corrects your understanding of how the program operates as you go along, giving you a solid idea of what the program is actually doing at runtime. The advantage of printf-style debugging is that it is easy to do, even in constrained or unfamiliar environments. The first thing that programmers learn to do in a new language is print to the screen, and it tends to always work [^printf_fails].

[^printf_fails]: Unless you don't see output because the output is buffered and hasn't been flushed, or because stdout is closed or redirected.

These advantages suggest that interactive debugging is most useful in large unfamiliar legacy projects written in familiar languages (e.g. Chromium), whereas printf-style debugging is most useful in small familiar greenfield projects written in unfamiliar languages (e.g. intro programming class assignments).

Because the value proposition of C++ these days is mostly maintaining large legacy projects, interactive debugging should be preferred for most C++ programming work.

Unfortunately, the default experience of doing interactive debugging on C++ projects is quite bad, and most programmers lack the knowledge to make it better. Printf-style debugging is oddly attractive in C++ simply because you can generally expect it to work, even with optimizations turned on.

Nonetheless, I believe that it is usually possible to generate highly-debuggable C++ binaries that work well with an interactive debugger without sacrificing too much performance. A highly-debuggable binary should do all of the following:

- any function, variable, or macro that was in scope at a point inside the source code should be available inside the debugger
- the overall performance of the program should be bearable
- backtraces should be complete and accurate
- standard sanitizers and debug modes should be enabled

Furthermore, I will share tricks to further enhance debugging at specific sites, and to generally improve how the interactive debugger works with the binary:

- simplification of preprocessor directives and macros
- native-speed conditional breakpoints
- better stepping behavior
- pretty-printers for the stdlib and vocabulary types

I have organized this advice into four categories:

1. [General changes to the way that all code in your project is compiled](#general-compilation-changes)
2. [Semi-specific changes to how certain translation units are compiled](#semi-specific-compilation-and-source-changes)
3. [Specific, targeted source code changes](#specific-source-changes)
4. [Debugger configuration changes](#debugger-configuration-changes)

And I base my advice on two key principles:

1. Because C++ is a fully ahead-of-time compiled environment, where everything about the binary is decided at compilation time, and because most C++ projects contain performance-critical code, **you have to choose in advance which parts of your binary will be debuggable and which parts of your binary will be fast**. You should make this choice considering the particular bug at hand that you are trying to fix. Contrast this situation with interpreted languages, where everything is debuggable by default, or JIT-ed languages, where an optimized thunk of code can be de-optimized at runtime if you suddenly want to step through it.
2. Even the best generic changes to the way that a C++ project is compiled will not get you to parity with the debugging experience of a scripting language. **Targeted, specific source-level changes and custom debugger extensions are necessary to achieve the best possible debugging experience in C++**.

This guide is also specific to using g++ and clang++ on x86_64 GNU/Linux with gdb. Some advice may apply to other platforms.

# General Compilation Changes
## Enable the sanitizers
Compile 1) your source code and 2) all third-party libraries with a compatible subset of the sanitizers that is relevant to your problem.
### How
Add one of these to your `CFLAGS` and `CXXFLAGS`:

- `-fsanitize=address,undefined`
- `-fsanitize=thread`
- (with clang only) `-fsanitize=memory`

With clang on Linux, you might need to reduce the ASLR security level in order to get TSan working. See reference.

With MSan, you will need to configure your build system to produce a position-independent executable (PIE).
### Why
C++ is not a safe language. If something "wrong" happens, then further execution becomes unpredictable. You really want to be able to catch "wrong" things immediately and the sanitizers are the best tools to do that, even if they aren't always perfect. It's very common in C++ to 1) observe something "weird", 2) read the related source, 3) think "that behavior is impossible", 4) try to debug it for way too long, 5) eventually realize that something "wrong" happened earlier that caused undefined behavior and broke your reasonable mental model of the code.

The sanitizers are not all compatible with each other, so you will need to test multiple builds with different subsets enabled.

The sanitizers will not catch everything. There is currently no production-quality C++ toolchain that promises to alert on all undefined behavior. Correctness issues from undefined behavior are currently an unavoidable risk of C++ code, and I don't expect that to change within the next five years.

### Ref
- [GCC sanitizers](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html)
- [Clang sanitizers (docs index)](https://clang.llvm.org/docs/index.html)
- [Raymond Chen: undefined behavior can result in time travel](https://devblogs.microsoft.com/oldnewthing/20140627-00/?p=633)
- [Address Sanitizer internals](https://blog.gistre.epita.fr/posts/benjamin.peter-2022-10-28-address_sanitizer_internals/)
- [Clang + TSan workaround for Linux](https://stackoverflow.com/a/77856955)
## Enable "debug mode" or "debug hardening" within your stdlib
Enable "debug mode" for libstdc++ (the g++/linux stdlib implementation), or "debug hardening" for libc++ (the clang++/MacOS stdlib implementation). Note that libc++ used to provide a legacy "debug mode", but it has been removed and you want the new "debug hardening" mode.

### How
If using libstdc++:

Add this define to your `CXXFLAGS` if you are able to recompile your dependencies from source. It will change the ABI: `-D_GLIBCXX_DEBUG`

Otherwise, add this define to your `CXXFLAGS` to keep ABI compatibility: `-D_GLIBCXX_ASSERTIONS`

If using libc++:

Add this define to your `CXXFLAGS`: -`D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG`

Hardening modes do not affect the ABI.

### Why
This enables various range checks and other assertions for stdlib containers.

Note that because the C++ stdlib relies extensively on class templates defined in header files, and template classes are instantiated separately in each translation unit, adding the flags when compiling your application is mostly sufficient to enable them. You don't need to recompile the stdlib.

The ABI compatibility story is complicated. libstdc++ provides separate options for whether or not you want to keep ABI compatibility, and gives you better coverage if you break ABI compatibility. libc++ has a single option and will silently enable/disable certain checks depending on the platform ABI.
### Ref
- [GCC manual](https://gcc.gnu.org/onlinedocs/libstdc++/manual/debug_mode.html)
- [GCC discussion of _GLIBCXX_DEBUG vs _GLIBCXX_ASSERTIONS](https://gcc.gnu.org/wiki/LibstdcxxDebugMode)
- [Historical docs on Clang's old debug mode](https://releases.llvm.org/12.0.0/projects/libcxx/docs/DesignDocs/DebugMode.html)
- [Clang's new hardening levels](https://libcxx.llvm.org/Hardening.html)
## Enable debugging information for preprocessor macros
Generate debug info for macros.
### How
Add the following to your `CFLAGS` and `CXXFLAGS`: `-ggdb3`
### Why
In certain macro-heavy codebases, where macros are used like functions and call each other, it can be very useful to be able to dynamically evaluate macros as part of expressions inside of gdb. In general, you shouldn't write new code this way, but any large C++ codebase probably has some parts that fit this description.

Note that you will still not be able to step-into macros.
### Ref
- [GDB manual](https://gcc.gnu.org/onlinedocs/gcc/Debugging-Options.html#:~:text=%2Dglevel-,%2Dggdblevel,-%2Dgvmslevel)
## Enable frame-pointers for all functions
Compile with frame-pointers.
### How
Add the following to your `CFLAGS` and `CXXFLAGS`: `-fno-omit-frame-pointer -mno-omit-leaf-frame-pointer`
### Why
For a long time, it was fashionable to omit the frame pointer to save an extra register and generate more efficient code. This made sense for release builds on 32-bit x86, where there weren't many registers. The theory was also that DWARF debug information would provide enough information to reconstruct the call stack. In practice, this never worked very well. For x86_64, there are many more registers and it is worth it to always include the frame-pointer, even for release builds. You definitely want it while debugging. It will make printing backtraces faster and more reliable. Especially since we plan to optimize some translation units, having a frame pointer will ensure that we still get great backtraces even in optimized code.

The leaf frame pointer flag may be necessary if you have an old clang, due to a now-fixed bug. It never hurts to add it.
### Ref
- [The return of the frame pointers](https://www.brendangregg.com/blog/2024-03-17/the-return-of-the-frame-pointers.html)
- [Fixed LLVM bug which required the leaf frame pointer flag](https://bugs.llvm.org/show_bug.cgi?id=9825)
## Enable asynchronous unwind tables
Enable instruction-level unwind tables for every function.
### How
Add the following to your `CFLAGS` and `CXXFLAGS`: `-fasynchronous-unwind-tables`

This will ensure that the `.eh_frame` binary section is produced.
### Why
This information is part of the size overhead of C++ exceptions, so projects will sometimes turn it off. However, it also allows for precise stack unwinding (for backtrace generation) inside the debugger.

We shouldn't mind the performance penalty during debugging. Enabling this flag will complement the frame pointers and give us the best possible backtraces.
### Ref
- [MaskRay overview of stack unwinding techniques](https://maskray.me/blog/2020-11-08-stack-unwinding)
- [Writing a custom unwinder in gdb](https://developers.redhat.com/articles/2023/06/19/debugging-gdb-create-custom-stack-winders#building_an_example_use_case)
- [GCC manual](https://gcc.gnu.org/onlinedocs/gcc/Code-Gen-Options.html)
## Set the build architecture to base x86_64
Set your binary to build for a very old x86_64 machine.
### How
Add the following to your `CFLAGS` and `CXXFLAGS`: `-march=x86-64`
### Why
This may be important if you want to do reversible debugging [^rev_fix]. Reversible debugging requires a detailed model of the hardware ISA. Historically, reverse debuggers have not supported all x86_64 instructions (e.g. AVX). `x86-64` is the baseline 64-bit x86 architecture without extensions, which is likely to be well-supported by all tools.

[^rev_fix]: I needed this for gdb's builtin reversible debugging. HN user `mark_undoio` says [here](https://news.ycombinator.com/item?id=41101564) that this is not usually necessary with [rr](https://rr-project.org/) or [Undo](https://undo.io/), which are more powerful, much faster, and have more complete ISA support. I would recommend them over gdb's builtin support.

### Ref
- [Gentoo guide to exactly the opposite](https://wiki.gentoo.org/wiki/GCC_optimization#-march)
- [Difference between mtune and march](https://stackoverflow.com/a/10559360)
- [x86_64 microarchitecture levels](https://en.wikipedia.org/wiki/X86-64#:~:text=Microarchitecture%20levels,-%5Bedit%5D)
## Ensure that static libraries are fully linked into your binary
Link with whole-archive so that the entire static archive is available.
### How
Add the following to your `LDFLAGS`: `--whole-archive`
### Why
It is reasonable to want to call any function that is available from your source code from your debugger. Unfortunately, many things in C++ conspire to make this tricky. One such thing is that the linker will only pull in object files from a static archive if you use a symbol from that object file. So if you have a static library as a dependency and don't use any functions from one of the objects within the archive, then you won't be able to use that object file from the debugger because it won't be present in your binary.

This is especially annoying if you statically link against your libc, because many libcs put every symbol into its own object file in order to decrease the final binary size, prevent inlining, and allow symbol shadowing. Then, inside the debugger, you find that you can't call e.g. strlen to check the size of a null-terminated string because you never called it in your program. Of course, glibc can't be statically linked, so this is more of a problem for embedded platforms.
### Ref
- [ld manpage](https://linux.die.net/man/1/ld#:~:text=reporting%20unresolved%20symbols.-,%2D%2Dwhole%2Darchive,-For%20each%20archive)
# Semi-Specific Compilation and Source Changes
## Partition your TUs into "debuggable" and "fast"
Partition your TUs into "debuggable" and "fast", and compile the "debuggable" TUs with `--ggdb3 -O0` and the  "fast" TU's with `--ggdb3 -O3` [^gdb_fix].

[^gdb_fix]: Thanks to HN user `dataflow` for catching my typos [here](https://news.ycombinator.com/item?id=41105618).

### How
You need to build different sets of TUs with different `CFLAGS` and `CXXFLAGS`.

This is unfortunately quite specific to your build system, and I am not aware of any that have this as a built-in feature. My recommendation is to hack up your build system so that you can specify a set of "debuggable" TUs, and then either convince your coworkers to let you merge the change or maintain it for yourself on a private branch.

Alternatively, you may be able to bypass the build system entirely. If your codebase has a compile_commands.json so that clangd can provide accurate intellisense, then you can re-purpose it to help you. The compilation database will have compiler commands for every TU in your project. You want to write a script that 1) runs a normal optimized build of your project, 2) grabs the compiler commands for your "debuggable" TUs, re-writes them with `--ggdb3 -O0` flags, and runs them, and 3) re-runs the linker command to relink the executable with the new debuggable object files.

Alternatively, gcc, clang, and msvc each provide pragmas that control optimizations for individual functions or ranges of functions: [^pragma_fix]

[^pragma_fix]: Thanks to HN users `forrestthewoods`, `o11c`, and `bialpio` for pointing out [here](https://news.ycombinator.com/item?id=41101725) that these pragmas exist.

For gcc, add `#pragma GCC optimize ("O0")` to the top of your "debuggable" source files, and compile the entire project with `--ggdb3 -O3`.

For clang, add `#pragma clang optimize off` to the top of your "debuggable" source files, and compile the entire project with `--ggdb3 -O3`.

### Why
C++ is often used for code that has to be fast. Unoptimized C++ code can be very slow, especially in large projects. Note that when debugging you often have a pretty good idea of roughly where the bug is going to be, even if you don't know exactly what's going wrong. And the ABI of the generated code doesn't depend on the optimization level, so it is possible to link together optimized and unoptimized TUs. So then, a reasonable strategy is to identify the TUs that have to be debugged, and then only compile those without optimizations, and compile the rest of the project with optimizations.

Note that we do still want debug information for the optimized TUs. This will always make our backtraces more informative, and we will sometimes be wrong about where the bug is, so it would be nice to poke around in the optimized TUs for a bit to gather information before we recompile (although the debugging experience will be worse).

Also note that sometimes a bug will only appear in optimized code. Usually this means that you have triggered undefined behavior, which the optimizer is taking advantage of to generate faster code. Hopefully UBSan is able to catch this for you, and if UBSan can't and the issue isn't obvious from the source then you should look backwards from the error and examine assembly to see where the compiler has done something weird.

Note that g++ recommends using `-Og` instead of `-O0` for the best debugging experience. But this will still inline functions and optimize out local variables, so I don't recommend using it. `-Og` is probably a decent choice if you have to compile your entire program at a single optimization level, but we can do even better with our split strategy.
### Ref
- [GCC manual on optimization levels](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)
- [GCC manual on optimization pragmas](https://gcc.gnu.org/onlinedocs/gcc/Function-Specific-Option-Pragmas.html)
- [Clang manual on optimization pragmas](https://clang.llvm.org/docs/LanguageExtensions.html#extensions-for-selectively-disabling-optimization)
- [MSVC manual on optimization pragmas](https://learn.microsoft.com/en-us/cpp/preprocessor/optimize?view=msvc-170)
## Explicitly instantiate important template classes
Explicitly instantiate every template class specialization that you want to debug.
### How
Add lines like `template class std::vector<Foo>;` to a single translation unit (in a cc / source file).

### Why
In C++, a member function of a template class is only instantiated if it is used, and this implicit instantiation is separate from the implicit instantiation of the surrounding template class. So, for example, if you want to be able to fully debug a `std::vector<Foo>`, then you need to have used every member function of `std::vector`, specifically on a `std::vector<Foo>`. It doesn't count to have used the member function on a `std::vector<Bar>`, because each template class is independent.

Confusingly, gdb will suggest that the function "may have been inlined", when the actual problem is that the template member function was never generated in the first place.

I think that it is reasonable to want to use any function from the class template on any specialization while debugging.

The way to get this behavior reliably is to explicitly instantiate the template class, which will ensure that all member functions are instantiated, even the ones that you do not use.

Note that Arthur O'Dwyer, who is substantially more qualified than I am to be giving advice on this, has an article where he explicitly and directly says not to do the thing that I am telling you to do. He is correct that some classes cannot be explicitly instantiated for all valid template arguments, but I am going to do it anyway because 1) it usually works, 2) it is obvious when it doesn't work, and 3) we are writing quick debugging hacks and not doing software engineering. Be aware that it may be a bad idea to leave explicit template instantiations of STL classes in your production code.
### Ref
- [Arthur O'Dwyer explicitly saying to never do the thing that I am telling you to do anyway](https://quuxplusone.github.io/blog/2021/08/06/dont-explicitly-instantiate-std-templates/)
# Specific Source Changes
## Evaluate preprocessor ifdef's
Run [unifdef](https://dotat.at/prog/unifdef/) to evaluate preprocessor ifdefs.
### How
Install unifdef and run it in-place on a subset of your codebase's files using the -D defines that you are going to use for your build.
### Why
As far as I can tell, the main uses for ifdefs are 1) header guards, 2) platform-specific code, and 3) commenting out blocks of debug or otherwise unused code. (1) is almost never confusing and both (2) and (3) are things that you'll know in advance. You might as well use a tool to evaluate them and make the control flow easier to understand.

This tip is especially useful if you are working with a very old codebase that has tons of platform-specific ifdefs that make it difficult to understand the code. The ideal solution would be to drop support for old platforms and delete the ifdefs, but that is often not possible.

Unfortunately, unifdef is not perfect at parsing modern C++ code. I don't remember the exact issue, but I have had it fail to parse a single file before on a large codebase. So, my recommendation would be to use it selectively on the files that you care about debugging. Alternatively, you can try your luck and use it everywhere.
### Ref
- [unifdef homepage](https://dotat.at/prog/unifdef/)
## Expand complex macros
Run the preprocessor manually to expand complex macros.
### How
Identify a confusing macro. Use `g++ -E` to run the preprocessor on the TU and evaluate the macro. Copy the expanded macro over the original source code.
### Why
With `g++ -ggdb3`, you gain the ability to list or evaluate macros. But you don't have the ability to step through them. Expanding the macro within the source gives you the ability to step-through the expanded macro in the debugger, which can be very useful in certain projects.

Note that `g++ -E` also evaluates all ifdefs, and you can set the values for defines via the command line. I still prefer to use unifdef for evaluating ifdefs because it gives back clean source code that hasn't been fully preprocessed.
### Ref
- [GCC options controlling the preprocessor](https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html)
## Set up fast conditional breakpoints using the x86 INT3 trick
Modify the source to insert native-speed conditional breakpoints that can be turned on or off from inside the debugger.
### How 
```
volatile bool breakpoint_1 = false;
...
void func() {
...
    if (breakpoint_1 && (x_id == 153827)) {
        __asm("int3\n\tnop");
    }
...
}
```

```
(gdb) p breakpoint_1 = true
```

The `nop` instruction after the `int3` helps gdb understand the context of where the breakpoint fired [^int_fix] .

[^int_fix]: Thanks to HN user `amluto` for suggesting the `nop` instruction [here](https://news.ycombinator.com/item?id=41104749).

Make sure that `breakpoint_1` has external linkage (e.g. isn't static and isn't inside of an anonymous namespace) so that you can easily enable/disable it regardless of where your debugger is sitting in the stack.

### Why
If you create a conditional breakpoint from inside of gdb, then it will trap on every occurrence, evaluate your break condition, and continue if the break condition is not met. This can be very slow. gdb does it this way because it only requires overwriting a single byte of the binary, which it knows how to do safely.

The way that gdb sets a breakpoint is to temporarily replace an instruction with the single byte `int $3` instruction, which has opcode 0xCC. This instruction generates a software interrupt and allows gdb to take over control. Then, once the instruction is hit, gdb makes sure to also evaluate the single instruction that it had to remove.

But nothing stops us from just inserting an `int $3` instruction into our binary ourselves. And furthermore, since we are doing this before the program is compiled, it is easy for us to write a condition on when the instruction fires. This can be hugely faster because we are able to evaluate the condition without needing to do a software interrupt on every occurrence.

The condition variable should be volatile so that we can safely update the variable in the debugger in order to enable / disable our breakpoint. Using volatile means that the program will always read the variable from memory before using it.
### Ref
- [Wikipedia on the INT x86 instruction](https://en.wikipedia.org/wiki/INT_(x86_instruction))
# Debugger Configuration Changes
## Avoid stepping into irrelevant code
Configure gdb to step-over the stdlib, third-party libraries, your project's utility code, and maybe all "fast" TUs.
### How
Add lines like `gdb skip -gfi /usr/lib/c++` to your global or project-specific `.gdbinit` file.
Also add lines for any third-party libraries or fast TUs that you would like to always step-over.
### Why
I often want to rapidly step through a function and step-into related code without ever stepping into core layers like the stdlib. When I am debugging my code, it is usually because I have a bug within my code, and I want to treat the stdlib and most parts of the project as a black box by default.

This may not sound like a big deal, but it can be really frustrating. For example, let's say that I want to step into a function call that takes a lot of arguments. Before actually stepping into the function call, gdb will step into each of the argument expressions. If one of those expressions calls a constructor, then gdb will step into the constructor and switch to a different file. A simple attempt to step into a function call at point can turn into dozens of step/next/finish commands spanning several files before you get where you want to go. It is often easier to just set a breakpoint on the function and continue.

The key insight is that you probably know in advance that you never want to step into most of those argument expression constructors, because they are probably for stdlib classes or small utility classes that you would like to treat as black boxes. After all, if you're constructing a class inside an argument list then it is probably something simple.

Luckily, gdb can be configured to always step-over arbitrary files and directories. We should take advantage of this and blacklist code that we don't usually want to step-into. For example: the stdlib, third-party dependencies, utility classes, custom string or enumeration classes, or classes that make heavy use of template meta-programming.
### Ref
- [StackOverflow answer on skipping over specific files and directories](https://stackoverflow.com/a/61866506)
## Enable stdlib pretty-printers
Enable gdb pretty-printers for the stdlib containers.
### How
This depends on your Linux distribution and your version of gdb. Run the following command inside gdb while attached to your running process to see if the stdlib pretty-printers are installed and available.

```
(gdb) info pretty-printer
```

Note that just running `info pretty-printer` inside a fresh gdb that is not attached to anything will not tell you if the stdlib pretty-printers are available. The pretty-printers are associated with a particular stdlib version, and so you need to have loaded a binary that is linked with a stdlib.
### Why
Improve the signal-to-noise ratio when printing stdlib containers inside the debugger. Reduce the mental load of debugging.

Note that gdb pretty-printers are the partial solution to template hell for debuggers. They complement C++20 concepts, which are the partial solution to template hell for compilers.
### Ref
- [GDB manual on using pretty-printers](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Pretty_002dPrinter-Commands.html)
## Write pretty-printers for your project's vocabulary types
Use the gdb Python API to write pretty-printers for your project's frequently-used classes that have a meaningful short text description that summarizes a complicated and confusing implementation.
### How
Refer to the gdb manual.
### Why
Improve the signal-to-noise ratio when printing objects inside the debugger. This is analogous to writing a custom `__str__` function on a Python object, except less useful because it only works within the debugger.

Especially consider writing pretty-printers for any core "vocabulary types" within your codebase that have a tricky implementation. A vocabulary type is a type that is commonly passed around across interfaces. Because they are commonly used, there is a high payoff for making them readable. Many vocabulary types will be basic or standard types, but you probably have a few custom ones in your codebase.

Note that gdb pretty-printers are the partial solution to template hell for debuggers. They complement C++20 concepts, which are the partial solution to template hell for compilers.
### Ref
- [GDB manual on writing a pretty-printer](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Writing-a-Pretty_002dPrinter.html)
- [Vocabulary types](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2125r0.pdf)

*Thank you to [Eliot Robson](https://eliotwrobson.github.io/#about) for providing feedback on drafts of this post. All mistakes are my own.*
