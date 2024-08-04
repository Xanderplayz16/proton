# Hello, World!

## Creating a project

Assuming you have Proton installed (if you don't, see [Installation](installation.md)), you can first create a directory for the project, and then create a new project using the built-in project management system.

`python -m proton project init --dir [project directory]`

You can see that 2 folders were created in the project directory, `src` and `web`. Both of these are used for storing code.

Let's take a look at `web`. As you can see, there is just one file. `index.html`. If you open up a code editor on it, you can see it is just a HTML Hello, World. 

Now, let's look back a directory, into `src`. There is only one file here (for now), main.py. If you open this up, you can see that it imports proton (as pt), declares a Window object with 2 arguments, the window name ('A Proton webapp') and the path of the HTML directory ("web"). After that, it calls window.start() with one argument, `debug = True`, which enables inspect element, and a couple neat debugging features. If you run this with `python -m proton project run`, it opens a Hello, World app, just what you probably expected. 

You might be thinking: `I need to distribute this to someone who doesn't know how to install dependecies, or python itself!` No worries, just run `python -m proton build --verbose` in the project root directory. It does take a while, but once it is done, a compiled executable (main.exe or main.bin on unix-likes) should be in the `dist` directory. As you can see, once you run main.exe, it works just as it did uncompiled.
