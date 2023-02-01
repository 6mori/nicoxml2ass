SET INPUT_DIR=%*
SET XML_SUFFIX=*.xml
SET JSON_SUFFIX=*.json

for %%i in (%INPUT_DIR%%JSON_SUFFIX%) do (
    SET INPUT_FILE="%%i"
    SETLOCAL ENABLEDELAYEDEXPANSION
    SET OUTPUT_FILE=!INPUT_FILE:json=xml!
    echo !OUTPUT_FILE!
    if NOT exist !OUTPUT_FILE1! (
        python "convert_chat_to_xml.py" !INPUT_FILE!
        python "xml2ass.py" !OUTPUT_FILE!
    ) else (
        echo !OUTPUT_FILE! existed
    )
    ENDLOCAL
)

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
