import { Text } from "@fluentui/react";
import { PersonFeedback24Regular } from "@fluentui/react-icons";

import styles from "./FeedbackButton.module.css";

interface Props {
    className?: string;
}

export const FeedbackButton = ({ className }: Props) => {
    const onClickFeedbackButton = () => {
        console.log("ok");
        window.open(
            "https://forms.office.com/Pages/ResponsePage.aspx?id=h5QXsCYw90S81iXtRSE40Cg1HtlUAJ5AviIohVLonMhUOFhCSzZSNjRBQ1VZTlhNU09HOVhRRTdDQy4u",
            "_blank"
        );
    };

    return (
        <div className={`${styles.container} ${className ?? ""}`} onClick={onClickFeedbackButton}>
            <PersonFeedback24Regular />
            <Text>{"Feedback"}</Text>
        </div>
    );
};
