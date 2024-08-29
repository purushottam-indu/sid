import { useMemo } from "react";
import { Stack, ActionButton } from "@fluentui/react";
import { IIconProps, initializeIcons } from "@fluentui/react";
import { TooltipHost, ITooltipHostStyles } from "@fluentui/react/lib/Tooltip";
import { IconButton } from "@fluentui/react/lib/Button";
import { useId } from "@fluentui/react-hooks";
import DOMPurify from "dompurify";
import styles from "./Answer.module.css";
import { AskResponse } from "../../api";
import { parseAnswerToHtml } from "./AnswerParser";
import { AnswerIcon } from "./AnswerIcon";
import rehypeRaw from "rehype-raw";
import rehypeHighlight from "rehype-highlight";
import Markdown from "react-markdown";
import "highlight.js/styles/github-dark.css";
import { useState } from "react";
import { saveAs } from "file-saver"; // For saving files
import { Document, Packer, Paragraph, TextRun } from "docx";
import jsPDF from "jspdf";
import japaneseFontFamily from "../../assets/NotoSansJP-Regular.ttf";
// import { Dropdown } from "@fluentui/react";

// UserChatMessage Component

// Answer Component
interface Props {
    answer: AskResponse;
    onFollowupQuestionClicked: (question: string) => void;
    showFollowupQuestions?: boolean;
    isAnswerCompleted?: boolean;
    regenerateResponse?: boolean;
    regenerateQuestion: string;
}

export const Answer = ({ answer, onFollowupQuestionClicked, showFollowupQuestions, isAnswerCompleted, regenerateResponse, regenerateQuestion }: Props) => {
    const parsedAnswer = useMemo(() => parseAnswerToHtml(answer.answer), [answer]);
    const sanitizedAnswerHtml = DOMPurify.sanitize(parsedAnswer.answerHtml);

    const handleExportTXT = () => {
        const txtBlob = new Blob([parsedAnswer.answerHtml], { type: "text/plain;charset=utf-8" });
        saveAs(txtBlob, "response.txt");
    };

    const handleExportPDF = async () => {
        const doc = new jsPDF();
        const margin = 20; // Set your desired margin value
        const topMargin = margin; // Adjust this value to set the top margin
        const bottomMargin = margin; // Adjust this value to set the bottom margin
        let cursorY = topMargin;
        let remainingText = parsedAnswer.answerHtml;
        const lineHeight = 6; // Assuming a line height of 12 units (adjust as needed)
        const availableHeight = doc.internal.pageSize.height - topMargin - bottomMargin;

        const fontSize = 12; // Set your desired smaller font size
        doc.setFontSize(fontSize);

        const fontUrl = japaneseFontFamily;

        // Fetch the TTF font file as an ArrayBuffer
        const fontBytes = await fetch(fontUrl).then(res => res.arrayBuffer());

        // Convert the ArrayBuffer to a Base64 string
        const base64String = btoa(new Uint8Array(fontBytes).reduce((data, byte) => data + String.fromCharCode(byte), ""));

        doc.addFileToVFS("NotoSansJP-Regular.ttf", base64String);
        doc.addFont("NotoSansJP-Regular.ttf", "NotoSansJP", "normal");

        doc.setFont("NotoSansJP");

        const addNewPage = () => {
            doc.addPage();
            cursorY = topMargin;
        };

        const lines = doc.splitTextToSize(remainingText, doc.internal.pageSize.width - 2 * margin);

        lines.forEach((line: string) => {
            if (cursorY + lineHeight > availableHeight) {
                addNewPage();
            }

            doc.text(line, margin, cursorY);
            cursorY += lineHeight;
        });

        doc.save("response.pdf");
    };

    const preprocessHTML = (html: string): string => {
        const processedHtml = html.replace(/\n/g, "<br>");
        return processedHtml;
    };

    const handleExportDOCX = async () => {
        const processedHtml = preprocessHTML(parsedAnswer.answerHtml);
        const tempElement = document.createElement("div");
        tempElement.innerHTML = processedHtml;

        // Extract text content
        const paragraphs = Array.from(tempElement.childNodes).map(node => {
            if (node.nodeType === Node.TEXT_NODE) {
                return new Paragraph({
                    children: [new TextRun(node.textContent || "")]
                });
            } else if (node.nodeType === Node.ELEMENT_NODE) {
                const element = node as HTMLElement;
                const textRuns = Array.from(element.childNodes).map(childNode => {
                    if (childNode.nodeType === Node.TEXT_NODE) {
                        return new TextRun(childNode.textContent || "");
                    } else if (childNode.nodeType === Node.ELEMENT_NODE) {
                        const childElement = childNode as HTMLElement;
                        return new TextRun(childElement.innerText);
                    } else {
                        return new TextRun("");
                    }
                });
                return new Paragraph({
                    children: textRuns
                });
            } else {
                return new Paragraph({
                    children: [new TextRun("")]
                });
            }
        });

        // Create document
        const doc = new Document({
            sections: [
                {
                    properties: {},
                    children: paragraphs
                }
            ]
        });

        // Generate blob
        const blob = await Packer.toBlob(doc);

        saveAs(blob, "response.docx");
    };

    const [showOptions, setShowOptions] = useState(false);
    const [exportFormat, setExportFormat] = useState<string | undefined>(undefined);

    const handleExportChange = (event: React.FormEvent<HTMLDivElement>, option?: { key: string }) => {
        if (option) {
            setExportFormat(option.key);
            switch (option.key) {
                case "pdf":
                    handleExportPDF();
                    break;
                case "txt":
                    handleExportTXT();
                    break;
                case "docx":
                    handleExportDOCX();
                    break;
                default:
                    break;
            }
        }
    };

    const exportOptions = [
        { key: "pdf", text: "PDF" },
        { key: "txt", text: "TXT" },
        { key: "docx", text: "DOCX" }
    ];

    const pdftooltipId = useId("tooltip_pdf");
    const wordtooltipID = useId("tooltip_word");
    const texttooltipID = useId("tooltip_txt");

    const calloutProps = {
        gapSpace: 0,
        styles: {
            beak: { background: "white" },
            beakCurtain: { background: "#c2c2d6" },
            calloutMain: { background: "white" }
        }
    };
    const hostStyles: Partial<ITooltipHostStyles> = {
        root: {
            display: "inline-block"
            // , background: "rgb(255, 255, 128)"
        }
    };
    initializeIcons();

    const wordIcon: IIconProps = { iconName: "WordDocument" };
    const pdfIcon: IIconProps = { iconName: "PDF" };
    const txtIcon: IIconProps = { iconName: "TextDocument" };

    return (
        <Stack className={`${styles.answerContainer}`} verticalAlign="space-between">
            <Stack.Item>
                <Stack horizontal horizontalAlign="space-between">
                    <AnswerIcon />
                    {!isAnswerCompleted && (
                        <>
                            <Stack horizontal>
                                <ActionButton
                                    style={{ color: "black" }}
                                    iconProps={regenerateResponse ? { iconName: "Refresh" } : { iconName: "" }}
                                    title="Regenerate"
                                    ariaLabel="Refresh"
                                    onClick={() => onFollowupQuestionClicked(regenerateQuestion)}
                                    disabled={regenerateResponse ? false : true}
                                ></ActionButton>
                                <ActionButton
                                    style={{ color: "black" }}
                                    iconProps={{ iconName: "Copy" }}
                                    title="Copy to clipboard"
                                    ariaLabel="Copy Code content"
                                    onClick={() => {
                                        navigator.clipboard.writeText(parsedAnswer.answerHtml);
                                    }}
                                    disabled={isAnswerCompleted ? true : false}
                                ></ActionButton>
                                <ActionButton
                                    style={{ color: "black" }}
                                    iconProps={{ iconName: "Download" }}
                                    title="Export"
                                    onClick={() => setShowOptions(!showOptions)}
                                ></ActionButton>
                                {showOptions && (
                                    <Stack horizontal tokens={{ childrenGap: 10 }}>
                                        <TooltipHost content="PDF" id={pdftooltipId} styles={hostStyles}>
                                            {/* // calloutProps={calloutProps} */}
                                            <div>
                                                <IconButton
                                                    style={{
                                                        color: "red"
                                                    }}
                                                    onClick={handleExportPDF}
                                                    iconProps={pdfIcon}
                                                    // title="PDF"
                                                ></IconButton>
                                            </div>
                                        </TooltipHost>
                                        <TooltipHost content="TXT" id={texttooltipID} styles={hostStyles}>
                                            <div>
                                                <IconButton
                                                    style={{
                                                        color: "black"
                                                    }}
                                                    onClick={handleExportTXT}
                                                    iconProps={txtIcon}
                                                    // title="TXT"
                                                ></IconButton>
                                            </div>
                                        </TooltipHost>
                                        <TooltipHost content="DOCX" id={wordtooltipID} styles={hostStyles}>
                                            <div>
                                                <IconButton
                                                    style={{
                                                        color: "blue"
                                                    }}
                                                    onClick={handleExportDOCX}
                                                    iconProps={wordIcon}
                                                    // title="DOCX"
                                                ></IconButton>
                                            </div>
                                        </TooltipHost>
                                    </Stack>
                                )}
                            </Stack>
                        </>
                    )}
                </Stack>
            </Stack.Item>

            <Stack.Item grow className={`${styles.answerStackItem}`}>
                <Markdown rehypePlugins={[rehypeRaw as any, rehypeHighlight]}>{parsedAnswer.answerHtml}</Markdown>
            </Stack.Item>

            {!!parsedAnswer.followupQuestions.length && showFollowupQuestions && onFollowupQuestionClicked && (
                <Stack.Item className={`${styles.answerStackItem}`}>
                    <Stack horizontal wrap className={`${styles.followupQuestionsList}`} tokens={{ childrenGap: 6 }}>
                        <span className={styles.followupQuestionLearnMore}>Follow-up questions:</span>
                        {parsedAnswer.followupQuestions.map((x, i) => {
                            return (
                                <a key={i} className={styles.followupQuestion} title={x} onClick={() => onFollowupQuestionClicked(x)}>
                                    {`${x}`}
                                </a>
                            );
                        })}
                    </Stack>
                </Stack.Item>
            )}
        </Stack>
    );
};
