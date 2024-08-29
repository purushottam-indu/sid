import * as React from "react";
import "./FileUpload.css";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import { TextField, Divider, Backdrop, CircularProgress, Snackbar, Alert, Tooltip } from "@mui/material";
import { ArrowUpload24Regular, CheckmarkCircle24Filled, Dismiss24Regular, DeleteDismiss24Filled } from "@fluentui/react-icons";
import Dropzone from "react-dropzone";
// import FileUploadIcon from "@mui/icons-material/FileUpload";
import { AiOutlineFile } from "react-icons/ai";
import { display } from "html2canvas/dist/types/css/property-descriptors/display";

interface Props {
    open: boolean;
    fileNames: string[];
    isEmbeddingsLoading: boolean;
    embeddingsLoaded: boolean;
    openAlert: boolean;
    openWarning: boolean;
    infoAlert: boolean;
    openDocClearAlert: boolean;
    handleCloseModal: () => void;
    handleSubmitFile: (event: React.FormEvent) => void;
    handleFileUpload: (uploadedFiles: File[]) => void;
    handleAlertClose: () => void;
    // handleWarningClose: () => void;
    // clearEmbeddings: () => void;
    deleteEmbeddings: () => void;
    openSnackbar: boolean;
    snackbarMessage: string;
    handleSnackbarClose: () => void;
    // handleinfoAlertClose: () => void;
}

export default function FileUploadModal({
    open,
    fileNames,
    isEmbeddingsLoading,
    embeddingsLoaded,
    openAlert,
    openWarning,
    infoAlert,
    openDocClearAlert,
    handleCloseModal,
    handleSubmitFile,
    handleFileUpload,
    handleAlertClose,
    // handleWarningClose,
    // handleinfoAlertClose,
    // clearEmbeddings,
    deleteEmbeddings,
    openSnackbar,
    snackbarMessage,
    handleSnackbarClose
}: Props) {
    // const [open, setOpen] = React.useState(false);
    // const handleOpen = () => setOpen(true);
    // const handleClose = () => setOpen(false);

    return (
        <div>
            <Modal open={open} onClose={handleCloseModal} aria-labelledby="modal-modal-title" aria-describedby="modal-modal-description">
                <Box className="upload-box">
                    <div className="flex-row-2">
                        <Typography id="modal-modal-title" variant="h6" component="h2" sx={{ display: "inline-block", width: "75%" }}>
                            Upload Document
                        </Typography>
                        <Button variant="text" onClick={handleCloseModal}>
                            <Dismiss24Regular />
                        </Button>
                    </div>
                    {/* <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                        Duis mollis, est non commodo luctus, nisi erat porttitor ligula.
                    </Typography> */}
                    <form onSubmit={handleSubmitFile}>
                        <Box sx={{ px: 2, m: 2 }}>
                            <Dropzone onDrop={handleFileUpload}>
                                {({ getRootProps, getInputProps }) => (
                                    <Box
                                        {...getRootProps()}
                                        className="center-column"
                                        sx={{
                                            height: 360,
                                            width: "100%",
                                            p: 2,
                                            border: "1px dashed grey",
                                            borderTop: "4px solid #0197f6",
                                            borderRadius: "16px"
                                        }}
                                    >
                                        <input {...getInputProps()} />
                                        <Box>
                                            {fileNames.length > 0 ? (
                                                <Box sx={{ display: "flex", flexDirection: "column" }}>
                                                    <AiOutlineFile style={{ fontSize: 30, margin: "auto", marginTop: 30, marginBottom: 10 }} />
                                                    <Typography sx={{ m: "auto" }}>Selected file:</Typography>
                                                    <ul>
                                                        {fileNames.map((name, index) => (
                                                            <li key={index}>{name}</li>
                                                        ))}
                                                    </ul>
                                                </Box>
                                            ) : (
                                                <Box sx={{ display: "flex", flexDirection: "column" }}>
                                                    {/* <FileUploadIcon style={{ fontSize: 30 }} /> */}
                                                    <ArrowUpload24Regular style={{ fontSize: 30, margin: "auto", marginTop: 30, marginBottom: 10 }} />
                                                    <Typography sx={{ m: "auto", textAlign: "center" }}>
                                                        Drag and drop a PDF/TXT/DOCX/PPTX/CSV/XLSX file here or Click to browse
                                                    </Typography>
                                                    <Typography sx={{ m: "auto" }}>{"[Total File Size Limit: 10MB]"}</Typography>
                                                </Box>
                                            )}
                                        </Box>
                                    </Box>
                                )}
                            </Dropzone>
                            {embeddingsLoaded && (
                                <Box sx={{ marginTop: -4, marginLeft: 1 }}>
                                    <CheckmarkCircle24Filled color="green" />
                                </Box>
                            )}
                        </Box>
                        <Box sx={{ py: 4 }}>
                            <Typography variant="h6"></Typography>
                            <Divider />
                        </Box>

                        <div className="flex-row-2">
                            <Box className="center-column" sx={{ display: "inline-block", width: "75%" }}>
                                <Button variant="contained" type="submit" sx={{ width: 200 }}>
                                    Submit
                                </Button>
                            </Box>
                            <Box sx={{ display: "inline-block" }} onClick={deleteEmbeddings}>
                                <Tooltip title="Delete File" placement="top">
                                    <Button>
                                        <DeleteDismiss24Filled color="red" />
                                    </Button>
                                </Tooltip>
                            </Box>
                        </div>
                    </form>
                    <Backdrop sx={{ color: "#fff", zIndex: theme => theme.zIndex.drawer + 4 }} open={isEmbeddingsLoading}>
                        <CircularProgress color="inherit" />
                    </Backdrop>
                </Box>
            </Modal>
            <Snackbar open={openAlert} autoHideDuration={6000} onClose={handleAlertClose}>
                <Alert onClose={handleAlertClose} severity="success" sx={{ width: "100%" }}>
                    File uploaded successfully !
                </Alert>
            </Snackbar>
            <Snackbar open={openWarning} autoHideDuration={6000} onClose={handleAlertClose} anchorOrigin={{ vertical: "top", horizontal: "center" }}>
                <Alert onClose={handleAlertClose} severity="warning" sx={{ width: "100%" }}>
                    File with maximum size of 10MB is allowed !
                </Alert>
            </Snackbar>
            <Snackbar
                open={openSnackbar} // State controlling whether the Snackbar is open
                autoHideDuration={4500}
                onClose={handleSnackbarClose} // Function to handle closing the Snackbar
                anchorOrigin={{ vertical: "bottom", horizontal: "left" }}
            >
                <Alert onClose={handleSnackbarClose} severity="error" sx={{ width: "100%" }}>
                    {snackbarMessage}
                </Alert>
            </Snackbar>
            <Snackbar open={openDocClearAlert} autoHideDuration={12000} onClose={handleAlertClose} anchorOrigin={{ vertical: "top", horizontal: "center" }}>
                <Alert onClose={handleAlertClose} severity="info" sx={{ width: "100%" }}>
                    *The responses are not being fetched from the document.
                </Alert>
            </Snackbar>
            <Snackbar open={infoAlert} autoHideDuration={6000} onClose={handleAlertClose} anchorOrigin={{ vertical: "top", horizontal: "center" }}>
                <Alert onClose={handleAlertClose} severity="info" sx={{ width: "100%" }}>
                    File with size above 5MB takes more time to process, Please be patient !
                </Alert>
            </Snackbar>
        </div>
    );
}
