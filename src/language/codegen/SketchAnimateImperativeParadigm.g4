grammar SketchAnimateImperativeParadigm;

// Lexer Rules
// Basic tokens
ID        : [a-zA-Z] [a-zA-Z0-9]* ;     // Identifiers
INT       : [0-9]+ ;                    // Integer numbers
FLOAT     : [0-9]+'.'[0-9]+ ;           // Float values
STRING    : '"' .*? '"';                // String literal for all quoted content
BOOLEAN   : 'true' | 'false';           // Boolean values

// Punctuation and Whitespace
SEMI      : ';' ;                       // Semicolon
COMMA     : ',' ;                       // Comma
DOT       : '.' ;                       // Dot
WS        : [ \t\r\n]+ -> skip ;        // Whitespace to be ignored

// Comments
LINE_COMMENT  : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;

// Parser Rules
program : mainBlock sequence* ;

mainBlock : 'main' '{' statement* '}' ;

// Sequences and invocations
sequence          : 'sequence' ID '(' parameterList? ')' '{' statement* '}' ;
sequenceInvocation: ID '(' argumentList? ')' ;

parameterList : parameter (COMMA parameter)* ;
parameter     : ID ;
argumentList  : expression (COMMA expression)* ;

// Statements
statement : groupDeclaration SEMI
          | animationStatement SEMI
          | sequenceInvocation SEMI
          | loadSVGStatement SEMI
          | exportAnimationStatement SEMI
          | delayStatement SEMI; // Add delayStatement to the list of statements

// SVG related
loadSVGStatement : 'loadSVG' '(' STRING ')' ;

// Exporting animations
exportAnimationStatement : 'exportAnimation' '(' exportParams ')' ;
exportParams : formatParam (COMMA additionalParam)* ;
formatParam  : 'gif' | 'mp4' | 'images' ;
additionalParam : STRING ;

// Group declarations
groupDeclaration : 'createGroup' ID '(' idList ')' ;
idList : ID (COMMA ID)* ;

// Animation statements
animationStatement : action '(' target COMMA startTime COMMA duration COMMA actionParameters? ')' ;
actionParameters   : moveToParams | rotateParams | colorParams | visibilityParams | exportParams ;

// Animation actions
action : 'moveTo'
       | 'rotate'
       | 'changeColor'
       | 'setVisible'
       | 'exportAsGif'
       | 'exportAsVideo'
       ;

// Time related parameters
startTime : expression ; // start time for animation (in ms)
duration  : expression ; // animation duration (in ms)
delayStatement : 'delay' '(' expression ')' ; // Introduces a waiting delay

// Specific action parameters
moveToParams : expression COMMA expression ; // x, y
rotateParams : expression ;             // angle
colorParams  : expression ;           // TODO: add color type
visibilityParams : expression ;       // true for visible, false for invisible

// Expressions
expression : ID | literal ;
literal    : INT | FLOAT | STRING | BOOLEAN ;


// Targets
target : ID ; // Target can be an individual ID or a group
