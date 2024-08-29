// src/components/UserChatMessage.tsx
import React, { useEffect } from "react";
import styles from "./UserChatMessage.module.css";
import { Stack, ActionButton } from "@fluentui/react";
import { useRecoilState } from "recoil";
import { selectedMessageAtom } from "../UserChatMessage/Atom";

interface UserChatMessageProps {
    message: string;
}

export const UserChatMessage: React.FC<UserChatMessageProps> = ({ message }) => {
    const [selectedMessage, setSelectedMessage] = useRecoilState(selectedMessageAtom);

    const handleButtonClick = () => {
        setSelectedMessage(message);
    };

    return (
        <Stack className={`${styles.answerContainer}`} verticalAlign="space-between">
            <div className={styles.container}>
                <div className={styles.message}>
                    <ActionButton
                        style={{ color: "black", paddingRight: "15px", margin: "auto" }}
                        iconProps={{ iconName: "Edit" }}
                        title="Edit Message"
                        onClick={handleButtonClick}
                    />
                    <div style={{ margin: "auto" }}>{message}</div>
                </div>
            </div>
        </Stack>
    );
};
