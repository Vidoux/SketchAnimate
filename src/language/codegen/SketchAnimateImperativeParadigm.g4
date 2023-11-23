grammar SketchAnimateImperativeParadigm;

// Lexer Rules
ID : [a-zA-Z] [a-zA-Z0-9]* ;         // Identifiers
INT    : [0-9]+ ;                    // Integer numbers
SEMI   : ';' ;                       // Semicolon
ASSIGN : '=' ;                       // Assignment
COMMA  : ',' ;                       // Comma
DOT    : '.' ;                       // Dot
WS     : [ \t\r\n]+ -> skip ;        // Whitespace to be ignored
IDList : ID (COMMA WS* ID)* ;            // List of identifiers


// Parser Rules
program : statement+ ;

statement : groupDeclaration SEMI
          | animationStatement SEMI ;


groupDeclaration : 'createGroup' ID '(' IDList ')' ;


groupID : ID ;


animationStatement : action '(' target (COMMA arguments)? ')' ;

target : ID | groupID ; // Target can be an individual ID or a group

action : 'moveTo' | 'resize' | 'changeColor' ; // Actions to manipulate objects or groups

arguments : INT (COMMA INT)* ; // Arguments for actions

// Example :
// createGroup group1(circle1, rect1);
// moveTo(group1, 100, 100);
// resize(circle1, 50);