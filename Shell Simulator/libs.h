#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <signal.h>
#include <fcntl.h>
#include <sys/types.h>
#include <errno.h> //maybe
#include <math.h>

#define MAXLINE 2048
#define MAXARG 512 