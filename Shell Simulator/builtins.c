#include "libs.h"
#include "globals.h"
#include "funcs.h"

// BUILTIN COMMANDS -------------------------------------------
int builtinCmd(char **args){
    int i, switchargs = 0;
    char *listCmds[3] = {"exit", "cd", "status"};

    // create switch-case num based on matching args
    for (i=0; i<3; i++){
        if (strcmp(args[0], listCmds[i]) == 0){
            switchargs = i + 1;
            break;
        }
    }

    switch(switchargs){
        case 1:
            //politely terminates all processes before exiting
            kill(0, SIGTERM);
            exit(0);
        case 2:
            // if no args included with cd, start at HOME path value
            if (args[1] == NULL){
                char *dir = getenv("HOME");
                chdir(dir);
            // exec chdir on args[1]--display error if no matches
            } else if(chdir(args[1]) < 0){
                printf(": cd %s: No such file or directory\n", args[1]);
                fflush(stdout);
                return 0;
            }
            return 1;
        case 3:
            // print status returned by last fg process if not builtin
            printf("exit value %d\n", statusCode);
            fflush(stdout);
            return 1;
        default:
            break;
    }
    //return 0 if not a built in
    return 0;
}