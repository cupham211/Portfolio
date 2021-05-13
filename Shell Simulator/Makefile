# Makefile for smallsh

all:
	gcc -Wall -g3 --std=gnu99 main.c redirects.c execs.c processcmd.c -lm builtins.c -o smallsh
exec:
	./smallsh
clean:
	rm -rf smallsh smallish.dSYM