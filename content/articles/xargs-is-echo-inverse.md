Title: xargs is the inverse function of echo
Date: 2024-04-12 09:00
Category: Blog

<style>
code {
  white-space : pre-wrap !important;
}
</style>

`xargs` is a particularly confusing unix command. I want to share my trick for understanding how it works.

Let's look at the abbreviated [tldr](https://tldr.sh/) output for xargs:

```
$ tldr xargs
xargs

 - Run a command using the input data as arguments:
   {{arguments_source}} | xargs {{command}}
```

So, for example, if you had a file named `files_to_delete` with the contents below:
```
obsolete_note.md
yucky_recipe.pdf
cringe_tiktok.mov
```

Then you could run the following line to delete each of the files [^cat_abuse]:
```
$ cat files_to_delete | xargs rm
```

[^cat_abuse]: I am aware that this is a [useless use of cat](https://porkmail.org/era/unix/award).

Which reduces to the following command:
```
$ rm obsolete_note.md yucky_recipe.pdf cringe_tiktok.mov
```

This is a general pattern that shows up in a lot of contexts when writing shell pipelines. And as you might expect, this is because xargs implements a necessary and fundamental operation in shell scripting: converting input data from stdin to cmdline args.

For context, there are two separate and equally important ways to pass input to a unix program: stdin and cmdline args [^env]. Sometimes, a program's cmdline args determine what it expects on stdin. And in general, programs can have quite complex behavior with respect to their input. But the basic differences between the two input sources are:

[^env]: There is also the [environment](https://en.wikipedia.org/wiki/Environment_variable), but it is uncommon to explicitly use that in shell pipelines.

- stdin is an infinite text stream for ongoing input
- cmdline args is a fixed text array of start-of-program input

Here's a generic example of how to pass input to a command within a pipeline [^echo_heredocs]:

```
$ echo $STDIN_DATA | $CMD $ARGS_DATA # $CMD may need to be given input via $STDIN_DATA and/or $ARGS_DATA
```

[^echo_heredocs]: Note that `$STDIN_DATA` is the cmdline args for `echo` but the stdin for `$CMD`. Also note that we could have replaced echo with a [heredoc](https://en.wikipedia.org/wiki/Here_document).

For most programs, it is obvious what the cmdline args are, because they are written out in the pipeline. The tricky part of xargs is that it dynamically constructs the cmdline args for the program it calls based on its own stdin.

In our earlier example, xargs dynamically constructed the call `rm obsolete_note.md yucky_recipe.pdf cringe_tiktok.mov` based on its stdin. We couldn't tell what the arguments to rm would be based on the original pipeline text `cat files_to_delete | xargs rm`.

Interestingly, the echo command implements exactly the opposite operation to xargs in shell scripting: converting input data from cmdline args to stdin:

```
$ tldr echo
echo

 - Print a text message. Note: quotes are optional:
   echo "{{Hello World}}"
```

Both xargs and echo show up frequently in shell pipelines. I think that echo is less confusing because the mental model of shell pipelines is of self-contained commands passing their output forward to the next command, and echo is just a command that directly generates output from cmdline args. For example:

```
$ echo $ARGS | command_plus_args | command_plus_args # echo naturally fits into the pipeline mental model as a source of data over stdin
$ command_plus_args | xargs $CMD | command_plus_args # xargs does something weird and unexpected by dynamically constructing a command in the middle of the pipeline
```

See how xargs breaks the mental model by constructing a command dynamically at runtime based on the previous link in the chain, which is counter-intuitive.

But this is also why xargs is so powerful. Shell pipelines only pass data through stdin/stdout, but many unix programs require input via cmdline args, and xargs makes it possible to use those programs within a pipeline.

And so now we can state the trick for understanding xargs, which was also the title of this post: xargs is the inverse function of echo.

- `echo` is a function that maps cmdline args to stdin
- `xargs` is a function that maps stdin to cmdline args
- `xargs echo` is an identity function because `echo $DATA | xargs echo | $CMD` is equivalent to `echo $DATA | $CMD`
- `echo $DATA | xargs $CMD` is another identity function because it is equivalent to `$CMD $DATA`

In fact, without any arguments, `xargs` defaults to behaving like `xargs echo` because defaulting to an identity function is a sensible thing to do.

So, in order to remember what xargs does, just think about what echo does, and remember that xargs performs the inverse.

*Thank you to [Eliot Robson](https://eliotwrobson.github.io/#about) for providing feedback on drafts of this post. All mistakes are my own.*

