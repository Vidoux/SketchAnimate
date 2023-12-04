grammar SketchAnimateImperativeParadigm;

// Lexer Rules
ID     : [a-zA-Z] [a-zA-Z0-9]* ;     // Identifiers
INT    : [0-9]+ ;                    // Integer numbers
SEMI   : ';' ;                       // Semicolon
ASSIGN : '=' ;                       // Assignment
COMMA  : ',' ;                       // Comma
DOT    : '.' ;                       // Dot
WS     : [ \t\r\n]+ -> skip ;        // Whitespace to be ignored

// Parser Rules
program : statement+ ;

statement : groupDeclaration SEMI
          | animationStatement SEMI ;

groupDeclaration : 'createGroup' ID '(' idList ')' ;

idList : ID (COMMA ID)* ;            // List of identifiers

animationStatement : action '(' target (COMMA arguments)? ')' ;

target : ID ; // Target can be an individual ID

action : 'moveTo' | 'resize' | 'changeColor' ; // Actions to manipulate objects

arguments : INT (COMMA INT)* ; // Arguments for actions

// Example :
// createGroup group1(circle1, rect1);
// moveTo(group1, 100, 100);
// resize(circle1, 50);
