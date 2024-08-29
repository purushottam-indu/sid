import styles from "./ClearChatButton.module.css";
import resetImage from "../../assets/reset.png";
import Tooltip from "@mui/material/Tooltip";
interface Props {
    className?: string;
    onClick: () => void;
    disabled?: boolean;
}

export const ClearChatButton = ({ className, disabled, onClick }: Props) => {
    return (
        <>
            <Tooltip title="Clear Chat" placement="right">
                <div className={`${styles.container} ${className ?? ""} ${disabled && styles.disabled}`} onClick={onClick}>
                    <div style={{ marginLeft: "15px", marginRight: "5px" }}>
                        <img
                            src={resetImage}
                            alt="Reset"
                            className={styles.resetIcon}
                            style={{ width: "40px", height: "40px" }} // Set the size here
                        />
                    </div>
                </div>
            </Tooltip>
        </>
    );
};
