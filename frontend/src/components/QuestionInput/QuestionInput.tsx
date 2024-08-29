import { useState, useEffect } from "react";
import { Stack, TextField } from "@fluentui/react";
import { Send28Filled } from "@fluentui/react-icons";
import { ClearChatButton } from "../ClearChatButton/ClearChatButton";
import styles from "./QuestionInput.module.css";
import { useRecoilState } from "recoil";
import { selectedMessageAtom } from "../UserChatMessage/Atom";
import Tooltip from "@mui/material/Tooltip";

interface Props {
    onSend: (question: string) => void;
    disabled: boolean;
    placeholder?: string;
    clearOnSend?: boolean;
    clearchat: () => void;
    isLoading: boolean;
    lastQuestionRef: any;
    fileuploadelement: any;
    value: string;
    isContent: boolean;
    // stopAnswerGeneration: () => void;
}

export const QuestionInput = ({ onSend, disabled, placeholder, clearOnSend, lastQuestionRef, clearchat, fileuploadelement }: Props) => {
    const [question, setQuestion] = useState<string>("");

    const [selectedMessage, setSelectedMessage] = useRecoilState(selectedMessageAtom);

    useEffect(() => {
        if (selectedMessage) {
            setQuestion(selectedMessage);
        }
    }, [selectedMessage]);

    const sendQuestion = () => {
        if (disabled || !question.trim()) {
            return;
        }

        onSend(question);

        if (clearOnSend) {
            setQuestion("");
            setSelectedMessage(""); // Clear the selected message
        }
    };

    const resetFunction = () => {
        // setisreset(true);
        if (!disabled) {
            clearchat();
        }
    };
    const onEnterPress = (ev: React.KeyboardEvent<Element>) => {
        if (ev.key === "Enter" && !ev.shiftKey) {
            ev.preventDefault();
            sendQuestion();
        }
    };

    const onQuestionChange = (_ev: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, newValue?: string) => {
        if (!newValue) {
            setQuestion("");
        } else {
            setQuestion(newValue);
        }
    };

    const sendQuestionDisabled = disabled || !question.trim();
    const resetDisabled = !lastQuestionRef.current || disabled;

    return (
        <Stack horizontal className={styles.questionInputContainer}>
            {!disabled ? (
                <Tooltip title="File Upload" placement="left">
                    {fileuploadelement}
                </Tooltip>
            ) : (
                <>{fileuploadelement}</>
            )}
            {/* {value} value + {question} question + {isContent} isContent + {valueOverload} valueOverload */}
            {/* {valueOverload} */}
            <TextField
                className={styles.questionInputTextArea}
                placeholder={placeholder}
                multiline
                resizable={false}
                borderless
                // value={contentvalue}
                value={question}
                onChange={onQuestionChange}
                onKeyDown={onEnterPress}
                disabled={disabled ? true : false}
                style={{ height: "50px", fontSize: "11px" }}
            />
            <div className={styles.questionInputButtonsContainer}>
                <div aria-label="Ask question button" onClick={sendQuestion}>
                    {/* {!disabled ? ( */}
                    <Tooltip title="Submit" placement="left">
                        <Send28Filled
                            // primaryFill="rgba(115, 118, 225, 1)"
                            primaryFill="rgba(0, 180, 237, 0.6)"
                            className={`${sendQuestionDisabled ? styles.questionInputSendButtonDisabled : ""}`}
                            // className={`${sendPlaceHolderDisabled ? styles.questionInputSendButtonDisabled : ""}`}
                        />
                    </Tooltip>
                </div>
            </div>
            <div className={styles.questionInputButtonsContainer}>
                {
                    // !disabled ?
                    <ClearChatButton
                        className={`${resetDisabled ? styles.questionInputSendButtonDisabled : styles.resetIcon}`}
                        // className={styles.resetIcon}
                        onClick={resetFunction}
                        disabled={resetDisabled}
                        // disabled={!lastQuestionRef.current || disabled}
                    />
                    // :
                    // <></>
                }
            </div>
        </Stack>
    );
};
