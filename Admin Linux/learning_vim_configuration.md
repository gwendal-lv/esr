# Beyond the basics

By now you have used enough `vim` to see it's tremendous text editing potential.
Out of the box it works very well, but with some additional configuration and a few plugins installed it get's even better.
We'll go over all basic aspects of tweaking your `~/.vimrc` file from some welcome changes, some aesthetic to a complete IDE. 
For IDE features we'll focus on `python3` and `bash` but I'll leave some links to point you in the right direction for other languages.
The point of this chapter is not to race towards the end but to understand what every step adds to your working comfort.
I highly advise to take the changes to your vimrc *slowly* and see if you actually *like* the change.
If you don't like a feature you don't have to use it, but it's still good to be aware of where you can take vim for future reference.

## Which vim to install

A simple `sudo apt install vim` installs a *basic* version of vim but when you're on a server and need to do some scripting it's a better idea to install `vim-nox`.
What's the difference?
We can get some information about both packages via `sudo apt-cache show vim vim-nox`.

Classic vim will give you the following description:

```
Description-en: Vi IMproved - enhanced vi editor
 Vim is an almost compatible version of the UNIX editor Vi.
 .
 Many new features have been added: multi level undo, syntax
 highlighting, command line history, on-line help, filename
 completion, block operations, folding, Unicode support, etc.
 .
 This package contains a version of vim compiled with a rather
 standard set of features.  This package does not provide a GUI
 version of Vim.  See the other vim-* packages if you need more
 (or less).
```

And vim-nox the following:

```
Description-en: Vi IMproved - enhanced vi editor - with scripting languages support
 Vim is an almost compatible version of the UNIX editor Vi.
 .
 Many new features have been added: multi level undo, syntax
 highlighting, command line history, on-line help, filename
 completion, block operations, folding, Unicode support, etc.
 .
 This package contains a version of vim compiled with support for
 scripting with Lua, Perl, Python 3, Ruby, and Tcl but no GUI.

```

I would *always* install vim-nox but this is personal preference.
Some people like the graphical versions of vim, or `gvim`, but I'm not a fan.
Maybe try the vim-gtk package to see if you like it.
Do keep in mind that the program you'll invoke is **always** `vim` no matter which version you install!
For graphical vim you'll invoke `gvim`.

**From here on out I expect a vim-nox installed!**

## Basic improvements

You'll probably always want to include the following in your vimrc.
You can [download](./assets/vimrc_basic) the file if you want to try it out but do take the time to read the comments.

```vim
" ----------------------------------------------------------------------------
" basic essentials
" ----------------------------------------------------------------------------

" don't make vim vi compatible (if not set you miss out on a lot of features!)
" you'll see this option set in most configuration files found online
set nocompatible

" enable filetype recognition plus indent and plugin (pretty much mandatory)
filetype plugin indent on

" enable syntax highlighting
syntax on

" backspace can be a tricky thing and this setting makes it work a lot better
set backspace=indent,eol,start

" when tab completing on the expert line you don't want to miss out on EDIT vs
" edit or nerdtree vs NERDTree and this setting ignores case completely
set ignorecase

" highlight your search patterns (very handy when building regexes)
set hlsearch

" highlight the search pattern as-you-go (tremendously helpful when
" constructing regexes)
set incsearch

" always show a status line at the bottom of your vim which shows some basic 
" information about the file, which line you're at etc
set laststatus=2

" show files in statusbar when opening via expert mode
set wildmenu

" also show all possible expert mode commands in the statusline
set wildmode=full

" reverse numbering (in the sideline) so you don't have to manually count how
" many lines you have to yank
set rnu

" it's also nice to still have your absolute line number in the sideline
set nu

" can do copy paste from the clipboard
set clipboard=unnamedplus
```

You can test out the vim configuration above by downloading it to your home directory and telling vim explicitly you want *that* vimrc by invoking `vim -u ~/vimrc_basic test.py` where `test.py` is just an example.
Each setting has some information about what it does but vim comes with built-in help.
You can invoke this help by pressing `:help laststatus`.

## Getting help

![vim help](./assets/vim_01.png)

Now, what has happened here?
Vim opened it's own documentation in a new *horizontal split* and moved the cursor there.
At first this is very intimidating but there are just a few command you need to know to manage this situation perfectly.
Don't worry about messing up the documentation, it's opened in read only mode.

* you can read the documentation by pressing `j` to go down and `k` to go up
* to navigate splits you use `CRTL-w j` to go down, `CRTL-w k` to go up, `CTRL-w l` to to right and `CRTL-w h` to go left
* to close the documentation you need to be *inside* the documentation split and press `:close` which means it will close the split you're in (if your cursor is on the **other** split you can use `:only` which does the opposite)

The `CTRL-w` affair is a shortcut to vim's window navigation.
You can read up a bit more in the manual at `:help window` but below is the gist of it.
It might sound a bit confusing at the start but think of `tmux` and it's *panes, splits and windows* and it might make some more sense.

```
Summary:
   A buffer is the in-memory text of a file.
   A window is a viewport on a buffer.
   A tab page is a collection of windows.

A window is a viewport onto a buffer.  You can use multiple windows on one
buffer, or several windows on different buffers.

A buffer is a file loaded into memory for editing.  The original file remains
unchanged until you write the buffer to the file.

A buffer can be in one of three states:

							*active-buffer*
active:   The buffer is displayed in a window.  If there is a file for this
	  buffer, it has been read into the buffer.  The buffer may have been
	  modified since then and thus be different from the file.
							*hidden-buffer*
hidden:   The buffer is not displayed.  If there is a file for this buffer, it
	  has been read into the buffer.  Otherwise it's the same as an active
	  buffer, you just can't see it.
							*inactive-buffer*
inactive: The buffer is not displayed and does not contain anything.  Options
	  for the buffer are remembered if the file was once loaded.  It can
	  contain marks from the |viminfo| file.  But the buffer doesn't
	  contain text.
```

If you actually read the documentation you must have noticed you can make tabs, as in firefox tabs, in vim!
I tend to mostly use buffers, based on [this](https://stackoverflow.com/questions/26708822/why-do-vim-experts-prefer-buffers-over-tabs) philosophy but you do you.
As for window navigation I add the following to my vimrc but you will probably not like it too much.
This remaps the arrow keys, which you should **not** be using for navigation text anyway, to window navigation.
If the `nnoremap` makes no sense try `:help mapping`.

```vim
" use the arrows for buffer navigation
nnoremap <down> <C-W><C-J>
nnoremap <up> <C-W><C-K>
nnoremap <left> <C-W><C-H>
nnoremap <right> <C-W><C-L>
```

## Switching quickly from config file to config file

A lot of information about vim online is geared towards programmers and not system administrators but I have a trick for you that will probably help you quite a bit when modifying configuration files.
You have to get comfortable with opening and navigating buffers first so a quick rundown on the basics.
To do this exercise properly first prepare the following files by executing the commands below.

```bash
echo "I am a first file" > ~/first_file.txt
echo "[unit]\nDescription=looks like a config file\nManual=maybe systemd\n" > ~/test.service
echo "import datetime\n\nd = datetime.datetime.now()\nprint(d)" >python_test.py
```

### Part one

1. Open up vim with my basic vimrc you downloaded above and you should have a blank vim in front of you.
2. Type `:edit ~/first_file.txt` to open up the first file.
3. Type `:edit ~/test.service` to open up the second file.
4. Type `:edit ~/python_test.py` to open up the third file.

You have now opened up all three files in one vim but how do you switch from one to the other?
They are loaded in memory and are called buffers.
To list all buffers currently opened in vim you type `:buffers` and you should see a list like the one below.

```vim
:buffers
  1      "first_file.txt"               line 1
  2 #    "test.service"                 line 1
  3 %a   "python_test.py"               line 1
Press ENTER or type command to continue
```

To go back to the buffer you where are just hit enter but if you want to **switch** to a different one type `:b 1`.
This will take you to the first buffer.
As you are opening and editing files in the same instance of vim you can yank and paste from one to the other!
Try playing around with this and make some changes to some files. 
At some point you'll be confronted with the following message.

```vim
E37: No write since last change (add ! to override)
```

This means you're trying to switch to an other buffer but you have unsaved changes in the one you're currently at.
I like to add the following to my vimrc to automatically save a buffer upon leaving.
Do keep in mind it can be a bit dangerous to overwrite files you're not too certain about.

```vim
" automatically save buffers
set autowrite
set autowriteall 
```

Once you feel comfortable move on to the next part.

### Part two

OK, quit vim completely and go to your home directory, where you created the three files before.
Open vim up again with my basic configuration but instead of `:edit` use `:find tes<TAB>` where <TAB> is your tab complete key.
Vim should list all files matching the `tes` pattern inside the folder you're in.
We can supercharge this behaviour by modifying the `path` vim will search in.
To see which paths are searched by default type `:set path` and you'll probably see `path=.,/usr/include,,`.
This is nice from a *programmers* point of view but we can change it to suit our administrator's point of view better.
To completely override we can change the setting by typing `:set path=/etc/**` and vim will now search our `/etc` folder **recursively**.
Try it out with `:find ssh<TAB>` to see it's full power!
This is a setting you can either fix in your vimrc, or change in the fly, your choice.

**Don't be greedy and set it to the root of your hard drive.
This will slow vim down way too much because there are just too many files and folders!**

## IDE like features without plugins

We already have syntax highlighting via the `set syntax=on` feature but we can also have autocomplete for quite a lot of scripting languages out of the box.
This is one of the main reasons we install vim-nox and not vim!
The shortcut to achieve it is a double whammy `<c-x><c-o>` which triggers omnicomplete.
Have a look at `:help omnifunc` to learn more about it but first, a hands on example.

1. Open the python file we made before with `vim -u ~/vimrc_basic ~/python_test.py`
2. Navigate to the end of the file, go into **insert** mode and type `datetime.`
3. Remain in insert mode after the `.` and hit `<c-x><c-o>`
4. Stay calm and read on.

![autocomplete](./assets/vim_02.png)

The screenshot above is probably very much like what you're confronted with.
The *dropdown* menu is a context aware autocomplete menu meaning these are all functions, methods, classes or variables belonging to this module.
The horizontal split window at the top shows the documentation of the menu item you have selected. 
You can navigate this list either with the *arrows* or with `<c-n>` to go down and `<c-p>` to go up.

I personally don't like the documentation jumping up and down on my screen so you can add the following to remove it all together.
Now to be able to view the documentation we'll need to install some plugins.
I have not found a clean way of hiding the preview window *and* adding a shortcut to show documentation.

```vim
set completeopt-=preview
```

### Complete more things

Vim can do a lot more than just complete python code.
When you press `<c-x>` you'll see a menu at the bottom along these lines.

```vim
-- ^X mode (^]^D^E^F^I^K^L^N^O^Ps^U^V^Y)
```

Every `^CHARACTER` is a different mode of autocomplete!
Try out the `^K` one just for fun.
It will probably say this the following.

```vim
'dictionary' option is empty
```

We can *set* a dictionary, which is just a list of words, to autocomplete from.
Let me walk you through an example.

1. Open up a blank text file with my basic vimrc.
2. Go into **insert** mode and type in `hipp`.
3. Stay in **insert** mode and type `<c-x><c-k>` which will show the same error message as before.
4. Exit insert mode with `ESC`
5. Set the dictionary by typing `:set dictionary=/usr/share/dict/american-english` (you should have this file)
6. Go into **insert** moder after `hipp` and type `<c-x><c-k>` again.

Nice no?
You can set this dictionary file to any text file you want and it will autocomplete from it.

## Beyond vanilla vim

You can extend vim's behavior by installing plugins.
There are to ways to do this, either manually by telling vim to source the plugin files, or to use a **plugin manager**.
I *highly* advise you to use a plugin manager.
There are multiple to choose from but I always go with [Vundle](https://github.com/VundleVim/Vundle.vim), mostly out of habit.
You're of coarse free to use any plugin manager you want but from here on out I assume you're using Vundle.

### Installing Vundle

First we'll need to install Vundle itself.
This is done by cloning the repository.
Make sure you have `git` and `curl` installed on your machine!

```bash
➜  ~ git:(master) ✗ sudo apt install git curl                    
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
curl is already the newest version (7.74.0-1.3+b1).
git is already the newest version (1:2.30.2-1).
0 upgraded, 0 newly installed, 0 to remove and 7 not upgraded.
➜  ~ git:(master) ✗ 
```

If this is the case you can go ahead and clone Vundle!
This will install Vundle to your home directory in a `~/.vim/bundle` folder.

```bash
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
```

Next we need to add a few **essential** lines to the vimrc.
Without this Vundle won't work!
Notice the `" ADD PLUGINS HERE`; this is where we will put links to the github plugins we want to install.
Vundle will take care of the installation with the `:VundleInstall` command.

```vim
" ----------------------------------------------------------------------------
" vundle essentials
" ----------------------------------------------------------------------------

set nocompatible
filetype off

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim

call vundle#begin()
Plugin 'VundleVim/Vundle.vim'

" ADD PLUGINS HERE

call vundle#end()

filetype plugin indent on
```

### Adding some basic plugins

We'll install a few basic plugins first.
The following projects are some I deem pretty essential but your milage may vary.

* [autopairs](https://github.com/jiangmiao/auto-pairs) to autmatically add matching closing brackets etc
* [NERDTree](https://github.com/preservim/nerdtree) to add a file browser to vim

You can find installation instructions on their git pages but it's most of the time pretty simple.
Between the `call vundle#begin()` and the `call vundle#end()` functions we'll add the plugins on separate lines.
Each plugin is a path to the github `$USERNAME/$REPOSITORYNAME`.
Once they are added we need to install them and this is done by calling `:VundleInstall`.

![installing plugins](./assets/vim_03.png)

It's done!
To close this window we can call `:close` and try out our plugins.
Open up a new text file with `:edit plugintest.md` and try the autopairs by typing any brackets you want.
The corresponding closing bracket will insert automatically.
To open up the NERDTree plugin type `:NERDTreeToggle` to show and hide the file browser.

### Configuring the plugins

To show and hide NERDTree a lot of people *map* a keyboard shortcut to the `:NERDTreeToggle` command.
This can be done by adding a configuration line **after** the plugin is loaded.
I tend to have three basic blocks in my vimrc and I would advise you to do the same.

1. load vundle and the plugins
2. my basic modifications
3. plugin configuration

So all the way at the bottom of my vimrc I would add the following.

```vim
" map a keyboard shortcut to show and hide NERDTree
nnoremap <C-t> :NERDTreeToggle<CR>
```

It's also nice to automatically close NERDTree when it's the last window left.
To do this we add the following (taken from the github documentation).

```vim
" Exit Vim if NERDTree is the only window remaining in the only tab.
autocmd BufEnter * if tabpagenr('$') == 1 && winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | quit | endif
```

Our full vimrc config now looks like this and can be downloaded [here](./assets/vimrc_vundle).

```vim
" ----------------------------------------------------------------------------
" vundle essentials
" ----------------------------------------------------------------------------

set nocompatible
filetype off

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim

call vundle#begin()
Plugin 'VundleVim/Vundle.vim'

" ADD PLUGINS HERE
Plugin 'jiangmiao/auto-pairs'
Plugin 'preservim/nerdtree'

call vundle#end()

filetype plugin indent on

" ----------------------------------------------------------------------------
" basic essentials
" ----------------------------------------------------------------------------

" don't make vim vi compatible (if not set you miss out on a lot of features!)
" you'll see this option set in most configuration files found online
set nocompatible

" enable filetype recognition plus indent and plugin (pretty much mandatory)
filetype plugin indent on    " required

" enable syntax highlighting
syntax on

" backspace can be a tricky thing and this setting make it work a lot better
set backspace=indent,eol,start

" when tab completing on the expert line you don't want to miss out on EDIT vs
" edit or nerdtree vs NERDTree and this setting ignores case completely
set ignorecase

" highlight your search patterns (very handy when building regexes)
set hlsearch

" highlight the search pattern as-you-go (tremendously helpful when
" constructing regexes)
set incsearch

" always show a status line at the bottom of your vim which shows some basic 
" information about the file, which line you're at etc
set laststatus=2

" show files in statusbar when opening via expert mode
set wildmenu

" also show all possible expert mode commands in the statusline
set wildmode=full

" reverse numbering (in the sideline) so you don't have to manually count how
" many lines you have to yank
set rnu

" it's also nice to still have your absolute line number in the sideline
set nu

" can do copy paste from the clipboard
set clipboard=unnamedplus

" automatically save buffers
set autowrite
set autowriteall 

" hide the documentation popup
set completeopt-=preview

" ----------------------------------------------------------------------------
" plugin configuration
" ----------------------------------------------------------------------------

" NERDTree
" --------

" map a keyboard shortcut to show and hide NERDTree
nnoremap <C-t> :NERDTreeToggle<CR>

" Exit Vim if NERDTree is the only window remaining in the only tab.
autocmd BufEnter * if tabpagenr('$') == 1 && winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | quit | endif
```

## Going full power

There is a lot of online debate on which plugins to use, which autocomplete engine is the best, if you even need anything beyond vanilla vim, etc.
From here on out I'll just list my current personal preferences.
I've done quite a bit of tweaking an testing over the years and this list can be a shortcut for you to not having to debug as much.

For me, autocomplete is essential.
I don't really understand *how* you can learn how to code without.
This being said, I use autocomplete for all sorts of things ranging from email to code and configuration files.
The modern way of doing autocomplete is to do it *asynchronous* meaning vim won't freeze when it's waiting on a list of possible candidates.
I'm a pretty big fan of the [Language Server Protocol](https://en.wikipedia.org/wiki/Language_Server_Protocol) and the world seems to agree it's the way to go.

For vim I use the following plugins as a bare minimum.

* [asyncomplete.vim](https://github.com/prabirshrestha/asyncomplete.vim) to offer async completion
* [vim-lsp](https://github.com/prabirshrestha/vim-lsp) which is a LSP client written in vimscript
* [asyncomplete-lsp.vim](https://github.com/prabirshrestha/asyncomplete-lsp.vim) 
* [mattn/vim-lsp-settings](https://github.com/mattn/vim-lsp-settings) which makes it *super* easy to install new language servers
* [yami-beta/asyncomplete-omni.vim](https://github.com/yami-beta/asyncomplete-omni.vim) to offer omni complete async
* [prabirshrestha/asyncomplete-file.vim](https://github.com/prabirshrestha/asyncomplete-file.vim) adds file path autocomplete

This might seem like a lot but they are all pretty neat plugins that work super well together.
With this installed vim becomes a language server client and a client is nothing without a server.
You can see a list of suppored servers [here](https://github.com/mattn/vim-lsp-settings) and mattn/vim-lsp-settings makes it super easy to install one.
In order for it all to work, for python and bash, you should do a systemwide installation of python3-pip, python3-venv and npm with the following command.

```bash
sudo apt install -y python3-pip python3-venv npm
```

For python just install the above mentioned plugins and open up a python file.
You'll be prompted to install [pyls](https://github.com/palantir/python-language-server) which is a very good language server.
Type `:LspInstallServer pyls-all`, wait for it to finish and you're good to go!
It might take some time to get everything initialized properly the first time you launch it, but that's quite normal.

For bash you'll need the npm package installed.
If that's the case you just open up a script and you'll be prompted to install the server.
Type `:LspInstallServer bash-language-server`, wait a bit and you're good to go!

## Wrapping up

That's it!
Your vim should now be fully charged to tackle any job you throw at it.
The full configuration file can be seen below and downloaded [here](./assets/vimrc_vundle_ide)

![full featured vim](./assets/vim_04.png)

```vim
" ----------------------------------------------------------------------------
" vundle essentials
" ----------------------------------------------------------------------------

set nocompatible
filetype off

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim

call vundle#begin()

" let vundle manage vundle...
Plugin 'VundleVim/Vundle.vim'

" Basic plugins
Plugin 'jiangmiao/auto-pairs'
Plugin 'preservim/nerdtree'
Plugin 'jeetsukumaran/vim-buffergator'

" IDE like plugins
Plugin 'prabirshrestha/asyncomplete.vim'
Plugin 'prabirshrestha/vim-lsp'
Plugin 'prabirshrestha/asyncomplete-lsp.vim'
Plugin 'mattn/vim-lsp-settings'
Plugin 'yami-beta/asyncomplete-omni.vim'
Plugin 'prabirshrestha/asyncomplete-file.vim'

" Language autocomplete for English
Plugin 'htlsne/asyncomplete-look'

" an additional colorscheme I like
Plugin 'altercation/vim-colors-solarized'

call vundle#end()

filetype plugin indent on

" ----------------------------------------------------------------------------
" basic essentials
" ----------------------------------------------------------------------------

" don't make vim vi compatible (if not set you miss out on a lot of features!)
" you'll see this option set in most configuration files found online
set nocompatible

" enable filetype recognition plus indent and plugin (pretty much mandatory)
filetype plugin indent on    " required

" enable syntax highlighting
syntax on

" backspace can be a tricky thing and this setting make it work a lot better
set backspace=indent,eol,start

" when tab completing on the expert line you don't want to miss out on EDIT vs
" edit or nerdtree vs NERDTree and this setting ignores case completely
set ignorecase

" highlight your search patterns (very handy when building regexes)
set hlsearch

" highlight the search pattern as-you-go (tremendously helpful when
" constructing regexes)
set incsearch

" always show a status line at the bottom of your vim which shows some basic 
" information about the file, which line you're at etc
set laststatus=2

" show files in statusbar when opening via expert mode
set wildmenu

" also show all possible expert mode commands in the statusline
set wildmode=full

" reverse numbering (in the sideline) so you don't have to manually count how
" many lines you have to yank
set rnu

" it's also nice to still have your absolute line number in the sideline
set nu

" can do copy paste from the clipboard
set clipboard=unnamedplus

" automatically save buffers
set autowrite
set autowriteall 

" spaces not tabs for coding purposes
set sw=4
set ts=4
set sts=4

" mouse usage can be handy, especially when using LspPeekDefinition
set mouse=a

" enable code folding
set foldmethod=indent

" set SPACE to toggle a fold
nnoremap <SPACE> za

" set the leader key for shortcuts (uncomment if you don't want it to be the
" default \ key
"let mapleader=";"

" ----------------------------------------------------------------------------
" plugin configuration
" ----------------------------------------------------------------------------

" NERDTree
" --------

" map a keyboard shortcut to show and hide NERDTree
nnoremap <C-t> :NERDTreeToggle<CR>

" Exit Vim if NERDTree is the only window remaining in the only tab.
autocmd BufEnter * if tabpagenr('$') == 1 && winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | quit | endif

" vim-lsp
" -------

" general vim-lsp settings
" ------------------------

" maps quite q few keyboad shortcuts
" this is taken staight off the github page with one added shortcut to peak at
" the definition of a function or class
function! s:on_lsp_buffer_enabled() abort
	setlocal omnifunc=lsp#complete
    setlocal signcolumn=yes
    if exists('+tagfunc') | setlocal tagfunc=lsp#tagfunc | endif
    nmap <buffer> gd <plug>(lsp-definition)
    nmap <buffer> gpd <plug>(lsp-peek-definition)
    nmap <buffer> gs <plug>(lsp-document-symbol-search)
    nmap <buffer> gS <plug>(lsp-workspace-symbol-search)
    nmap <buffer> gr <plug>(lsp-references)
    nmap <buffer> gi <plug>(lsp-implementation)
    nmap <buffer> gt <plug>(lsp-type-definition)
    nmap <buffer> <leader>rn <plug>(lsp-rename)
    nmap <buffer> [g <plug>(lsp-previous-diagnostic)
    nmap <buffer> ]g <plug>(lsp-next-diagnostic)
    nmap <buffer> K <plug>(lsp-hover)
    inoremap <buffer> <expr><c-f> lsp#scroll(+4)
    inoremap <buffer> <expr><c-d> lsp#scroll(-4)

    let g:lsp_format_sync_timeout = 2000
    autocmd! BufWritePre *.rs,*.go call execute('LspDocumentFormatSync')
endfunction

augroup lsp_install
    au!
    " call s:on_lsp_buffer_enabled only for languages that has the server registered.
    autocmd User lsp_buffer_enabled call s:on_lsp_buffer_enabled()
augroup END

" asyncomplete
" ------------

" make tab complete work
inoremap <expr> <Tab>   pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
inoremap <expr> <cr>    pumvisible() ? asyncomplete#close_popup() : "\<cr>"

" force refresh with CTRL-SPACE
imap <c-@> <Plug>(asyncomplete_force_refresh)

" asyncomplete-file
" -----------------

au User asyncomplete_setup call asyncomplete#register_source(asyncomplete#sources#file#get_source_options({
	\ 'name': 'file',
    \ 'allowlist': ['*'],
    \ 'priority': 10,
    \ 'completor': function('asyncomplete#sources#file#completor')
    \ }))

" asyncomplete-omni
" -----------------

autocmd User asyncomplete_setup call asyncomplete#register_source(asyncomplete#sources#omni#get_source_options({
	\ 'name': 'omni',
	\ 'allowlist': ['*'],
	\ 'blocklist': ['c', 'cpp', 'html'],
	\ 'completor': function('asyncomplete#sources#omni#completor'),
	\ 'config': {
	\   'show_source_kind': 1,
	\ },
	\ }))

" asyncomplete-look
" -----------------

au User asyncomplete_setup call asyncomplete#register_source({
	\ 'name': 'look',
    \ 'allowlist': ['text', 'markdown'],
    \ 'completor': function('asyncomplete#sources#look#completor'),
    \ })

" ----------------------------------------------------------------------------
" visual configuration
" ----------------------------------------------------------------------------

" set a colorscheme
colorscheme solarized
set background=dark

" do soft wrap of text but not in the middle of words
set wrap linebreak nolist

" don't do hard wraps in any files
set textwidth=0

" add a color column at the 80 char
set colorcolumn=80

" spelling highlight needs to be done after the colorscheme load                
highlight SpellBad term=underline cterm=underline 

" enable English spellchecking in markdown files
autocmd FileType markdown setlocal spell
autocmd FileType markdown setlocal spelllang=en
```

### Notes

`man systemd.unit 2>/dev/null| grep --color -P "^[[:space:]]{2,}[[:<:]][A-Z]\w+[=]{0,1}$" | sed -e 's/[[:space:]]//g'`
