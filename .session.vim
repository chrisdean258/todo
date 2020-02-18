let SessionLoad = 1
if &cp | set nocp | endif
let s:cpo_save=&cpo
set cpo&vim
inoremap <expr> <S-Tab> (pumvisible()?"\":"\\")
nnoremap <silent>  :nohlsearch
nnoremap    g
nnoremap  t :tabnew <cfile>
nnoremap  v :vs <cfile>
nnoremap  P "+P
nnoremap  p "+p
nnoremap <silent>  	 :tabnew
nnoremap  l l
nnoremap  k k
nnoremap  j j
nnoremap  h h
vnoremap <silent>  sw :call SwapArgs("visual")
nnoremap <silent>  sw :set opfunc=SwapArgsg@
vnoremap <silent>  w :call Wrap("visual")
nnoremap <silent>  w :set opfunc=Wrapg@
nnoremap  O O
nnoremap  o o
nnoremap <silent>  s% :source %
nnoremap <silent>  sv :silent source $MYVIMRC
nnoremap <silent>  ev :vsplit $MYVIMRC
nnoremap <silent>  g :call Indent()
noremap   <Nop>
nnoremap # :set hlsearch#zz
nnoremap * :set hlsearch*zz
nnoremap <expr> - MoveLineDown()
nnoremap <silent> . :call RepeatFunc().
nnoremap / :set hlsearch/
nnoremap ? :set hlsearch?
nnoremap N :set hlsearchNzz
nnoremap <silent> Q :tabprevious
nnoremap <silent> S<F12> <Nop>
nnoremap <silent> <expr> S SingleInsert("a")
nnoremap VJJJ Vjjj
nnoremap VJJ Vjj
nnoremap VJ Vj
nnoremap Y y$
nnoremap \p :set paste
vnoremap <silent> \\ :call Comment("visual")
nnoremap <silent> \\ :call Comment()
nnoremap <expr> _ MoveLineUp()
vmap gx <Plug>NetrwBrowseXVis
nmap gx <Plug>NetrwBrowseX
nnoremap gI g^i
nnoremap j gj
nnoremap k gk
nnoremap n :set hlsearchnzz
nnoremap <silent> s<F12> <Nop>
nnoremap <silent> <expr> s SingleInsert("i")
vnoremap <silent> <Plug>NetrwBrowseXVis :call netrw#BrowseXVis()
nnoremap <silent> <Plug>NetrwBrowseX :call netrw#BrowseX(expand((exists("g:netrw_gx")? g:netrw_gx : '<cfile>')),netrw#CheckIfRemote())
nnoremap <silent> <S-Tab> :tabnext
nnoremap <silent> <S-Down> :resize -5 
nnoremap <silent> <S-Up> :resize +5 
nnoremap <silent> <S-Left> :vertical resize -5 
nnoremap <silent> <S-Right> :vertical resize +5 
nnoremap <silent> <M-Right> :llast
nnoremap <silent> <M-Left> :lfirst
nnoremap <silent> <M-Down> :lprev
nnoremap <silent> <M-Up> :lnext
inoremap <expr> 	 (pumvisible()?"\":CleverTab())
imap  jki
imap JK jk
imap Jk jk
inoremap \p :set pastei
inoremap gqq gqqA
inoremap <expr> jk CleverEsc()
cabbr w!! %!sudo tee > /dev/null %
cabbr Q! =CommandLineStart(":", "q!", "Q!")
cabbr $$ =CommandLineStart(":", ".,$s", "$$")
cabbr a =CommandLineStart(":", "'a,.s", "a")
cabbr S =CommandLineStart(":", "%s", "S")
cabbr WQ =CommandLineStart(":", "wq", "WQ")
cabbr Wq =CommandLineStart(":", "wq", "Wq")
cabbr Q =CommandLineStart(":", "q", "Q")
cabbr W =CommandLineStart(":", "w", "W")
cabbr sp =CommandLineStart(":", "vs", "sp")
cabbr help =CommandLineStart(":", "vert help", "help")
cabbr jk SyntasticReset
let &cpo=s:cpo_save
unlet s:cpo_save
set autoindent
set autoread
set background=dark
set backspace=indent,eol,start
set backup
set backupdir=~/.vim/backup//
set cinoptions=(8,N-s,l1
set commentstring=<!--\ %s\ -->
set fileencodings=ucs-bom,utf-8,default,latin1
set helplang=en
set hidden
set incsearch
set infercase
set matchpairs=(:),{:},[:],<:>
set path=.,/usr/include,,,**
set printoptions=paper:letter
set pumheight=15
set ruler
set runtimepath=~/.vim,~/.vim/bundle/syntastic,~/.vim/bundle/vim-javascript,/var/lib/vim/addons,/usr/share/vim/vimfiles,/usr/share/vim/vim80,/usr/share/vim/vimfiles/after,/var/lib/vim/addons/after,~/.vim/bundle/vim-javascript/after,~/.vim/after
set scrolloff=5
set shiftwidth=0
set shortmess=filnxToOatI
set showcmd
set sidescroll=1
set sidescrolloff=5
set smartindent
set softtabstop=-1
set splitbelow
set splitright
set suffixes=.bak,~,.swp,.o,.info,.aux,.log,.dvi,.bbl,.blg,.brf,.cb,.ind,.idx,.ilg,.inx,.out,.toc
set switchbuf=usetab
set tabpagemax=1000
set tags=./tags,./TAGS,tags,./tags;/home/chris,./.tags;/home/chris
set termencoding=utf-8
set undodir=~/.vim/undo//
set undofile
set wildignore=*.o,*~,*.pyc,*/.git/*,*/.hg/*,*/.svn/*,*/.DS_Store
set wildmenu
set wildmode=longest,list,full
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/git/todo
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +3 templates/login.html
badd +0 templates/todo.html
argglobal
silent! argdel *
$argadd templates/login.html
edit templates/todo.html
set splitbelow splitright
wincmd t
set winminheight=1 winheight=1 winminwidth=1 winwidth=1
argglobal
inoremap <buffer> <expr>  HTMLCarriageReturn()
inoremap <buffer> <silent> > >:call EndTagHTML()a
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal backupcopy=
setlocal balloonexpr=
setlocal nobinary
setlocal breakindent
setlocal breakindentopt=
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,0#,!^F,o,O,e
setlocal cinoptions=(8,N-s,l1
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s:<!--,m:\ \ \ \ ,e:-->
setlocal commentstring=<!--%s-->
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'html'
setlocal filetype=html
endif
setlocal fixendofline
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
setlocal foldmethod=manual
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal formatprg=
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=-1
setlocal include=
setlocal includeexpr=
setlocal indentexpr=HtmlIndent()
setlocal indentkeys=o,O,<Return>,<>>,{,},!^F
setlocal infercase
setlocal iskeyword=@,48-57,_,192-255,$
setlocal keywordprg=
setlocal linebreak
setlocal nolisp
setlocal lispwords=
setlocal nolist
setlocal makeencoding=
setlocal makeprg=
setlocal matchpairs=(:),{:},[:],<:>
setlocal modeline
setlocal modifiable
setlocal nrformats=bin,octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=htmlcomplete#CompleteTags
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
set relativenumber
setlocal relativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=0
setlocal noshortname
setlocal signcolumn=auto
setlocal smartindent
setlocal softtabstop=-1
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'html'
setlocal syntax=html
endif
setlocal tabstop=2
setlocal tagcase=
setlocal tags=
setlocal termkey=
setlocal termsize=
setlocal textwidth=0
setlocal thesaurus=
setlocal undofile
setlocal undolevels=-123456
setlocal nowinfixheight
setlocal nowinfixwidth
set nowrap
setlocal wrap
setlocal wrapmargin=0
silent! normal! zE
let s:l = 12 - ((11 * winheight(0) + 37) / 74)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
12
normal! 05|
tabnext 1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxToOatI
set winminheight=1 winminwidth=1
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
