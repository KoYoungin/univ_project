#include <stdlib.h> // malloc, atoi
#include <stdio.h>
#include <ctype.h> // isdigit
#include <assert.h> // assert

#define MAX_STACK_SIZE	50

////////////////////////////////////////////////////////////////////////////////
// LIST type definition
typedef struct node
{
	char		data;
	struct node	*left;
	struct node	*right;
} NODE;

typedef struct
{
	NODE	*root;
} TREE;

////////////////////////////////////////////////////////////////////////////////
// Prototype declarations

/* Allocates dynamic memory for a tree head node and returns its address to caller
	return	head node pointer
			NULL if overflow
*/
TREE *createTree( void);

/* Deletes all data in tree and recycles memory
*/
void destroyTree( TREE *pTree);

static void _destroy( NODE *root);

/*  Allocates dynamic memory for a node and returns its address to caller
	return	node pointer
			NULL if overflow
*/
static NODE *_makeNode( char ch);

/* converts postfix expression to binary tree
	return	1 success
			0 invalid postfix expression
*/
int postfix2tree( char *expr, TREE *pTree);

/* Print node in tree using inorder traversal
*/
void traverseTree( TREE *pTree);

/* internal traversal function
	an implementation of ALGORITHM 6-6
*/
static void _traverse( NODE *root);

/* Print tree using inorder right-to-left traversal
*/
void printTree( TREE *pTree);

/* internal traversal function
*/
static void _infix_print( NODE *root, int level);

/* evaluate postfix expression
	return	value of expression
*/
float evalPostfix( char *expr);

////////////////////////////////////////////////////////////////////////////////
void destroyTree( TREE *pTree)
{
	if (pTree)
	{
		_destroy( pTree->root);
	}
		
	free( pTree);
}

////////////////////////////////////////////////////////////////////////////////
void printTree( TREE *pTree)
{
	_infix_print(pTree->root, 0);
	
	return;
}

////////////////////////////////////////////////////////////////////////////////
void traverseTree( TREE *pTree)
{
	_traverse(pTree->root);
	
	return;
}

////////////////////////////////////////////////////////////////////////////////
int main( int argc, char **argv)
{
	TREE *tree;
	char expr[1024];
	
	fprintf( stdout, "\nInput an expression (postfix): ");
	
	while (fscanf( stdin, "%s", expr) == 1)
	{
		// creates a null tree
		tree = createTree();
		
		if (!tree)
		{
			printf( "Cannot create tree\n");
			return 100;
		}
		
		// postfix expression -> expression tree
		int ret = postfix2tree( expr, tree);
		if (!ret)
		{
			fprintf( stdout, "invalid expression!\n");
			destroyTree( tree);
			continue;
		}
		
		// expression tree -> infix expression
		fprintf( stdout, "\nInfix expression : ");
		traverseTree( tree);
		
		// print tree with right-to-left infix traversal
		fprintf( stdout, "\n\nTree representation:\n");
		printTree(tree);
		
		// evaluate postfix expression
		float val = evalPostfix( expr);
		fprintf( stdout, "\nValue = %f\n", val);
		
		// destroy tree
		destroyTree( tree);
		
		fprintf( stdout, "\nInput an expression (postfix): ");
	}
	return 0;
}
static NODE *_makeNode( char ch){
	NODE *node=(NODE *)malloc(sizeof(NODE));
	if(!node)	return NULL;
	node->data = ch;
	node->left = NULL;
	node->right = NULL;
	return node;
}
static void _destroy( NODE *root){
	if(root!=NULL){
		_destroy(root->left);
		_destroy(root->right);
		free(root);
	}
}
static void _traverse( NODE *root){
	if(root!=NULL){
		if(isdigit(root->data)){
			printf("%c",root->data);
		}
		else{
			printf("(");
			_traverse(root->left);
			printf("%c",root->data);
			_traverse(root->right);
			printf(")");
		}
	}
}
static void _infix_print( NODE *root, int level){
	if(root!=NULL){
		if(isdigit(root->data)){
			for(int i=0;i<level;i++)
				printf("\t");
			printf("%c\n",root->data);
		}
		else{
			_infix_print(root->right,level+1);
			for(int i=0;i<level;i++)
				printf("\t");
			printf("%c\n",root->data);
			_infix_print(root->left,level+1);
		}
	}
}
TREE *createTree( void ){
	TREE*tree=(TREE*)malloc(sizeof(TREE));
	if(!tree) NULL;
	tree->root = NULL;
	return tree;
}
int postfix2tree( char *expr, TREE *pTree){
	NODE *stack[MAX_STACK_SIZE];
	int i,j,top=0;
	NODE *node;
	for(i=0;expr[i];i++){
		node = _makeNode(expr[i]);
		stack[top] = node;
		if(isdigit(stack[top]->data)){
			top++;
		}
		else{
			top -= 2;
			if(top<0){
				_destroy(node);
				if(top==-1) _destroy(stack[0]);
				return 0;
			}
			node->left=stack[top];
			node->right=stack[top+1];
			if(expr[i]=='+'||expr[i]=='/'||expr[i]=='*'||expr[i]=='-'){
				stack[top]=node;
				top++;
				stack[top]=NULL;
			}
			else{
				_destroy(node);
				for(i=0;i<top;i++)
					_destroy(stack[i]);
				return 0;
			}
		}
	}
	if(top>1){
		for(i=0;i<top;i++)
			_destroy(stack[i]);
		return 0;
	}
	pTree->root=stack[top-1];
	
	return 1;
}
float evalPostfix( char *expr){
	int i,top=0;
	float cal,fstack[1024];
	for(i=0;expr[i];i++){
		
		if(isdigit(expr[i])){
			cal=expr[i]-'0';
			fstack[top]=cal;
			top++;
		}
		else if(expr[i]=='+'||expr[i]=='/'||expr[i]=='*'||expr[i]=='-'){	
			if(expr[i]=='+'){
				cal = fstack[top-2]+fstack[top-1];
			}
			else if(expr[i]=='-'){
				cal = fstack[top-2]-fstack[top-1];
			}
			else if(expr[i]=='*'){
				cal = fstack[top-2]*fstack[top-1];
			}
			else{	// if /
				cal = fstack[top-2]/fstack[top-1];
			}
			fstack[top-2]=cal;
			fstack[top-1]=0;
			top--;
		}
	}
	return fstack[0];
}











