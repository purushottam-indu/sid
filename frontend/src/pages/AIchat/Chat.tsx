import { useRef, useState, useEffect } from "react";
import { useBoolean } from "@fluentui/react-hooks";
import { DefaultButton, Text } from "@fluentui/react";
import readNDJSONStream from "ndjson-readablestream";
import styles from "./Chat.module.css";
import { chatApi, Approaches, AskResponse, ChatRequest, ChatTurn } from "../../api";
import { Answer, AnswerError, AnswerLoading } from "../../components/Answer";
import { QuestionInput } from "../../components/QuestionInput";
import { UserChatMessage } from "../../components/UserChatMessage";
import { AnalysisPanelTabs } from "../../components/AnalysisPanel";
import { IDropdownOption } from "@fluentui/react/lib/Dropdown";
import { Access } from "../../api";
import { accessApi } from "../../api";
import { UploadDocumentButton } from "../../components/UploadDocumentButton/UploadDocument";
import FileUploadModal from "../../components/FileUpload/FileUpload";
import { FileUpload, uploadApi } from "../../api";
import { Snackbar, Alert, AlertTitle } from "@mui/material";
import "../../components/Navbar/navbar.css";
import { useRecoilState } from "recoil";
import { selectedMessageAtom } from "../../components/UserChatMessage/Atom";
import { FaStop } from "react-icons/fa6";
import { useTheme } from "../../ThemeContext";

interface ChatProps {
    isSideBarOpen: boolean;
    promptTemplate: string;
    setPromptTemplate: (promptTemplate: string) => void;
}

const Chat = ({ isSideBarOpen, promptTemplate, setPromptTemplate }: ChatProps) => {
    // console.log("inChat ", isSideBarOpen);
    const [isConfigPanelOpen, setIsConfigPanelOpen] = useState(false);
    // const [promptTemplate, setPromptTemplate] = useState<string>("");
    const [shouldStream, setShouldStream] = useState<boolean>(true);
    const [isScreenSmall, setIsScreenSmall] = useState<boolean>(window.innerWidth < 769);
    const [useSuggestFollowupQuestions, setUseSuggestFollowupQuestions] = useState<boolean>(false);
    const lastQuestionRef = useRef<string>("");
    const chatMessageStreamEnd = useRef<HTMLDivElement | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [isAnswerCompleted, setAnswerCompletion] = useState<boolean>(false);
    const [error, setError] = useState<unknown>();
    const [isOpen, { setTrue: openHelpWindow, setFalse: dismissHelpWindow }] = useBoolean(false);
    const [activeCitation, setActiveCitation] = useState<string>();
    const [activeAnalysisPanelTab, setActiveAnalysisPanelTab] = useState<AnalysisPanelTabs | undefined>(undefined);

    const modelApproach = useRef<string>("GPT3.5");
    const [modelApproachState, setModelApproachState] = useState<string>("GPT3.5");

    const [selectedAnswer, setSelectedAnswer] = useState<number>(0);
    const [answers, setAnswers] = useState<[user: string, response: AskResponse][]>([]);
    const [sliderValue, setSliderValue] = useState(5);
    const promptHasChanged = useRef<boolean>(false);
    const sliderAriaValueText = (value: number) => `${value / 10}`;
    const sliderValueFormat = (value: number) => `${value / 10}`;
    const [fileUploadPanelOpen, setFileUploadPanelOpen] = useState(false);
    const [fileNames, setFileNames] = useState<string[]>([]);
    const [files, setFiles] = useState<File[]>([]);
    const [isEmbeddingsLoading, setIsEmbeddingsLoading] = useState(false);
    const [embeddingsLoaded, setEmbeddingsLoaded] = useState(false);
    const [openAlert, setOpenAlert] = useState(false);
    const [selectedModel, setSelectedModel] = useState<IDropdownOption | undefined>({ key: "GPT3.5", text: "GPT 3.5" });
    const [openDocClearAlert, setOpenDocClearAlert] = useState(false);
    const [openDocClearAlertforchat, setOpenDocClearAlertforchat] = useState(false);
    const [openWarning, setWarning] = useState(false);
    const [stopGenerating, setStopGenerating] = useState(false);
    const { isDarkTheme, toggleTheme } = useTheme();
    const [uploaded_files, setuploaded_files] = useState<string[]>([]);
    const [openGuidlinesAlert, setOpenGuidlinesAlert] = useState(false);

    const onChangeModel = (event: React.FormEvent<HTMLDivElement>, item: IDropdownOption | undefined): void => {
        setSelectedModel(item);
    };

    const sliderOnChange = (value: number) => setSliderValue(value);

    const getStyles = () => ({
        main: [
            {
                selectors: {
                    ["@media (min-width: 720px)"]: {
                        maxHeight: "90%",
                        minWidth: "800px",
                        maxWidth: "900px"
                    }
                }
            }
        ]
    });

    const openFileUploadPanel = () => {
        if (!isAnswerCompleted) setFileUploadPanelOpen(true);
    };
    const closeFileUploadPanel = () => {
        setFileUploadPanelOpen(false);
    };

    const handleSubmitFile = async (event: React.FormEvent) => {
        event.preventDefault();
        setIsEmbeddingsLoading(true);

        // const prevFileNamesCopy = [...fileNames];
        // console.log("prevFileNamesCopy: ", prevFileNamesCopy);

        try {
            if (files.length > 0) {
                const request: FileUpload = {
                    files: files
                };

                const response = await uploadApi(request);

                // console.log("API Response:", response);

                if (response.status === "success") {
                    setOpenAlert(true);
                    setEmbeddingsLoaded(true);
                    setFileNames([]);
                    // Assuming files is an array of File objects
                    const uploadedFileNames = files.map(file => file.name);

                    // Append the uploaded file names to the fileNames state
                    setuploaded_files(prevFileNames => [...prevFileNames, ...uploadedFileNames]);
                }
            }
        } catch (error: unknown) {
            console.error("Error uploading files:", error);
            setFileNames([]);
            // Set state to show Snackbar with error message
            if (error instanceof Error) {
                if (error.message === "try_after_some_time") {
                    console.error("if try_after_some_time");
                    setSnackbarMessage("Please Try after some time");
                    setOpenSnackbar(true);
                    // setFileNames(prevFileNamesCopy);
                } else if (error.message === "file_size_error") {
                    console.error("if file_size_error");
                    setSnackbarMessage("Upload small size files, or try with few number of files");
                    setOpenSnackbar(true);
                    // setFileNames(prevFileNamesCopy);
                } else if (error.message === "csv_excel_error") {
                    console.error("if csv_excel:", error);
                    setSnackbarMessage("Upload Single Excel or CSV File, Cannot be uploaded with multiple files.");
                    setOpenSnackbar(true);
                    // setFileNames(prevFileNamesCopy);
                } else if (error.message === "csv_excel_already_present_error") {
                    console.error("if csv_excel_already_present:", error);
                    setSnackbarMessage("CSV/Excel already uploaded, Clear it and try uploading");
                    setOpenSnackbar(true);
                    // setFileNames(prevFileNamesCopy);
                } else if (error.message === "unstructured_data_already_uploaded") {
                    console.error("if unstructured_data_already_uploaded:", error);
                    setSnackbarMessage("Delete the previously uploaded files before uploading CSV/Excel, and try uploading");
                    setOpenSnackbar(true);
                    // setFileNames(prevFileNamesCopy);
                } else {
                    console.error("else:", error);
                    setSnackbarMessage("Please Try after some time");
                    setOpenSnackbar(true); // Assuming you have setOpenSnackbar to control the visibility
                    // alert("Error uploading files. Please check the console for details.");
                    // setFileNames(prevFileNamesCopy);
                }
            }

            // console.log("catch error");
        } finally {
            setIsEmbeddingsLoading(false);
        }
    };

    const [infoAlert, setInfoAlert] = useState(false);

    const handleAlertClose = () => {
        setOpenAlert(false);
        setWarning(false);
        setInfoAlert(false);
        setOpenDocClearAlert(false);
        setOpenDocClearAlertforchat(false);
        setOpenGuidlinesAlert(false);
    };

    //Fileupload
    const fileuploadelement = () => {
        return (
            <div className={styles.upload} style={{ fontSize: "30px", marginLeft: "4px" }}>
                <UploadDocumentButton className={!isAnswerCompleted ? styles.commandButton : styles.commandButtonDisabled} onClick={openFileUploadPanel} />
                <FileUploadModal
                    open={fileUploadPanelOpen}
                    embeddingsLoaded={embeddingsLoaded}
                    isEmbeddingsLoading={isEmbeddingsLoading}
                    fileNames={fileNames}
                    openAlert={openAlert}
                    openWarning={openWarning}
                    infoAlert={infoAlert}
                    openDocClearAlert={openDocClearAlert}
                    handleCloseModal={closeFileUploadPanel}
                    handleFileUpload={handleFileUpload}
                    handleSubmitFile={handleSubmitFile}
                    handleAlertClose={handleAlertClose}
                    deleteEmbeddings={deleteEmbeddings}
                    openSnackbar={openSnackbar}
                    snackbarMessage={snackbarMessage}
                    handleSnackbarClose={handleSnackbarClose}
                />
            </div>
        );
    };

    const handleFileUpload = (uploadedFiles: File[]) => {
        //initialize
        setFiles([]);
        setFileNames([]);
        // setEmbeddingsLoaded(false);

        const allowedExtensions = /(\.pdf|\.txt|\.pptx|\.docx|\.csv|\.xlsx)$/i;

        uploadedFiles.forEach(file => {
            if (!allowedExtensions.exec(file.name)) {
                alert("Please upload PDF/TXT/DOCX/PPTX/CSV/XLSX files only");
                return;
            }

            if (file.size > 10 * 1000 * 1024) {
                setWarning(true);
                return;
            }

            if (file.size > 5 * 1000 * 1024) {
                setInfoAlert(true);
            }

            setFiles(prevFiles => [...prevFiles, file]);
            setFileNames(prevFileNames => [...prevFileNames, file.name]);
        });
    };

    //Prompt
    const closeConfigPanel = () => {
        setIsConfigPanelOpen(false);
        if (promptHasChanged.current == true) {
            clearChat();
            promptHasChanged.current = false;
        }
    };

    const clearPrompt = () => {
        setPromptTemplate("");
        clearChat();
    };

    const deleteEmbeddings = () => {
        embeddingInit();
        setOpenDocClearAlert(true);
        clearEmbeddings();
    };
    const deleteEmbeddingsforchat = () => {
        embeddingInit();
        setOpenDocClearAlertforchat(true);
        clearEmbeddings();
        setOpenGuidlinesAlert(false);
    };

    const embeddingInit = () => {
        setFiles([]);
        setFileNames([]);
        setEmbeddingsLoaded(false);
    };
    const clearEmbeddings = () => {
        // Call the API to delete the folder on the backend
        setuploaded_files([]);
        fetch("/delete-folder", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
                // Include any other headers your backend requires, such as authentication tokens
            }
            // If you need to send data along with the delete request, include it here.
            // body: JSON.stringify({ folderName: 'folder_to_delete' }),
        })
            .then(response => {
                // Check if the response status code is not in the range 200-299
                if (!response.ok) {
                    return response.text().then(text => {
                        throw new Error(text || "Server responded with an error!");
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log("Folder deleted successfully:", data);
                // Clear state only after the folder has been successfully deleted
            })
            .catch(error => {
                console.error("Error deleting the folder:", error.message);
                // Handle the error state here if needed
            });

        // Open the alert to notify the user
    };

    async function stopGeneratingAnswer() {
        setStopGenerating(true);
        console.log("stopping answer generation");
    }

    let stop = false;

    //API CALL
    const makeApiRequest = async (question: string) => {
        lastQuestionRef.current = question;

        error && setError(undefined);
        setIsLoading(true);
        setActiveCitation(undefined);
        setActiveAnalysisPanelTab(undefined);

        try {
            const history: ChatTurn[] = answers.map(a => ({ user: a[0], bot: a[1].answer }));
            const request: ChatRequest = {
                history: [...history, { user: question, bot: undefined }],
                approach: embeddingsLoaded ? Approaches.DocumentQNA : Approaches.General,
                shouldStream: shouldStream,
                overrides: {
                    modelType: modelApproach.current,
                    promptTemplate: promptTemplate.length === 0 ? undefined : promptTemplate,
                    suggestFollowupQuestions: useSuggestFollowupQuestions,
                    temperature: sliderValue / 10
                }
            };

            console.log(request + " as request ");

            setAnswerCompletion(true);

            const response = await chatApi(request);

            if (!response.body) {
                throw Error("No response body");
            }
            if (shouldStream) {
                let answer: string = "";
                // let isAnswerCompleted: boolean = false;
                let askResponse: AskResponse = {} as AskResponse;

                for await (const event of readNDJSONStream(response.body)) {
                    // console.log("inside loop: ", document.getElementById("stop")?.innerText)
                    if (document.getElementById("stop")?.title == "Continue") {
                        // if (document.getElementById("stop")?.innerHTML == "Continue") {
                        setStopGenerating(false);
                        break;
                    }
                    if (event["data_points"]) {
                        askResponse = event;
                    } else if (event["choices"] && event["choices"][0]["delta"]["content"]) {
                        answer += event["choices"][0]["delta"]["content"];
                        let latestResponse: AskResponse = { ...askResponse, answer: answer };
                        setIsLoading(false);
                        setAnswers([...answers, [question, latestResponse]]);
                        // console.log("answer", answer);
                    } else if (event["error"]) {
                        alert(event["error"]);
                    }
                    // console.log("event", JSON.stringify(event));
                }
                setAnswerCompletion(false);
                setContentValue("");
                setContent(false);
            } else {
                const parsedResponse: AskResponse = await response.json();

                if (response.status > 299 || !response.ok) {
                    throw Error(parsedResponse.error || "Unknown error");
                }
                setAnswers([...answers, [question, parsedResponse]]);
            }
        } catch (e) {
            setError(e);
        } finally {
            setIsLoading(false);
        }
    };

    //Clear Chat
    const clearChat = () => {
        lastQuestionRef.current = "";
        error && setError(undefined);
        setActiveCitation(undefined);
        setActiveAnalysisPanelTab(undefined);
        setAnswers([]);
    };

    useEffect(() => chatMessageStreamEnd.current?.scrollIntoView({ behavior: "smooth" }), [isLoading]);

    const onUseSuggestFollowupQuestionsChange = (_ev?: React.FormEvent<HTMLElement | HTMLInputElement>, checked?: boolean) => {
        setUseSuggestFollowupQuestions(!!checked);
    };

    const onToggleTab = (tab: AnalysisPanelTabs, index: number) => {
        if (activeAnalysisPanelTab === tab && selectedAnswer === index) {
            setActiveAnalysisPanelTab(undefined);
        } else {
            setActiveAnalysisPanelTab(tab);
        }

        setSelectedAnswer(index);
    };

    //snackbar for error message
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState("");

    const handleSnackbarClose = (event?: React.SyntheticEvent, reason?: string) => {
        if (reason === "clickaway") {
            return;
        }
        setOpenSnackbar(false);
    };
    //check for permitted users, Access :
    const [hasAccess, setHasAccess] = useState<Access>({ hasModAccess: false });

    const makeAccessApiRequest = async () => {
        try {
            const response = await accessApi();
            console.log(response);
            setHasAccess(response);
        } catch (e) {
            console.log(e);
        }
    };

    useEffect(() => {
        // This function will be called only once during the initial render

        try {
            embeddingInit();
            clearEmbeddings();
        } catch (e) {
            console.log(e);
        }
        makeAccessApiRequest();

        // Cleanup function (optional)
        return () => {
            console.log(hasAccess);
        };
    }, []);

    const handleModelApproachChange = (_ev?: React.MouseEvent<HTMLElement>, newAlignment?: string) => {
        setModelApproachState(newAlignment || "GPT3.5");
        modelApproach.current = newAlignment || "GPT3.5";
        console.log(newAlignment);
        clearChat();
    };

    const handleClick = () => {
        // Open another link
        window.open(
            // "https://sankyopharma.sharepoint.com/sites/DSTeam_CoE_AIML/Shared%20Documents/Forms/AllItems.aspx?isAscending=true&OR=Teams%2DHL&CT=1710835373668&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiIyNy8yNDAyMDExOTMwNyIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D&sortField=LinkFilename&id=%2Fsites%2FDSTeam%5FCoE%5FAIML%2FShared%20Documents%2FGeneral%2FOpen%20AI%20Enablement%2F00%20Documents%20Approved%20by%20Legal%2C%20Compliance%2C%20Comms%2FChatDSI%20Usage%20Guidelines%5F3%2D26%2D24%2Epdf&viewid=b54b96d0%2Dd392%2D4730%2Db9a0%2D5ead22297885&parent=%2Fsites%2FDSTeam%5FCoE%5FAIML%2FShared%20Documents%2FGeneral%2FOpen%20AI%20Enablement%2F00%20Documents%20Approved%20by%20Legal%2C%20Compliance%2C%20Comms",
            // "_blank"
            "https://sankyopharma.sharepoint.com/:b:/s/DSTeam_CoE_AIML/ETF4r68T6mtFvor7wgAhrLQBHh-g4dzaSzVvZNef3J4Uug?e=h6eeNO",
            "_blank"
        );
    };

    // Creativity button
    const [selectedButton, setSelectedButton] = useState("More Balanced");
    const handleButtonClick = (buttonName: string) => {
        setSelectedButton(buttonName);
        // Set slider value based on button clicked
        switch (buttonName) {
            case "More Creative":
                setSliderValue(10);
                break;
            case "More Balanced":
                setSliderValue(5);
                break;
            case "More Precise":
                setSliderValue(1);
                break;
            default:
                break;
        }
    };

    // const [isNavbarExpanded, setIsNavbarExpanded] = useState(false);
    const [, setSelectedMessage] = useRecoilState(selectedMessageAtom);
    const [contentValue, setContentValue] = useState<string>("");
    const [isContent, setContent] = useState<boolean>(false);
    useEffect(() => {
        const handleResize = () => {
            setIsScreenSmall(window.innerWidth < 769);
        };

        window.addEventListener("resize", handleResize);

        return () => {
            window.removeEventListener("resize", handleResize);
        };
    }, []);

    if (isSideBarOpen && isScreenSmall) {
        return null; // or you can return <div></div> or any placeholder content
    }
    return (
        <div className={` ${isSideBarOpen ? styles.shrunk : styles.container}`}>
            {" "}
            <div className={styles.chatRoot}>
                <div className={styles.chatContainer}>
                    {!lastQuestionRef.current ? (
                        <div className={styles.chatEmptyState}>
                            <p className={styles.disclaimerText} style={{ filter: isDarkTheme ? "brightness(20)" : "brightness(1)" }}>
                                *ChatDSI is designed to engage in natural language conversations, answer questions, and assist with various tasks but currently
                                cannot access DSI repositories to obtain internally stored information. Since it is an AI-powered assistant, output should
                                always be validated by a human prior to use. Please follow the{" "}
                                <span onClick={handleClick} style={{ textDecoration: "underline", cursor: "pointer" }}>
                                    ChatDSI Usage Guidelines
                                </span>{" "}
                                at all times.
                            </p>
                            {/* <Query /> */}
                            <div className={styles.boxesContainerquerySuggestion}>
                                <div
                                    className={styles.boxquerySuggestion}
                                    onClick={() => setSelectedMessage("Show me an example of R code to run a Kaplan-Meier plot using a survival package.")}
                                >
                                    <p className={styles.querytitle}>Coding</p>
                                    “Show me an example of R code to run a Kaplan-Meier plot using a survival package.”
                                </div>
                                <div
                                    className={styles.hideboxquerySuggestion}
                                    onClick={() =>
                                        setSelectedMessage("Provide an easy-to-read summary of the following article that is no more than 750 words: ")
                                    }
                                >
                                    <p className={styles.querytitle}>Summarization</p>
                                    “Provide an easy-to-read summary of the following article that is no more than 750 words: ”
                                </div>
                                <div
                                    className={styles.boxquerySuggestion}
                                    onClick={() =>
                                        setSelectedMessage(
                                            "Please refine the conclusion of my research paper on the impact of artificial intelligence in drug discovery to make it clearer and emphasize the following findings:"
                                        )
                                    }
                                >
                                    <p className={styles.querytitle}>Writing Assistance</p>
                                    “Please refine the conclusion of my research paper on the impact of artificial intelligence in drug discovery to make it
                                    clearer and emphasize the following findings: ”
                                </div>
                                <div
                                    className={styles.boxquerySuggestion}
                                    onClick={() =>
                                        setSelectedMessage(
                                            "Explore the possibility of predicting individual health outcomes based on various factors (genetics, lifestyle, medical history). Develop a predictive model that tailors recommendations for personalized healthcare interventions."
                                        )
                                    }
                                >
                                    <p className={styles.querytitle}>Summarization</p>
                                    “Explore the possibility of predicting individual health outcomes based on various factors (genetics, lifestyle, medical
                                    history). Develop a predictive model that tailors recommendations for personalized healthcare interventions.”
                                </div>
                                <div
                                    className={styles.hideboxquerySuggestion}
                                    onClick={() => setSelectedMessage("In Excel (Office 365), how do I remove duplicate entries from a column of data? ")}
                                >
                                    <p className={styles.querytitle}>Tutoring</p>
                                    “In Excel (Office 365), how do I remove duplicate entries from a column of data?”
                                </div>
                                <div
                                    className={styles.hideboxquerySuggestion}
                                    onClick={() => setSelectedMessage("Create a job description for a Data Analyst to work in [open role] at Daiichi Sankyo.")}
                                >
                                    <p className={styles.querytitle}>Creation</p>
                                    "Create a job description for a Data Analyst to work in [open role] at Daiichi Sankyo.”
                                </div>
                            </div>
                            <div className={styles.cylindricalBar}>
                                <div className={styles.responseStyle}>Select Response Style</div>
                                <div className={styles.buttonContainer}>
                                    <DefaultButton
                                        className={`${styles.temperatureButton} ${selectedButton === "More Creative" ? styles.clicked : ""}`}
                                        onClick={() => handleButtonClick("More Creative")}
                                    >
                                        More Creative
                                    </DefaultButton>
                                    <DefaultButton
                                        className={`${styles.temperatureButton} ${selectedButton === "More Balanced" ? styles.clicked : ""}`}
                                        onClick={() => handleButtonClick("More Balanced")}
                                    >
                                        More Balanced
                                    </DefaultButton>
                                    <DefaultButton
                                        className={`${styles.temperatureButton} ${selectedButton === "More Precise" ? styles.clicked : ""}`}
                                        onClick={() => handleButtonClick("More Precise")}
                                    >
                                        More Precise
                                    </DefaultButton>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className={styles.chatMessageStream}>
                            {answers.map((answer, index) => (
                                <div key={index}>
                                    <UserChatMessage message={answer[0]} />
                                    {/* {answers.length} and {index + 1} and {answer[0]} and {lastQuestionRef.current} */}
                                    <div className={styles.chatMessageGpt}>
                                        <Answer
                                            key={index}
                                            answer={answer[1]}
                                            onFollowupQuestionClicked={q => makeApiRequest(q)}
                                            showFollowupQuestions={useSuggestFollowupQuestions && answers.length - 1 === index}
                                            isAnswerCompleted={isAnswerCompleted && answers.length === index + 1 && answer[0] === lastQuestionRef.current}
                                            regenerateResponse={answers.length === index + 1 && answer[0] === lastQuestionRef.current}
                                            regenerateQuestion={answer[0]}
                                        />
                                    </div>
                                </div>
                            ))}

                            {isLoading && (
                                <>
                                    <UserChatMessage message={lastQuestionRef.current} />
                                    <div className={styles.chatMessageGptMinWidth}>
                                        <AnswerLoading />
                                    </div>
                                </>
                            )}
                            {error ? (
                                <>
                                    <UserChatMessage message={lastQuestionRef.current} />
                                    <div className={styles.chatMessageGptMinWidth}>
                                        <AnswerError error={error.toString()} onRetry={() => makeApiRequest(lastQuestionRef.current)} />
                                    </div>
                                </>
                            ) : null}
                            <div ref={chatMessageStreamEnd} />
                        </div>
                    )}
                    {/* Chat Input */}
                    <div className={styles.chatInput}>
                        {/* Stop Generate  */}
                        <div>
                            {isAnswerCompleted && !isLoading && (
                                <button
                                    className={styles.stopButtonContent}
                                    onClick={() => {
                                        stopGeneratingAnswer();
                                    }}
                                >
                                    <div id="stop" className={styles.stopButton} title={`${stopGenerating ? "Continue" : "Stop Generate Response"}`}>
                                        <FaStop style={{ fontSize: "11px" }} />
                                        {/* {" "} */}
                                    </div>
                                    <div className={styles.stopText1} style={{ color: isDarkTheme ? "white" : "black" }}>
                                        Stop Responding
                                    </div>
                                </button>
                            )}
                            {/* QuestionInput/ Input Bar / Chat Input*/}
                            <QuestionInput
                                fileuploadelement={fileuploadelement()}
                                clearchat={clearChat}
                                isLoading={isLoading}
                                lastQuestionRef={lastQuestionRef}
                                clearOnSend
                                disabled={isAnswerCompleted}
                                onSend={question => makeApiRequest(question)}
                                placeholder="Ask me a question..."
                                value={isContent ? contentValue : ""}
                                isContent={isContent}
                            />
                        </div>
                    </div>
                    <div className={styles.chatInput}>
                        {embeddingsLoaded == false ? (
                            <>
                                <Text className={styles.customPromptMessageResponse} style={{ color: isDarkTheme ? "white" : "black" }}>
                                    {
                                        // isLoading &&
                                        isAnswerCompleted && (
                                            <>
                                                {" "}
                                                The response is being generated <span className={styles.loadingdots} />{" "}
                                            </>
                                        )
                                    }
                                </Text>
                            </>
                        ) : (
                            // disclaimer Message for file upload
                            <div className={styles.customPromptMessage}>
                                <Text
                                    className={styles.customPromptMessage}
                                    style={{ color: isDarkTheme ? "white" : "black", marginBottom: promptTemplate == "" ? "0" : "-5px", fontSize: "11px" }}
                                >
                                    {uploaded_files[0].endsWith(".xlsx") ? (
                                        <>
                                            {`The responses are being fetched from the document ${uploaded_files[0]}.`}
                                            <span onClick={() => setOpenGuidlinesAlert(!openGuidlinesAlert)} className={styles.guidelines}>
                                                Guidelines...
                                            </span>
                                            <Snackbar
                                                open={openGuidlinesAlert}
                                                // autoHideDuration={12000}
                                                onClose={handleAlertClose}
                                                anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
                                                sx={{ marginBottom: "10%" }}
                                            >
                                                <Alert onClose={handleAlertClose} severity="info" sx={{ width: "100%" }}>
                                                    <AlertTitle sx={{ fontSize: "11px", fontWeight: "800" }}>Guidelines to Q&A with Excel File:</AlertTitle>
                                                    <p style={{ fontSize: "11px" }}>
                                                        {`• Mention the column name and worksheet name (if multiple columns of the same name are present 
                                                        in other worksheets as well) from which you want the data to be extracted.
                                                        • Mention the worksheet name, in addition to the question in the input.
                                                        • Kindly be more specific about the ask in the input.`}
                                                    </p>
                                                </Alert>
                                            </Snackbar>
                                        </>
                                    ) : uploaded_files[0].endsWith(".csv") ? (
                                        <>
                                            {`The responses are being fetched from the document ${uploaded_files[0]}.`}
                                            <span onClick={() => setOpenGuidlinesAlert(true)} className={styles.guidelines}>
                                                Guidelines...
                                            </span>
                                            <Snackbar
                                                open={openGuidlinesAlert}
                                                // autoHideDuration={12000}
                                                onClose={handleAlertClose}
                                                anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
                                                sx={{ marginBottom: "8%" }}
                                            >
                                                <Alert onClose={handleAlertClose} severity="info" sx={{ width: "100%" }}>
                                                    <AlertTitle sx={{ fontSize: "11px", fontWeight: "800" }}>Guidelines to Q&A with CSV File:</AlertTitle>
                                                    <p style={{ fontSize: "11px" }}>
                                                        {`• Mention the column name from which you want the data to be extracted.
                                                        • Kindly be more specific about the ask in the input.`}
                                                    </p>
                                                </Alert>
                                            </Snackbar>
                                        </>
                                    ) : (
                                        `The responses are being fetched from document ${uploaded_files[0]}.`
                                    )}
                                    {/* Custom Prompt */}

                                    {/* Clear Document */}
                                    <button className={styles.clearPrompt} onClick={deleteEmbeddingsforchat} style={{ color: isDarkTheme ? "white" : "" }}>
                                        <Text>
                                            <u>
                                                <i>Clear Document</i>
                                            </u>
                                        </Text>
                                    </button>
                                </Text>
                            </div>
                        )}
                        {promptTemplate == "" ? (
                            <div></div>
                        ) : (
                            !isAnswerCompleted && (
                                <div className={styles.customPromptMessage}>
                                    <Text
                                        className={styles.customPromptMessage}
                                        style={{
                                            color: isDarkTheme ? "white" : "",
                                            fontSize: "11px",
                                            // marginBottom: embeddingsLoaded == false ? "0" : "-5px",
                                            // marginBottom: !embeddingsLoaded ? "0" : "5px",
                                            // marginTop: !embeddingsLoaded ? "0" : "-5px",
                                            overflow: "hidden"
                                        }}
                                    >
                                        *Assistant behaviour is being modified by custom prompt.
                                        <button className={styles.clearPrompt} onClick={clearPrompt}>
                                            <Text>
                                                <u>
                                                    <i>Clear Prompt</i>
                                                </u>
                                            </Text>
                                        </button>
                                    </Text>
                                </div>
                            )
                        )}
                        <QuestionInput
                            fileuploadelement={fileuploadelement()}
                            clearchat={clearChat}
                            isLoading={isLoading}
                            lastQuestionRef={lastQuestionRef}
                            clearOnSend
                            placeholder="Ask me a question..."
                            disabled={isAnswerCompleted}
                            onSend={question => makeApiRequest(question)}
                            value={contentValue}
                            isContent={isContent}
                        />
                        <Snackbar
                            open={openDocClearAlertforchat}
                            autoHideDuration={12000}
                            onClose={handleAlertClose}
                            anchorOrigin={{ vertical: "top", horizontal: "center" }}
                        >
                            <Alert onClose={handleAlertClose} severity="info" sx={{ width: "100%" }}>
                                *The responses are not being fetched from the document.
                            </Alert>
                        </Snackbar>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Chat;
