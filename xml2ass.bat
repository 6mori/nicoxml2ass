SET INPUT_DIR=%*
SET XML_SUFFIX=*.xml

for %%i in (%INPUT_DIR%%XML_SUFFIX%) do (
    SET INPUT_FILE="%%i"
    SETLOCAL ENABLEDELAYEDEXPANSION
    SET OUTPUT_FILE1=!INPUT_FILE:xml=ass!
    SET OUTPUT_FILE2=!INPUT_FILE:xml=ssa!
    if NOT exist !OUTPUT_FILE1! (
        if NOT exist !OUTPUT_FILE2! (
            python "xml2ass.py" !INPUT_FILE!
        ) else (
            echo !OUTPUT_FILE2! existed
        )
    ) else (
        echo !OUTPUT_FILE1! existed
    )
    ENDLOCAL
)
pause
