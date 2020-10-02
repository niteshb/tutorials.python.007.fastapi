@echo off
if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==xtransfer GOTO label_transfer_start

REM '1st call' mode
set VY_ALIAS_BATCH_GEN_NO_DEBUG=y
if NOT x%1==xdebug GOTO label_start

REM 'debug' mode
echo Debug mode on
set VY_ALIAS_BATCH_GEN_NO_DEBUG=transfer
%0 %2 %3 %4 %5 %6 %7 %8 %9
GOTO label_exit

REM 'transfer' mode. Here we debug by setting VY_ALIAS_BATCH_GEN_NO_DEBUG=<blank>
:label_transfer_start
echo Tranferred into batchfile sub call
set VY_ALIAS_BATCH_GEN_NO_DEBUG=
if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==x echo arguments    :: (0, '%0') (1, '%1') (2, '%2') (3, '%3') (4, '%4') (5, '%5') (6, '%6') (7, '%7') (8, '%8') (9, '%9')
if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==x echo command line :: %0 %1 %2 %3 %4 %5 %6 %7 %8 %9
echo ##############################################################
GOTO label_start

##############################################################
REM Actual start of the program
:label_start

:label_Switcher
if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==x echo label_Switcher & REM (Switcher) <- (help)
if x%1==xh         GOTO label_help
if x%1==x          GOTO label_help
if x%1==x-h        GOTO label_help
if x%1==x--help    GOTO label_help
if x%1==xmain      GOTO label_main
if x%1==xhw        GOTO label_hello_world
if x%1==xmake      GOTO label_make
GOTO label_invalid & REM (Switcher) <- (make)
:label_main
if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==x echo label_main & REM (main) <- (main_run_server)
if x%2==xrun       GOTO label_main_run_server
GOTO label_invalid & REM (main) <- (main_run_server)
:label_hello_world
if x%VY_ALIAS_BATCH_GEN_NO_DEBUG%==x echo label_hello_world & REM (hello_world) <- (hello_world_run_server)
if x%2==xrun       GOTO label_hello_world_run_server
GOTO label_invalid & REM (hello_world) <- (hello_world_run_server)

##############################################################
:label_invalid
echo Invalid command. Type '%0 h' to get help
GOTO label_exit

##############################################################
:label_help
@echo on
@echo Command Options:
@echo   make h        : This help message
@echo   make main run   : uvicorn main:app --reload
@echo   make hw run   : uvicorn helloWorld:app --reload
@echo   make make     : python P:\@common\python\vyAliasBatchScriptGenerator\tests\main.py make.vyalias
@echo.
@echo off
GOTO label_exit

##############################################################
:label_main_run_server
@echo on
uvicorn main:app --reload
@echo off
GOTO label_exit

##############################################################
:label_hello_world_run_server
@echo on
uvicorn helloWorld:app --reload
@echo off
GOTO label_exit

##############################################################
:label_make
@echo on
python P:\@common\python\vyAliasBatchScriptGenerator\tests\main.py make.vyalias
@echo off
GOTO label_exit

##############################################################
:label_exit