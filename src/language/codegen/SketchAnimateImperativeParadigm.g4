grammar SketchAnimateImperativeParadigm;

// Lexer Rules
ID       : [a-zA-Z] [a-zA-Z0-9]* ;     // Identifiers
INT      : [0-9]+ ;                    // Integer numbers
SEMI     : ';' ;                       // Semicolon
COMMA    : ',' ;                       // Comma
DOT      : '.' ;                       // Dot
WS       : [ \t\r\n]+ -> skip ;        // Whitespace to be ignored
STRING   : '"' .*? '"';                // String literal for all quoted content
BOOLEAN  : 'true' | 'false';           // Boolean values

// Parser Rules
program : statement+ ;

statement : groupDeclaration SEMI
          | animationStatement SEMI ;

groupDeclaration : 'createGroup' ID '(' idList ')' ;

idList : ID (COMMA ID)* ;              // List of identifiers

animationStatement : action '(' target COMMA actionParameters ')' ;

target : ID ;                          // Target can be an individual ID or a group

action : 'moveTo' | 'rotate' | 'changeColor' | 'setVisible' | 'exportAsGif' | 'exportAsVideo' | 'resize';

parameter : INT | STRING | BOOLEAN ;   // Parameters can be integers, strings, or booleans

actionParameters : parameter (COMMA parameter)* ;

// Examples:
// moveTo(svg1, 100, 100);
// resize(svg1, 50);
