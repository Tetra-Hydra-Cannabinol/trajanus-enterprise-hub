# Research Finding #68

**Date:** 2025-12-17 08:57
**Topic:** Python stdout parsing Electron reliable
**Score:** 0.22086334

---

## Parsing a stdout in Python - Stack Overflow

**URL:** https://stackoverflow.com/questions/2101426/parsing-a-stdout-in-python
**Published:** Unknown date

---

## Content

If you are on \nix, I would recommend you to use commands module.

`import commands
status, res = commands.getstatusoutput("wget --version | grep Wget")
print status # Should be zero in case of of success, otherwise would have an error code
print res # Contains stdout`
sharjeel's user avatar

## 1 Comment

Add a comment

`subprocess`

## Your Answer

Thanks for contributing an answer to Stack Overflow!

But avoid …

To learn more, see our tips on writing great answers.

### Sign up or log in [...] Stack Internal

Knowledge at work

Bring the best of human thought and AI automation together at your work.

# Parsing a stdout in Python

In Python I need to get the version of an external binary I need to call in my script.

Let's say that I want to use Wget in Python and I want to know its version.

I will call

`os.system( "wget --version | grep Wget" )`

and then I will parse the outputted string.

How to redirect the stdout of the os.command in a string in Python? [...] Use the `subprocess` module:

`subprocess`
`from subprocess import Popen, PIPE
p1 = Popen(["wget", "--version"], stdout=PIPE)
p2 = Popen(["grep", "Wget"], stdin=p1.stdout, stdout=PIPE)
output = p2.communicate()`
Pär Wieslander's user avatar

## Comments

Add a comment

Use `subprocess` instead.

`subprocess`
Ignacio Vazquez-Abrams's user avatar

## 3 Comments

Add a comment

`Subprocess.popen`

`pipe()`
`subproces.popen()`
`os.pipe()`
`subprocess.popen()`
`C`
`popen()`

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
