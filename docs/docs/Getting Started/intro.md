# Hello, World!

## Creating a project

Assuming you have Proton installed (if you don't, see [Installation](installation.md)), you can first create a directory for the project, and then create a new project using the built-in project management system.

`python -m proton project init --dir [project directory; argument not required if you are in the directory already]`

You can see that 2 folders were created in the project directory, `src` and `web`. Both of these are used for storing code.

Let's take a look at `web  `. As you can see, there is just one file. `index.html`. If you open up a code editor on it, you can see it is just a plain `<h1>`</h1> Hello, World! file. 

Now, let's look back a directory, into `src`. There is only one file here (for now), main.py. If you open this up, you can see that it imports proton (as pt), declares a Window object with 2 arguments, the window name ('A Proton webapp') and the path of the webs-app directory ("web"). After that, it calls window.start() with two arguments, `debug = True`, which enables inspect element, and a couple neat debugging features, and `gui = qt`, which just fixes some stuff on Linux. If you run this with `python src/main.py`, it pops up a plain, Times New Roman, Hello, World app, just what you probably expected. 

You might be thinking: `How is this a webapp framework if you can't build your projects, and they are stuck as python?` No worries, just run `python -m proton build --verbose` in the project root directory. It does take a while, but once it is done, a compiled executable (main.exe or main.bin on linux/mac) should be in the `dist` directory. As you can see, once you run main.exe, it is just like you probably expected, exactly the same as when you ran it in python form.


