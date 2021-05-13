#include "libs.h"
#include "globals.h"
#include "funcs.h"

// EXECUTE COMMANDS -------------------------------------------
void execCmd(char *strcopy, char **args){
    pid_t childPid;
    int status;
    int in_redirect = 0, out_redirect = 0, fd0, fd1;
    char *io_filenames[3];

    childPid = fork();

    if (childPid == -1) {
        perror("fork() failed!");
        fflush(stdout);
        statusCode = 1;
        return;
    // in the child process
    } else if (childPid == 0){
        struct sigaction default_action, ignore_action;
        //change sigint to DFL (kills fg) child processes---------------------------
        default_action.sa_handler = SIG_DFL;
        if(sigaction(SIGINT, &default_action, NULL) <0){
            printf("SigINT in child failed\n");
            fflush(stdout);
        }

        //keep sigtstp as IGN in child without msg--------------------------------
        ignore_action.sa_handler = SIG_IGN;
        if(sigaction(SIGTSTP, &ignore_action, NULL) <0){
            printf("SigTSTP in child failed\n");
            fflush(stdout);
        }

        // if redirect symbols detected, set flags and route
        if(strchr(strcopy, '<') && strchr(strcopy, '>')){
            in_redirect = 1;
            out_redirect = 1;
            redirect_io(io_filenames, args);

        } else if (strchr(strcopy, '<')){
            //REDIRECTING INPUT WITH NO FILE SPECIFIED NOT BEING CAUGHT: head <
            in_redirect = 1;
            redirect_input(io_filenames, args); 
        } else if (strchr(strcopy, '>')){
            out_redirect = 1;
            redirect_output(io_filenames, args);
        }

        //duplicate and reroute the io filenames to stdin/stdout
        if (in_redirect == 1){

            fd0 = open(io_filenames[0], O_RDONLY, 0);
            // write error in file instead of unable to open
            if (fd0 < 0){
                printf("Error--Can't open %s\n", io_filenames[0]);
                fflush(stdout);
                statusCode = 1;
                return;
            }
            dup2(fd0, STDIN_FILENO);
            close(fd0);
            // reset input redirection flag
            in_redirect = 0;
        }

        if (out_redirect == 1){
            fd1 = creat(io_filenames[1], 0644);
            if (fd1 < 0){
                printf("Error--Can't open %s\n", io_filenames[1]);
                fflush(stdout);
                statusCode = 1;
                return;
            }
            dup2(fd1, STDOUT_FILENO);
            close(fd1);
            //reset output redirect flag
            out_redirect = 0;
        }
        if (flag_bg == 1 && flag_tstp == 0){
            printf("Background process %d started\n", getpid());
            fflush(stdout);
        }

        //FINALLY EXECUTE COMMAND------------------------------
        execvp(args[0], args);
        printf("command not found\n");
        fflush(stdout);
        statusCode = 1;
        return;
        
    // in the parent bracket    
    } else {
        //if not a bg process or tstp flag is on, parent waits for child to finish
        if (flag_bg == 0 || flag_tstp == 1){
            // childPid = waitpid(childPid, &status, 0);
            waitpid(childPid, &status, 0);
        
            //if exited normally
            if (WIFEXITED(status)){
                // printf("Process %d terminated normally with status %d\n", childPid, WEXITSTATUS(status));
                // fflush(stdout);
                statusCode = WEXITSTATUS(status);
            // if terminated abnormally
            } else {
                // printf("Process %d finished abnormally due to signal %d\n", childPid, WTERMSIG(status));
                // fflush(stdout);
                statusCode = WTERMSIG(status);
            }
        }
    }
}