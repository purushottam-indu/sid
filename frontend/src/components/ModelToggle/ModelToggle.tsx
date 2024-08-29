import * as React from "react";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import { Box, Tooltip } from "@mui/material";
import { Approaches } from "../../api";

interface Props {
    value: string;
    handleChange: () => void;
    disabled: boolean;
}

export default function ModelToggleButton({ handleChange, value, disabled }: Props) {
    return (
        <ToggleButtonGroup color="primary" value={value} exclusive onChange={handleChange} aria-label="Platform" disabled={disabled}>
            <ToggleButton value={"GPT3.5"} style={{ minWidth: "6rem" }} title="For faster response" sx={{ p: 1 }}>
                <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                    <span style={{ fontSize: "1rem" }}>GPT 3.5</span>
                    <span style={{ fontSize: "0.54rem" }}>Input ($0.003/1k tokens)</span>
                    <span style={{ fontSize: "0.54rem" }}>Output ($0.004/1k tokens)</span>
                </div>
            </ToggleButton>

            <ToggleButton value={"GPT4"} title="More precise but responses can take longer" style={{ minWidth: "6rem" }}>
                <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                    <span style={{ fontSize: "1rem" }}>GPT 4</span>
                    <span style={{ fontSize: "0.54rem" }}>Input ($0.01/1k tokens)</span>
                    <span style={{ fontSize: "0.54rem" }}>Output ($0.03/1k tokens)</span>
                </div>
            </ToggleButton>
        </ToggleButtonGroup>
    );
}
