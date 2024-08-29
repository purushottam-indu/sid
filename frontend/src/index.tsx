import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import { createHashRouter, RouterProvider } from "react-router-dom";
import { initializeIcons } from "@fluentui/react";

import "./index.css";

import Layout from "./pages/layout/Layout";
import Chat from "./pages/AIchat/Chat";
import { ThemeProvider } from "./ThemeContext";

initializeIcons();
function App() {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [promptTemplate, setPromptTemplate] = useState<string>("");

    // Define the router configuration
    const router = createHashRouter([
        {
            path: "/",
            element: (
                <Layout
                    isSidebarOpen={isSidebarOpen}
                    setIsSidebarOpen={setIsSidebarOpen}
                    promptTemplate={promptTemplate}
                    setPromptTemplate={setPromptTemplate}
                />
            ),
            children: [
                {
                    index: true,
                    element: <Chat isSideBarOpen={isSidebarOpen} promptTemplate={promptTemplate} setPromptTemplate={setPromptTemplate} />
                },
                {
                    path: "*",
                    lazy: () => import("./pages/NoPage")
                }
            ]
        }
    ]);

    // Render the router
    return (
        <React.StrictMode>
            <ThemeProvider>
                <RouterProvider router={router} />
            </ThemeProvider>
        </React.StrictMode>
    );
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(<App />);
