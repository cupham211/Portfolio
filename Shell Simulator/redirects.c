#include "libs.h"
#include "globals.h"
#include "funcs.h"

// REDIRECT INPUT and OUTPUT------------------------------------
void redirect_io(char **io_filenames, char **args){
    int i=0;
    while(args[i] != NULL){
        //change redirect symbols to NULL
        if (strcmp(args[i], "<") == 0){
            args[i] = NULL;
            //if no filename/patch specified, reroute to /dev/null
            if (strcmp(args[i+1], ">") == 0){
                i++;
            } else if(args[i+1]){
                io_filenames[0] = args[i+1];
                //NULL out filename
                args[i+1] = NULL;
                // i++ to get to a char without exiting in next loop
                i++;
                i++;
            }
        }

        if(strcmp(args[i], ">") == 0){
            args[i] = NULL;
            //if no output file specified and not bg
            if (!args[i+1]){
                printf("Error--no file/directory specified\n");
                fflush(stdout);
                continue;
            }
            //if only & is next it means its a bg cmd and filename not specified
            if (strcmp(args[i+1], "&") ==0 && !io_filenames[0]){
                io_filenames[0] = "/dev/null";
                io_filenames[1] = "/dev/null";
            } else if (strcmp(args[i+1], "&") == 0){
                io_filenames[1] = "/dev/null";
                args[i+1] = NULL;
            } else if(args[i+1]){
                io_filenames[1] = args[i+1];
                args[i+1] = NULL;
            }
        }
        i++;
    }
}

// REDIRECT INPUT--------------------------------------------------------
void redirect_input(char **io_filenames, char **args){
    int i=0;
    while(args[i]){
        if(strcmp(args[i], "<") == 0){
            args[i] = NULL;
            if (!args[i+1]){
                printf("Error--no file/directory specified\n");
                fflush(stdout);
            } else if (strcmp(args[i+1], "&") == 0){
                io_filenames[0] = "/dev/null";
                args[i+1] = NULL;
            } else if (args[i+1]){
                io_filenames[0] = args[i+1];
                args[i+1] = NULL;
            }
        }
        i++;
    }
}

// REDIRECT OUTPUT-------------------------------------------------------
void redirect_output(char **io_filenames, char **args){
    int i =0;
    while(args[i] != NULL){
        if (strcmp(args[i], ">") == 0){
            args[i] = NULL;
            if (!args[i+1]){
                printf("Error--no file/directory specified\n");
                fflush(stdout);
            } else if(strcmp(args[i+1], "&")==0){
                io_filenames[1] = "/dev/null";
            } else if (args[i+1]){
                io_filenames[1] = args[i+1];
                args[i+1] = NULL;
            }
        }
        i++;
    }
}