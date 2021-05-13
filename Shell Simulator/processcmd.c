#include "libs.h"
#include "globals.h"
#include "funcs.h"

// VARIABLE EXPANSION---------------------------
char* var_expansion(char *str){

  char *substr = "$$";
  int i, count = 0;
  int pid = getpid();
  // make room to hold pid and transfer it over
  char *curPid = malloc(sizeof(char)*log10(pid));
  sprintf(curPid, "%d", pid);

  int pid_size = strlen(curPid);
  int substr_size = strlen(substr);
  
  // Count number of times $$ occur in the string
    for (i = 0; str[i] != '\0'; i++) {
        if (strstr(&str[i], substr) == &str[i]) {
            count++;
  
            // Jumping to index after the old word.
            i += substr_size - 1;
        }
    }
  // make a string big enough to store expanded cmd
  char *expanded = (char*)malloc(i + count * (pid_size - substr_size) + 1);
    i = 0;
    while (*str) {
        // compare the substring with the result
        if (strstr(str, substr) == str) {
            strcpy(&expanded[i], curPid);
            i += pid_size;
            str += substr_size;
        }
        else
            expanded[i++] = *str++;
    }
  
    expanded[i] = '\0';

    free(curPid);
    return expanded;
  
}

// PARSE ARGUMENTS --------------------------------
void parse(char *str, char **args){
    int i = 0;
    //separate string by spaces and new line
    args[i] = strtok(str, " \n");
    //populate args and put NULL after last processed token
    while(args[i] != NULL) {
        args[++i] = strtok(NULL, " \n");
    }
}