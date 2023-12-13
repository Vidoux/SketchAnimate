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
FLOAT     : [0-9]+'.'[0-9]+ ;          // Float values
LINE_COMMENT : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;


// Parser Rules
program : mainBlock sequence* ;

mainBlock : 'main' '{' statement* '}' ;

sequence : 'sequence' ID '(' parameterList? ')' '{' statement* '}' ;

parameterList : parameter (COMMA parameter)* ;
parameter : ID ;

statement : groupDeclaration SEMI
          | animationStatement SEMI
          | sequenceInvocation SEMI
          | loadSVGStatement SEMI
          | exportAnimationStatement SEMI;

loadSVGStatement : 'loadSVG' '(' STRING ')' ;
exportAnimationStatement : 'exportAnimation' '(' exportParams ')' ;
exportParams : formatParam (COMMA additionalParam)* ;
formatParam : 'gif' | 'mp4' | 'images' ;
additionalParam : STRING ;

groupDeclaration : 'createGroup' ID '(' idList ')' ;

idList : ID (COMMA ID)* ;              // List of identifiers

animationStatement : action '(' target (COMMA actionParameters)? ')' ;

sequenceInvocation : ID '(' argumentList? ')' ;

argumentList : expression (COMMA expression)* ;
expression : ID | literal ;
literal : INT | FLOAT | STRING | BOOLEAN ;

target : ID ;                          // Target can be an individual ID or a group

action : 'moveTo' | 'rotate' | 'changeColor' | 'setVisible' | 'exportAsGif' | 'exportAsVideo' ;

actionParameters : moveToParams | rotateParams | colorParams | visibilityParams | exportParams ;

moveToParams : expression COMMA expression COMMA expression ; // x, y, duration
rotateParams : expression COMMA expression ;           // angle, duration
colorParams : expression ;    //TODO ajout type                // Color as a string (could be text, hex, or rgba)
visibilityParams : expression ;             // true for visible, false for invisible

// Example :
// main {
//   createGroup group1(circle1, rect1);
//   sequenceAnimate(group1);
// }
//
// sequence sequenceAnimate(group) {
//   moveTo(group, 100, 100, 500);
//   changeColor(circle1, '"red"');
// }
