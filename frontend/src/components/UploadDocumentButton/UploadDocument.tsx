import { IoMdAttach } from "react-icons/io";
 
import styles from "./UploadDocumentButton.module.css";
 
interface Props {
    className?: string;
    onClick: () => void;
    disabled?: Boolean;
}
 
export const UploadDocumentButton = ({ className, disabled, onClick }: Props) => {
    return (
        <div className={`${styles.container} ${className ?? ""}`} onClick={onClick}>
            <IoMdAttach />
        </div>
    );
};
 
