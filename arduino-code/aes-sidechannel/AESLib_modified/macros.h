// logical constants
#define TRUE  1
#define FALSE 0

// bit macros
#define sbi(x,y) 		x|=(1<<y)
#define cbi(x,y) 		x&=~(1<<y)
#define tbi(x,y) 		x^=(1<<y)
#define isHigh(x,y)		((x&(1<<y))==(1<<y)) ? 1:0
#define isLow(x,y)		((x&(1<<y))==0) ? 1:0


// modulus macro
#define MOD(x)  		((x)>=0?x:-(x))
#define SIGN(x)			((x)>=0?1:-1)

// min max macros
#define MIN2(a,b)     	((a<=b)?a:b)
#define MIN4(a,b,c,d) 	(MIN2(MIN2(a,b),MIN2(c,d)))
#define MAX2(a,b)     	((a>=b)?a:b)
#define MAX4(a,b,c,d) 	(MAX2(MAX2(a,b),MAX2(c,d)))

// positive value
#define pos(x)			(x>0?x:0)


#define assign16bit(x,y)	{cli();x=y;sei();}