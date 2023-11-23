grammar SketchAnimate;

// Lexer Rules
ID     : [a-zA-Z]+ ;                 // Identifiers
INT    : [0-9]+ ;                    // Integer numbers
SEMI   : ';' ;                       // Semicolon
ASSIGN : '=' ;                       // Assignment
COMMA  : ',' ;                       // Comma
DOT    : '.' ;                       // Dot
WS     : [ \t\r\n]+ -> skip ;        // Whitespace to be ignored

// Parser Rules
program : statement+ ;

statement : objectDeclaration SEMI
          | animationStatement SEMI ;

objectDeclaration : ID ASSIGN 'new' 'Object' '(' arguments ')' ;

arguments : INT (COMMA INT)* ; // Generic arguments, like position and size

animationStatement : ID DOT action '(' INT (COMMA INT)? ')' ;

action : 'moveTo' | 'resize' | 'changeColor' ; // Actions, applicable to any object

// Example of use:
// c = new Object(10, 20, 30);
// c.moveTo(100, 100);
// c.resize(50);
