


# Format

- General
  - There are only two acceptable top-level components: functions and imports
  - That means: no global variables, no classes, etc
- Functions
  - Functions are standard Python functions, multi or single line (lambdas don't count)
- Imports
  - Imports can take the forms of `import MODULE` or `from MODULE import FUNCTION`
  - Aliases are not supported

Disclaimer: I'm trying to parse a non-regular language (Python) with regular expressions (finite automata can't handle infinitely nested components). As a result - this is very fragile and doesn't work for MANY cases.