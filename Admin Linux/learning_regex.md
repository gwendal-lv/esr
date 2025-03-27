# Regular Expressions

First of all, this will be a bit painful but as with `vim` once you overcome the initial learning curve you start to see the potential regular expressions bring to the table.
To make matters even worse, there are multiple *flavors* of regexes.
An overview and comparison between different flavors can be found on [wikipedia](https://en.wikipedia.org/wiki/Comparison_of_regular-expression_engines).
Don't see this as a reason *not* to learn some basic expressions though, a little experience goes a long way.

## What are they?

> A regular expression (shortened as regex or regexp;[1] also referred to as rational expression[2][3]) is a sequence of characters that specifies a search pattern. Usually such patterns are used by string-searching algorithms for "find" or "find and replace" operations on strings, or for input validation. It is a technique developed in theoretical computer science and formal language theory.

[wikipedia](https://en.wikipedia.org/wiki/Regular_expression)

You can see regular expressions as find (and replace) on steroids.
As a practical example, I used *a lot* of regular expressions to clean up the multiple choice LPI questionnaires.
This was done in `vim` so I used the vim flavor regex but it's not too much different from the main one you should know, `grep`.

From a practical system administer point of view you'll probably use regexes in this order:

1. with `grep`
2. with `sed` (went copy pasting commands found online)
3. with `vim`
4. with a scripting language such as `python3`

## How to learn them?

Some tips and pointers before we head into the actual syntax.

### Vim

There is a setting in `vim` that is disabled by default but highly advised to learn vim regexes.
By setting `set incsearch` in your `~/.vimrc` or in the **expert** command line vim will highlight whatever matches the pattern you're searching for.
This can be a tremendous help when building complex patterns.

### Grep

By default `grep` only interprets basic regular expressions.
If you want, or more likely *need* to use [extended](https://www.gnu.org/software/grep/manual/html_node/Basic-vs-Extended.html) expressions you should use `grep -E` or `egrep` instead.
For completeness's sake I should mention there is a third *version* of `grep` invoke with `grep -P` that interprets the patterns as [perl regex](https://perldoc.perl.org/perlre).
One of the advantages of perl regexes is reverse matching.

## The basics

### Fundamental structure and anchoring

Download the following [file](./assets/regex_03.txt) which is an American English dictionary we will use to test out some basic patterns.
Fire up a terminal and find all words that contain the string `abba`.
You already know how to do this with `grep`, nothing really special here.
`grep 'abba' regex_03.txt` should give give you a list containing 16 words.
Notice the color output in you terminal.

What if we only want the words containing `abba` but who *also* start with `s`?
This can be done with the following line `grep 's.*abba' regex_03.txt`.
You should have 6 matches left.
How about the same ones, but they have to end with an `s`?
You guessed it, `grep 's.*abba.*s' regex_03.txt`, get's the job done.

Now, what are those special characters?
They are *like* [wildcards in bash](https://ryanstutorials.net/linuxtutorial/wildcards.php) but on steroids.
In the example above, the `.` represents almost any character, and the `*` means as **many** times as we want.
They are both very powerful, and broad, matching patterns that are part of the [fundamental structure](https://www.gnu.org/software/grep/manual/html_node/Fundamental-Structure.html#Fundamental-Structure) of regex.
They work well but sometime we need to be a bit more precise, which we'll get to in a bit.

Second little example with the same list.
What if we want all words with the letter `a` in them?
Easy, `grep 'a' regex_03.txt` should do the trick but 52849 results are a bit much.
Let's trim it back to only the words having `aa` in them?
`grep 'aa' regex_03.txt` brings it down to 65 matches.
Nice.
Now, how about only the ones that *start* with `aa`?
This can be done with an other core concept of regex called [anchoring](https://www.gnu.org/software/grep/manual/html_node/Anchoring.html#Anchoring) and can be done as such `grep '^aa' regex_03.txt`.
Here the `^` signifies the **start** of the line.
Last one, I promise, what if we want of those three only the ones with `s` at the end?
Right, `grep '^aa.*s$' regex_03.txt` should do the trick where `$` means **ends** with.

### Character classes and bracket expansion

Let's find, in the following [file](./assets/regex_04.txt) all words starting with a capital case letter.
This can be done in multiple ways.
First we try one you *should* remember from your bandit days.
Does `[a-zA-Z]` ring a bell?
You used it to do ROT13 rotation somewhere around level 12.
`grep '^[A-Z].*' regex_04.txt` greps out all words starting with a capital.
Wonderful, but a bit too many words.

Let's limit it to only words that have punctuation in them.
This, `grep '^[A-Z][[:alnum:]]*[[:punct:]].*' regex_04.txt`, which is *very* cryptic does the job.

Let's break it down a bit:

* `^[A-Z]` matches all capital letters
* `[[:alnum:]]*` all letters and number, as many times as we want
* `[[:punct:]]` matches any punctuation, but just **once**
* `.*` matches almost any character as many times as we want

In the above pattern you see *two* different forms of character classes, the `[A-Z]` and the `[[:alnum:]]`.
Worth noting is that you can negate an expansion by putting a `^` inside it as such `grep '^[^A-Z].*' regex_03.txt` (note I used the first list because the animals list has no words starting with a capital letter).
This is basically the same as `grep '^[a-z].*' regex_03.txt`.

### The backslash character and special expressions

If we want to match only animals that contain multiple words we can use [special expressions](https://www.gnu.org/software/grep/manual/html_node/The-Backslash-Character-and-Special-Expressions.html#The-Backslash-Character-and-Special-Expressions).
Have a look at the output of this grep pattern `grep '\s[[:alpha:]]*' regex_04.txt`.
Here we notice we can select only parts of the lines too!
A handy flag we can add to the `grep` command is `-o` which will only print the part that matches (in red).

If we only want single words coming out of the search we can do this like so `grep -o '\s[a-zA-Z]*\>' regex_04.txt`.
Notice how it starts with an empty space?
let's break this one down.

* `\s` matches whitespace
* `[a-zA-Z]*` matches the entire alphabet as many times as we want
* `\>` matches the end of the word (not really needed here)

## Beyond basic

The tests done above are a quick introduction to what regex are and how to read them.
To master them there are only two things you need to do.

1. use them
2. google 

There is just no other way to wrap your head around it.
You should see it as a puzzle you're trying to solve.
To get you started I urge you to go to [this](http://regextutorials.com/) website and start the **introduction to regex** section.
It highlights automatically what your pattern is doing.
Once you completed the introduction you should try their exercises and the ones I made for you below.
You can fine very good cheat sheets online, like [this](https://cheatography.com/davechild/cheat-sheets/regular-expressions/) one, so have a look around.

## Exercises

Below are some practical exercises and files to go with them.
Use them to test out you grepping skills and as inspiration for personal challenges.
I've tested all of the challenges myself but there are a lot of different ways to get the same result with a different regex.

* configuration [file](./assets/sysctl.conf)
	* print only lines with actual configuration settings (ignore comments and empty lines)
* css [file](./assets/teddit.css)
	* extract all the hex color codes
* html [file](./assets/teddit.html)
	* html extract pictures
		* just jpg
		* jpg and png at the same time
* log [file](./assets/auth.log)
	* extract all IP addresses
		* plus only the unique ones
	* extract all wrong logins for known users
	* extract all unknown users (this is tricky and requires backwards searching using `grep -P`)
	* extract all the dates and times for successful logins (might require multiple greps in a pipe)
* mail dump [file](./assets/dump.mail)
	* extract all unique email addresses
	* extract all web links
		* only the base link (https://www.example.co.uk)
		* both http and https links

## Extra challenges

Regex patterns on their own are nice but can get a bit boring.
Try to integrate them into script to discover their true power.
An example would be to take the IP addresses from the [auth.log](./assets/auth.log) file and do a region discovery on them.
You can save all the country codes to a file and do an analysis on them to see where all the attacks are coming from.
