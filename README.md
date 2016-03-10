This is a basic Unicode category library. Run `./maketables.py` to generate
code that will test whether a character is in a particular Unicode category.

Currently the only supported language is C++.

# Language code

The following sections describe the code generated for each supported language.

## C++

The generated code is in a file called unicat.h. You should copy this into
your source distribution and use how you like.

The categories are in the namespace `unicat::categories`, and have the same
name as the corresponding Unicode category. To test whether a `char32_t` is
in a category, use the function `unicat::is`.

For example:

    unicat::is(c, unicat::categories::Ss);

# Extending to other languages

The languages specific code is generated using Jinja templates. Contributions
for other languages are welcome.
