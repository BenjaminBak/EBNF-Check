# EBNF-Check

Our project "EBNF-Check" functions as a parser for a formal grammar.
It is able to examine whether a word can be derived from a given grammar written in the EBNF or not.
It also checks your grammar input for potential syntax errors.

## Installing / Getting started

To get started: 
- download the files main.py and txtfile.txt 
- put them in one folder 
- then open the txtfile.txt, copypaste or write your formal grammar onto the file
- then execute the main.py file.

Now a console should open. After checking your grammar, the console will ask you for the word you want to check.
Based on your Grammar it will determine if the word can be derived from the grammar or not.
The program loop allows you to check multiple Words. To Use a different Grammar, change the txtfile.txt file and restart the program.

## Features

* check the formal grammar for errors
* examine a word


## Planned Features:

* you can choose between using the EBNF or the standard BNF and the program will work with both
* ability to use quotations marks as a content

## Configuration

- you can use a line as a comment by putting "#" as the first character (then the parser will ignore the line)
- at the moment you should not use quotation marks as the content of a terminal e.g. "He says: "I like school"" would brake the program, instead you could use "He says: 'I like school'"
- when defining a non-terminal you should only use the following characters: 0-9, a-z, A-Z, - and _
- you can define a non-terminal only once in your grammar
- be aware that the derivation of multiple non-terminals in one line is currently not possible (e.g. word, number = "Hello", "1"; would lead to an error)
- be aware that at the moment the usage of special sequences (?...?) and exceptions (-) is not possible

## Example for an input (EBNF)


`example = word, number, character, ["."];`
`word = ("Hello", word) | "Hello";`
`number = "1", {"1"};`
`character = "!" | "," | "?";`



## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.


