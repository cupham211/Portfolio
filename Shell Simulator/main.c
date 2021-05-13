// Author: Christine Pham
// Date: 4/27/2021
// CS 344 - Operating Systems
// to run type: make
// next: chmod +x ./p3testscript (or test script)
// next: ./p3testscript 2>&1

#include "libs.h"
#include "funcs.h"

// Global variables
//initialize var for status command
int statusCode = 0;
int flag_bg = 0;
int flag_builtin = 0;
volatile sig_atomic_t flag_tstp = 0;

// RESET GLOBAL FLAGS 4 new commands-----------------
void reset_flags(){
    flag_bg = 0;
    flag_builtin = 0;
}

// Print cwd ----------------------------------------
void cwd() {
    char cwd[MAXLINE];
    getcwd(cwd, sizeof(cwd));
    printf("current working directory is: %s\n", cwd);
    fflush(stdout);
}

// INPUT ARGUMENTS------------------------------------
void inputStr(char *str){
    // command prompt loops until a non-empty string with no #
    do {
        printf("\n: ");
        fflush(stdout);
        fgets(str, MAXLINE, stdin);
    } while (str[0] == '\n' || strncmp(str,"#", 1) == 0);
}

// CHECK BG CMD---------------------------------------
void check_bg(char *strcopy, char **args){
    if (strchr(strcopy, '<') || strchr(strcopy, '>')){
        if (strchr(strcopy, '&')){
            flag_bg = 1;
            return;
        }
    }

    int i = 0;
    while(args[i]){
        if(strcmp(args[i], "&") == 0){
            flag_bg = 1;
            args[i] = NULL;
        }
        i++;
    }
}

// HANDLER FOR SIGINT---------------------------------
void handle_SIGINT(int sig){
    char *msg = "Terminated by signal 2\n";
    write(STDOUT_FILENO, msg, 22);
}

// HANDLER FOR SIGTSTP----------------------
void handle_SIGTSTP(int sig){

    if (flag_tstp == 0){
        char *on = "Entering foreground-only mode (& is now ignored)\n";
        flag_tstp = 1;
        write(STDOUT_FILENO, on, 49);
    } else {
        char *off = "Exiting foreground-only mode\n";
        flag_tstp = 0;
        write(STDOUT_FILENO, off, 29);
    }
}

// MAIN ----------------------------------------------
int main(void){
    // init arrays to store commands
    char str[MAXLINE], *args[MAXARG];
    // vars for zombie children
    pid_t zombiePid;
    int zombieStatus;

    // ***init the signal handlers***----------------------
    struct sigaction SIGINT_action, SIGTSTP_action;

    // introduce program and print cwd-----------------------------------------------------
    printf("Smallsh Program\n\n");
    fflush(stdout);
    cwd();

    while (1){
        //-------******SIGINT STRUCT INIT******-------------------------------
        // ignore sigint in parent process
        SIGINT_action.sa_handler = handle_SIGINT;
        // block all catchable signals while in the handler
        sigfillset(&SIGINT_action.sa_mask);
        // no flags set
        SIGINT_action.sa_flags = 0;
        if(sigaction(SIGINT, &SIGINT_action, NULL) < 0){
        printf("SigTSTP parent failed\n");
        fflush(stdout);
        }
        //-------****SIGTSTP STRUCT INIT*****---------------------------------
        SIGTSTP_action.sa_handler = handle_SIGTSTP;
        // block all catchable signals while in the handler
        sigfillset(&SIGTSTP_action.sa_mask);

        // no flags set
        SIGTSTP_action.sa_flags = 0;
        sigaction(SIGTSTP, &SIGTSTP_action, NULL);

        // child signal handler-------------------------------------------
        while((zombiePid = waitpid(-1, &zombieStatus, WNOHANG)) > 0){
            if (flag_tstp == 0){
                printf("Background process %d terminated with exit value %d\n", zombiePid, WEXITSTATUS(zombieStatus));
                fflush(stdout);
            } else { statusCode = WEXITSTATUS(zombieStatus); }
        }
        char *cmd = NULL;
        // get command string from user------
        inputStr(str);
        // expand variables------------
        cmd = var_expansion(str);
        //create copy of command line arg string
        char strcopy[MAXLINE];
        strcpy(strcopy, cmd);
        // tokenize string into arguments--------
        parse(cmd, args);
        // check if cmd is a BuiltIn command
        flag_builtin = builtinCmd(args);
        if (flag_builtin == 0){
            // check if cmd is a background process
            check_bg(strcopy, args);
            // check sigtstp flag-------------------------------------------
            execCmd(strcopy, args);
        }
        //reset flags for background and builtin
        reset_flags();
        free(cmd);
    }
    return 0;
}