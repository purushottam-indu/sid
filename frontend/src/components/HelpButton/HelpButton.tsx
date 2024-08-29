import { Text } from "@fluentui/react";
import { ChatHelp24Regular } from "@fluentui/react-icons";

import styles from "./HelpButton.module.css";

interface Props {
    className?: string;
    onClick: () => void;
    disabled?: boolean;
}

export const HelpButton = ({ className, disabled, onClick }: Props) => {
    return (
        <div className={`${styles.container} ${className ?? ""} ${disabled && styles.disabled}`} onClick={onClick}>
            <ChatHelp24Regular />
            <Text>{"Help"}</Text>
        </div>
    );
};
