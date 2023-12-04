grammar SketchAnimateImperativeParadigm;

// Lexer Rules
ID     : [a-zA-Z] [a-zA-Z0-9]* ;     // Identifiers
INT    : [0-9]+ ;                    // Integer numbers
SEMI   : ';' ;                       // Semicolon
COMMA  : ',' ;                       // Comma
DOT    : '.' ;                       // Dot
WS     : [ \t\r\n]+ -> skip ;        // Whitespace to be ignored
STRING : '"' ( [a-zA-Z0-9 ] | '\t' )* '"';     // String literal, including spaces and tabs
BOOLEAN: 'true' | 'false';           // Boolean values
COLOR_HEX : '#' [0-9a-fA-F]{6} ;      // Hexadecimal color code
COLOR_RGBA : 'rgba(' [0-9]+ ',' [0-9]+ ',' [0-9]+ ',' [0-9]+ ')' ; // RGBA color code

// Parser Rules
program : statement+ ;

statement : groupDeclaration SEMI
          | animationStatement SEMI ;

groupDeclaration : 'createGroup' ID '(' idList ')' ;

idList : ID (COMMA ID)* ;            // List of identifiers

animationStatement : action '(' target (COMMA actionParameters)? ')' ;

target : ID ; // Target can be an individual ID or a group

action : 'moveTo' | 'rotate' | 'changeColor' | 'setVisible' | 'exportAsGif' | 'exportAsVideo' ;

actionParameters : moveToParams | rotateParams | colorParams | visibilityParams | exportParams ;



moveToParams : INT COMMA INT COMMA INT ; // x, y, duration
rotateParams : INT COMMA INT ;           // angle, duration
colorParams : STRING | COLOR_HEX | COLOR_RGBA ; // Color can be a string, hex, or rgba
visibilityParams : BOOLEAN ;             // true for visible, false for invisible
exportParams : STRING ;                  // file format
// Example :
// createGroup group1(circle1, rect1);
// moveTo(group1, 100, 100);
// resize(circle1, 50);