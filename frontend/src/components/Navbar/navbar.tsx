import React, { useEffect, useRef, useState } from "react";
import * as IoIcons from "react-icons/io";
import { Link } from "react-router-dom";
import { SidebarData } from "./sidebar";
import "./navbar.css";
import { IconContext } from "react-icons";
import { useBoolean } from "@fluentui/react-hooks";
import GeneralHelp from "../../components/GeneralHelp/GeneralHelp";
import { logoutApi } from "../../api";
import { TextField, Dialog, DialogType, PrimaryButton, DialogFooter } from "@fluentui/react";
import { createHashRouter } from "react-router-dom";
import { useTheme } from "../../ThemeContext";
import Switch from "../../components/Switch/Switch";

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
const getStyles1 = () => ({
    main: [
        {
            borderRadius: "15px",
            selectors: {
                ["@media (min-width: 720px)"]: {
                    maxHeight: "80%",
                    minWidth: "500px",
                    maxWidth: "600px"
                }
            }
        }
    ]
});

interface NavbarProps {
    toggleNavbar: () => void;
    onParameters: () => void;
    setIsSidebarOpen: (isSidebarOpen: boolean) => void; // to pass the boolean value back to heirarchy
    isSidebarOpen: boolean;
    promptTemplate: string;
    setPromptTemplate: (promptTemplate: string) => void;
}

const Navbar = ({ onParameters, isSidebarOpen, setIsSidebarOpen, promptTemplate, setPromptTemplate }: NavbarProps) => {
    const [isOpen, { setTrue: openHelpWindow, setFalse: dismissHelpWindow }] = useBoolean(false);
    const [sidebar, setSidebar] = useState<boolean>(false);
    const [isConfigPanelOpen, setIsConfigPanelOpen] = useState(false);
    const promptHasChanged = useRef<boolean>(false);
    const [userName, setUserName] = useState<string>("user.name");
    const { isDarkTheme, toggleTheme } = useTheme();
    const navbarRef = useRef<HTMLDivElement>(null);

    const handleClickOutside = (event: MouseEvent) => {
        if (navbarRef.current && !navbarRef.current.contains(event.target as Node)) {
            setIsSidebarOpen(false);
        }
    };

    useEffect(() => {
        document.addEventListener("mousedown", handleClickOutside);

        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [navbarRef]);

    function getCookie(name: string) {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                return cookie.substring(name.length + 1);
            }
        }
        return "user.name";
    }

    useEffect(() => {
        const name = getCookie("username");
        const decodedName = decodeURIComponent(name.replace(/^"(.*)"$/, "$1").replace(/\\054/g, ","));
        console.log(decodedName);

        setUserName(decodedName);
    }, []);

    const closeConfigPanel = () => {
        setIsConfigPanelOpen(false);
        if (promptHasChanged.current == true) {
            clearChat();
            promptHasChanged.current = false;
        }
    };

    const clearChat = () => {
        // lastQuestionRef.current = "";
        // error && setError(undefined);
        // setActiveCitation(undefined);
        // setActiveAnalysisPanelTab(undefined);
        // setAnswers([]);
    };

    const clearPrompt = () => {
        setPromptTemplate("");
        clearChat();
    };

    const onPromptTemplateChange = (_ev?: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, newValue?: string) => {
        setPromptTemplate(newValue || "");
        promptHasChanged.current = true;
    };

    const [isDraggable, { toggle: toggleIsDraggable }] = useBoolean(false);
    const modalPropsStyles = { type: DialogType.normal, main: { maxWidth: 2000 } };
    const modalProps = React.useMemo(
        () => ({
            isBlocking: true,
            // title: "Customize ChatDSI",
            styles: modalPropsStyles
            //  dragOptions: isDraggable ? dragOptions : undefined
        }),

        [isDraggable]
    );

    const showSidebar = (): void => {
        console.log("before", isSidebarOpen);
        setIsSidebarOpen(!isSidebarOpen);
        console.log("after", isSidebarOpen);
    };

    const handleHelpClick = (e: React.MouseEvent) => {
        e.preventDefault();
        openHelpWindow();
    };

    // Define the router configuration
    const router = createHashRouter([
        {
            path: "/",
            lazy: () => import("../../pages/NoPage")
        }
    ]);

    const handleLogout = async () => {
        try {
            const response = await logoutApi();
            const data = await response.json();
            if (!response.ok) {
                const errorText = await response.text();
                console.log("Failed to logout:", errorText);
                console.error("Failed to logout:", errorText);
                alert("Failed to logout: " + errorText);
                // return;
            }

            // console.log(data, "data output");
            console.log(response.status, "response.status");
            // console.log(response.text(), "response text");
            // console.log(response.json(), "response json");
            console.log(response, "response");
            if (response.ok) {
                // Assuming the backend will return a success message or status

                alert(
                    decodeURIComponent(
                        getCookie("username")
                            .replace(/^"(.*)"$/, "$1")
                            .replace(/\\054/g, ",")
                    ) + " logged out successfully"
                );
                console.log("Logged out from frontend");
                window.location.replace(data.auth_url);
            } else {
                console.log("Response not ok and failed to logout");
                console.error("Failed to logout");
            }
        } catch (error) {
            console.log("error and failed to logout", error);
            console.error("An error occurred during logout", error);
        }
    };

    const dragOptions = {
        moveMenuItemText: "Move",
        closeMenuItemText: "Close"
    };

    const handleFeedbackClick = () => {
        window.open(
            "https://forms.office.com/Pages/ResponsePage.aspx?id=h5QXsCYw90S81iXtRSE40Cg1HtlUAJ5AviIohVLonMhUOFhCSzZSNjRBQ1VZTlhNU09HOVhRRTdDQy4u",
            "_blank"
        );
    };

    const sidebarItems = SidebarData(isDarkTheme);

    return (
        <div ref={navbarRef}>
            <IconContext.Provider value={{ color: "#fff" }}>
                <div className={`navbar ${isDarkTheme ? "dark-theme" : "bright-theme"}`}>
                    <button className="menu-bars no-border" onClick={showSidebar}>
                        <IoIcons.IoMdMenu style={{ color: isDarkTheme ? "white" : "black" }} />
                    </button>
                </div>
                <nav className={`nav-menu ${isSidebarOpen ? "active" : ""} ${isDarkTheme ? "dark-theme" : "bright-theme"}`}>
                    <ul className={"nav-menu-items"}>
                        {sidebarItems.map((item, index) => (
                            <li key={index} className={item.cName}>
                                {item.path ? (
                                    <Link to={item.path}>
                                        <div>
                                            <div className="navbar-icons">{item.icon}</div>
                                            <span className="navtextSpan">{item.title}</span>
                                        </div>
                                        <span>{">"}</span>
                                    </Link>
                                ) : item.title === "Help" ? (
                                    <div onClick={handleHelpClick} className="nav-text-clickable">
                                        <div className="navbar-icons">{item.icon}</div>
                                        <span className="navtextSpan">{item.title}</span>
                                    </div>
                                ) : item.title === "Feedback" ? (
                                    <div onClick={handleFeedbackClick} className="nav-text-clickable ">
                                        <div className="navbar-icons">{item.icon}</div>
                                        <span className="navtextSpan">{item.title}</span>
                                    </div>
                                ) : item.title === "Customize" ? (
                                    <div onClick={() => setIsConfigPanelOpen(!isConfigPanelOpen)} className="nav-text-clickable ">
                                        <div className="navbar-icons">{item.icon}</div>
                                        <span className="navtextSpan">{item.title}</span>
                                    </div>
                                ) : item.title === "Logout" ? (
                                    <div onClick={handleLogout}>
                                        <div className="navbar-icons">{item.icon}</div>
                                        <span className="navtextSpan"> {item.title}</span>
                                    </div>
                                ) : item.title === "username" ? (
                                    <div>
                                        <div className="navbar-icons">{item.icon}</div>
                                        <span className="navtextSpan">{userName}</span>
                                    </div>
                                ) : item.isSwitch ? (
                                    <div>
                                        <Switch checked={isDarkTheme} onChange={toggleTheme} />
                                        <span className="theme-text navtextSpan">{isDarkTheme ? "Dark Mode" : "Light Mode"}</span>
                                    </div>
                                ) : (
                                    <>
                                        {/* {getCookie("username")} */}
                                        <div className="navbar-icons">{item.icon}</div>
                                        <span className="navtextSpan">{item.title}</span>
                                    </>
                                )}
                            </li>
                        ))}
                    </ul>
                </nav>
                <Dialog
                    hidden={!isOpen}
                    onDismiss={dismissHelpWindow}
                    modalProps={modalProps}
                    dialogContentProps={{
                        title: "ChatDSI Helper",
                        closeButtonAriaLabel: "Close"
                    }}
                    styles={getStyles}
                >
                    <GeneralHelp />
                </Dialog>
                <div className="customizeChatDSI">
                    <Dialog
                        dialogContentProps={{
                            title: "Customize ChatDSI's Behavior",
                            closeButtonAriaLabel: "Save"
                        }}
                        modalProps={modalProps}
                        hidden={!isConfigPanelOpen}
                        // isBlocking={false}
                        onDismiss={() => setIsConfigPanelOpen(false)}
                        styles={getStyles1}
                    >
                        <DialogFooter>
                            <PrimaryButton className="saveConfigPanel" onClick={closeConfigPanel} text="Save" />
                        </DialogFooter>

                        <hr style={{ margin: "0px 0", color: "red" }} />
                        <div className="parameterstext1">
                            Customize your chat experience by assigning roles to ChatDSI that meet specific needs. For example, in the Custom Prompt field
                            below, instruct ChatDSI to function as a proficient French translator or as a Python coding assistant or other unique roles.
                        </div>
                        <TextField
                            defaultValue={promptTemplate}
                            label="Custom Prompt"
                            multiline
                            rows={5}
                            autoAdjustHeight
                            onChange={onPromptTemplateChange}
                            className="chatPromptTemplate"
                            placeholder="Tell ChatDSI to take on a specific role and respond to all queries in that manner."
                        />

                        <div className="parameterstext2">
                            When you hit save, this will override ChatDSI's usual behavior, and it will only function as instructed until the prompt is cleared
                            via the "Clear Prompt" link that will appear above the prompt bar. More on this feature can be found in the user manual.
                        </div>
                    </Dialog>
                </div>
            </IconContext.Provider>
        </div>
    );
};

export default Navbar;
