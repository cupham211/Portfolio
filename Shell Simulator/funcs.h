// file headers to hoist

//main 
void reset_flags();
void cwd();
void inputStr(char *str);
void check_bg(char *strcopy, char **args);
void handle_SIGINT(int sig);
void handle_SIGTSTP(int sig);

//builtins
int builtinCmd(char **args);

//processcmd
char* var_expansion(char *str);
void parse(char *str, char **args);

//execs
void execCmd(char *strcopy, char **args);

//redirects
void redirect_io(char **io_filenames, char **args);
void redirect_input(char **io_filenames, char **args);
void redirect_output(char **io_filenames, char **args);

